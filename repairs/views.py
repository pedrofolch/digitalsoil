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

from .serializers import RepairSerializer, RepairOrderSerializer
from comments.forms import CommentForm
from comments.models import Comment
from repairs.forms import RepairForm, RepairOrderForm
from repairs.models import RepairFile, RepairOrder
from .permissions import IsOwnerOrReadOnly


def repiar_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/repairs/')
    else:
        return redirect('/login/')


def user_gains_perms(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.has_perm('repairs.repair_create')

    content_type = ContentType.objects.get_for_model(RepairFile)
    permission = Permission.objects.get(
        codename='repair_create',
        content_type=content_type,
    )
    user.user_permissions.add(permission)

    user.has_perm('repairs.repair_create')

    user = get_object_or_404(User, pk=user_id)

    user.has_perm('repairs.repair_create')


def repair_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = RepairForm(request.POST or None, request.FILES or None)
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
    return render(request, "repairs/snippets/form-snippet.html", context)


def repair_detail(request, slug=None):
    instance = get_object_or_404(RepairFile, slug=slug)
    # if instance.publish > timezone.now().date() or instance.draft:
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
    return render(request, "repairs/repair_detail.html", context)


def repair_list(request):
    today = timezone.now().date()
    queryset_list = RepairFile.objects.all()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = RepairFile.objects.all()

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
        "title": "Repairs and Invoices",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "repairs/repair_list.html", context)


def repair_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(RepairFile, slug=slug)
    form = RepairForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "repairs/snippets/form-snippet.html", context)


def repair_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(RepairFile, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("repairs:repair_list")


class RepairPageNumberPagination(pagination.PageNumberPagination):
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


class RepairDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepairFile.objects.all()
    serializer_class = RepairSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RepairListCreateAPIView(generics.ListCreateAPIView):
    queryset = RepairFile.objects.all()
    serializer_class = RepairSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = RepairPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def repair_order_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/repair-order/')
    else:
        return redirect('/login/')


def user_order_gains_perms(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.has_perm('repairs.repair_order_create')

    content_type = ContentType.objects.get_for_model(RepairOrder)
    permission = Permission.objects.get(
        codename='repair_order_create',
        content_type=content_type,
    )
    user.user_permissions.add(permission)

    user.has_perm('repairs.repair_order_create')

    user = get_object_or_404(User, pk=user_id)

    user.has_perm('repairs.repair_order_create')


def repair_order_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = RepairOrderForm(request.POST or None, request.FILES or None)
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
    return render(request, "repairs/snippets/form-snippet.html", context)


def repair_order_detail(request, slug=None):
    instance = get_object_or_404(RepairOrder, slug=slug)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    share_string = quote_plus(instance.problem_found)

    initial_data = {
            "content_type": instance.get_content_type,
            "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated:
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get("problem_found")
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
    return render(request, "repairs/repair_order_detail.html", context)


def repair_order_list(request):
    today = timezone.now().date()
    queryset_list = RepairOrder.objects.all()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = RepairOrder.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(problem_found__icontains=query) |
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
        "title": "Repairs Order",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "repairs/repair_order_list.html", context)


def repair_order_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(RepairFile, slug=slug)
    form = RepairOrderForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "repairs/snippets/form-snippet.html", context)


def repair_order_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(RepairOrder, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("repairs:repair_order_list")


class RepairOrderPageNumberPagination(pagination.PageNumberPagination):
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


class RepairOrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RepairOrder.objects.all()
    serializer_class = RepairOrderSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RepairOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = RepairOrder.objects.all()
    serializer_class = RepairOrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = RepairOrderPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
