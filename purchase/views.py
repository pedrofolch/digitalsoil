try:
    from urllib.parse import quote_plus  # python 3
except:
    pass
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from django.views.generic import ListView, DetailView as DetailsView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View as Views
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission, User
from comments.forms import CommentForm
from comments.models import Comment
from .permissions import IsOwnerOrReadOnly
from purchase.api.serializers import PurchaseSerializer
from purchase.forms import PurchaseOrderForm
from purchase.models import PurchaseOrder
from analytics.models import View
from .utils import AjaxableResponseMixin


def purchase_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/order/')
    else:
        return redirect('/login/')


def user_gains_perms(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.has_perm('purchase.purchase_order_create')

    content_type = ContentType.objects.get_for_model(PurchaseOrder)
    permission = Permission.objects.get(
        codename='purchase_order_create',
        content_type=content_type,
    )
    user.user_permissions.add(permission)

    user.has_perm('purchase.purchase_order_create')

    user = get_object_or_404(User, pk=user_id)

    user.has_perm('purchase.purchase_order_create')


class PurchaseView(Views):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            object_list = PurchaseOrder.objects.set_filter(public=True).order_by('-timestamp')
            return render(request, "folch2iot.html", {"object_list": object_list})

        user = request.user
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        qs = PurchaseOrder.objects.filter(user__id__in=is_following_user_ids, public=True).order_by("-update")[:3]
        return render(request, "purchase/home-feed.html", {'object_list': qs})

#
# class SupplierDetailView(LoginRequiredMixin, DetailsView):
#     def get_queryset_supplier(self):
#         return Supplier.objects.filter(user=self.request.user)


class PurchaseListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = PurchaseOrder.objects.filter(
                Q(post__ixecact=slug) |
                Q(categroy__iexact=slug) |
                Q(category__icontains=slug)
            )
            return queryset
        else:
            return PurchaseOrder.objects.filter(user=self.request.user)


class PurchaseCreateView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    form_class = PurchaseOrderForm
    login_url = '/login/'
    template_name = 'purchase/form.html'
    success_url = "/order/"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super(PurchaseCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(PurchaseCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Add Purchase Order'
        return context


class PurchaseUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PurchaseOrderForm
    login_url = '/login/'
    template_name = 'purchase/detail.html'
    success_url = 'order/'

    def get_context_data(self, *args, **kwargs):
        context = super(PurchaseUpdateView, self).get_context_data(**kwargs)
        name = self.get_object().title
        context['title'] = f'Update purchase order: {name}'
        return context

    def get_queryset(self):
        return PurchaseOrder.objects.filter(user=self.request.user)


class PurchaseDelete(DeleteView):
    model = PurchaseOrder
    success_url = reverse_lazy


# class HomeView(View):
#     def get(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             object_list = Supplier.objects.set_filter(public=True).order_by('-pub_date')
#             return render(request, "folch2iot.html", {"object_list": object_list})
#
#         user = request.user
#         is_following_user_ids = [x.user.id for x in user.is_following.all()]
#         qs = Supplier.objects.set_filter(user__id__in=is_following_user_ids, public=True).order_by("-update")[:3]
#         return render(request, "providers/home-feed.html", {'object_list': qs})


def purchase_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PurchaseOrderForm(request.POST or None, request.FILES or None)
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
    return render(request, "purchase/form.html", context)


def purchase_detail(request, slug=None):
    instance = get_object_or_404(PurchaseOrder, slug=slug)
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
    return render(request, "purchase/detail.html", context)


def purchase_list(request):
    today = timezone.now().date()
    queryset_list = PurchaseOrder.objects.filter(user=request.user)  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = PurchaseOrder.objects.all()

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
        "title": "Purchase Order",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "purchase/list.html", context)


def purchase_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(PurchaseOrder, slug=slug)
    form = PurchaseOrderForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "purchase/form.html", context)


def purchase_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(PurchaseOrder, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("purchase:list")


class PurchasePageNumberPagination(pagination.PageNumberPagination):
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


class PurchaseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class PurchaseDetailView(DetailsView):
    model = PurchaseOrder

    def get_object_purchase(self, **kwargs):
        post_slug = self.kwargs.get("slug")  # grab the primary key of the object
        post_query = PurchaseOrder.objects.filter(slug=post_slug)  # returns a list with the filtered results
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

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['request'] = self.request
    #     return context


class PurchaseListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PurchasePageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
