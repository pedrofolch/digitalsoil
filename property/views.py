try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission, User
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from django.views.generic import DetailView

from .serializers import AssetSerializer
from comments.forms import CommentForm
from comments.models import Comment
from assets.forms import AssetForm
from assets.models import TypeOfAsset
from engine_room.models import EngineSpecs
from .permissions import IsOwnerOrReadOnly
from analytics.models import View


def asset_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/assets/')
    else:
        return redirect('/login/')


def user_gains_perms(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.has_perm('assets.asset_create')

    content_type = ContentType.objects.get_for_model(TypeOfAsset)
    permission = Permission.objects.get(
        codename='asset_create',
        content_type=content_type,
    )
    user.user_permissions.add(permission)

    user.has_perm('assets.asset_create')

    user = get_object_or_404(User, pk=user_id)

    user.has_perm('assets.asset_create')


def asset_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = AssetForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()

        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "assets/asset_form.html", context)


def asset_detail(request, slug=None):
    instance = get_object_or_404(TypeOfAsset, slug=slug)
    # if instance.publish >= timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)

    initial_data = {
            "content_type": instance.get_content_type,
            "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated:
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = instance.comments
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "assets/typeofasset_detail.html", context)


def asset_list(request):
    today = timezone.now().date()
    engine = EngineSpecs.objects.filter(user=request.user)

    # queryset_list = TypeOfAsset.objects.all()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = TypeOfAsset.objects.all()
        query = request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()

        paginator = Paginator(queryset_list, 8)  # Show 25 contacts per page
        page_request_var = "page"
        page = request.GET.get(page_request_var)

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset = paginator.page(paginator.num_pages)

        context = {
            "object_list": queryset,
            "title": "Asset List",
            "page_request_var": page_request_var,
            "today": today,
            "engine_list": engine
        }
        return render(request, "assets/asset_list.html", context)


def asset_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(TypeOfAsset, slug=slug)
    form = AssetForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "assets/asset_form.html", context)


def asset_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(TypeOfAsset, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:list")


class AssetPageNumberPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 20

    def get_paginated_response(self, data):
        author = False
        user = self.request.user
        if user.is_authenticated:
            author = True
        context = {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'author': author,
            'results': data,
        }
        return Response(context)


class AssetDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TypeOfAsset.objects.all()
    serializer_class = AssetSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class AssetDetailView(DetailView):
    model = TypeOfAsset

    def get_object_asset(self, *args, **kwargs):
        post_slug = self.kwargs.get("slug")  # grab the primary key of the object
        post_query = TypeOfAsset.objects.filter(slug=post_slug)  # returns a list with the filtered results
        if post_query.exists():
            post_object = post_query.first()  # grab the first item in the list if it exists
            view, created = View.objects.get_or_create(
                user=self.request.user,
                post=post_object
            )  # specify the fields for the View object to be created
            if view:
                view.views_count += 1  # add 1 view onto the view tally
                view.save()
            return post_object
        raise Http404  # if the object does not exist


class AssetListCreateAPIView(generics.ListCreateAPIView):
    queryset = TypeOfAsset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = AssetPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
