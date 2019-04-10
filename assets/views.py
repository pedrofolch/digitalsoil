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

from .api.serializers import AssetSerializer
from comments.forms import CommentForm
from comments.models import Comment
from assets.forms import TypeOfAssetForm, MarineAssetForm, AutomobileAssetForm, \
    EquipmentAssetForm, AssetForm, PartsForm, MarineVesselManufacturerForm, MarineModelTypeForm,\
    CarManufacturerForm, CarModelTypeForm, EquipmentManufacturerForm, EquipmentModelTypeForm, ThroughHullForm
from assets.models import TypeOfAsset, MarineVessel, Automobile, Equipment, Asset, Parts, MarineVesselManufacturer, \
    MarineModelType, CarManufacturer, CarModelType, EquipmentManufacturer, EquipmentModelType, ThroughHull
from .permissions import IsOwnerOrReadOnly
from analytics.models import View
from engine_room.models import Engines


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

    form = TypeOfAssetForm(request.POST or None, request.FILES or None)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def asset_asset_create(request):
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
    return render(request, "assets/snippets/form-snippet.html", context)


def parts_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PartsForm(request.POST or None, request.FILES or None)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def marine_manufacturer_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = MarineVesselManufacturerForm(request.POST or None, request.FILES or None)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def marine_model_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = MarineModelTypeForm(request.POST or None, request.FILES or None)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def car_manufacturer_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = CarManufacturerForm(request.POST or None, request.FILES or None)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def car_model_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = CarModelTypeForm(request.POST or None, request.FILES or None)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def equipment_manufacturer_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = EquipmentManufacturerForm(request.POST or None, request.FILES or None)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def equipment_model_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = EquipmentModelTypeForm(request.POST or None, request.FILES or None)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def through_hull_model_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = ThroughHullForm(request.POST or None, request.FILES or None)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def marine_asset_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = MarineAssetForm(request.POST or None, request.FILES or None)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def land_asset_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = AutomobileAssetForm(request.POST or None, request.FILES or None)
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
    return render(request, "assets/land_asset_form.html", context)


def equipment_asset_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = EquipmentAssetForm(request.POST or None, request.FILES or None)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def asset_detail(request, slug=None, pk=None):
    instance = get_object_or_404(TypeOfAsset, slug=slug)
    sea = get_object_or_404(MarineVessel, slug=slug)
    land = get_object_or_404(Automobile, slug=slug)
    asset = get_object_or_404(Asset, pk=pk)
    part = get_object_or_404(Parts, pk=pk)
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
        "sea": sea,
        "land": land,
        "asset": asset,
        "part": part,
    }
    # if instance.exist():
    #     post_object = slug.first()  # grab the first item in the list if it exists
    #     view, created = View.objects.get_or_create(
    #         user=request.user,
    #         post=post_object
    #     )  # specify the fields for the View object to be created
    #     if view:
    #         view.views_count += 1  # add 1 view onto the view tally
    #         view.save()
    #     return post_object
    return render(request, "assets/typeofasset_detail.html", context)


def asset_asset_detail(request, pk=None):
    instance = get_object_or_404(Asset, pk=pk)
    # if instance.publish >= timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    if pk.exists():
        post_object = pk.first()  # grab the first item in the list if it exists
        view, created = View.objects.get_or_create(
            user=request.user,
            post=post_object
        )  # specify the fields for the View object to be created
        if view:
            view.views_count += 1  # add 1 view onto the view tally
            view.save()
        return post_object
    return render(request, "assets/asset_detail.html", context)


def parts_detail(request, pk=None):
    instance = get_object_or_404(Parts, pk=pk)
    # if instance.publish >= timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    context = {
        "title": instance.title,
        "instance": instance,
    }
    if pk.exists():
        post_object = pk.first()  # grab the first item in the list if it exists
        view, created = View.objects.get_or_create(
            user=request.user,
            post=post_object
        )  # specify the fields for the View object to be created
        if view:
            view.views_count += 1  # add 1 view onto the view tally
            view.save()
        return post_object
    return render(request, "assets/parts_detail.html", context)


def marine_manufacturer_detail(request, pk=None):
    instance = get_object_or_404(MarineVesselManufacturer, pk=pk)
    # if instance.publish >= timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    context = {
        "title": instance.title,
        "instance": instance,
    }
    if pk.exists():
        post_object = pk.first()  # grab the first item in the list if it exists
        view, created = View.objects.get_or_create(
            user=request.user,
            post=post_object
        )  # specify the fields for the View object to be created
        if view:
            view.views_count += 1  # add 1 view onto the view tally
            view.save()
        return post_object
    return render(request, "assets/marine_manufacturer_detail.html", context)


def marine_model_detail(request, pk=None):
    instance = get_object_or_404(MarineModelType, pk=pk)
    # if instance.publish >= timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    context = {
        "title": instance.title,
        "instance": instance,
    }
    if pk.exists():
        post_object = pk.first()  # grab the first item in the list if it exists
        view, created = View.objects.get_or_create(
            user=request.user,
            post=post_object
        )  # specify the fields for the View object to be created
        if view:
            view.views_count += 1  # add 1 view onto the view tally
            view.save()
        return post_object
    return render(request, "assets/marine_model_detail.html", context)


def car_manufacturer_detail(request, pk=None):
    instance = get_object_or_404(CarManufacturer, pk=pk)
    # if instance.publish >= timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    context = {
        "title": instance.title,
        "instance": instance,
    }
    if pk.exists():
        post_object = pk.first()  # grab the first item in the list if it exists
        view, created = View.objects.get_or_create(
            user=request.user,
            post=post_object
        )  # specify the fields for the View object to be created
        if view:
            view.views_count += 1  # add 1 view onto the view tally
            view.save()
        return post_object
    return render(request, "assets/land_manufacturer_detail.html", context)


def car_model_detail(request, pk=None):
    instance = get_object_or_404(CarModelType, pk=pk)
    # if instance.publish >= timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    context = {
        "title": instance.title,
        "instance": instance,
    }
    if pk.exists():
        post_object = pk.first()  # grab the first item in the list if it exists
        view, created = View.objects.get_or_create(
            user=request.user,
            post=post_object
        )  # specify the fields for the View object to be created
        if view:
            view.views_count += 1  # add 1 view onto the view tally
            view.save()
        return post_object
    return render(request, "assets/land_model_detail.html", context)


def equipment_manufacturer_detail(request, pk=None):
    instance = get_object_or_404(EquipmentManufacturer, pk=pk)
    # if instance.publish >= timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    context = {
        "title": instance.title,
        "instance": instance,
    }
    if pk.exists():
        post_object = pk.first()  # grab the first item in the list if it exists
        view, created = View.objects.get_or_create(
            user=request.user,
            post=post_object
        )  # specify the fields for the View object to be created
        if view:
            view.views_count += 1  # add 1 view onto the view tally
            view.save()
        return post_object
    return render(request, "assets/equipment_manufacturer_detail.html", context)


def through_hull_detail(request, pk=None):
    instance = get_object_or_404(ThroughHull, pk=pk)
    # if instance.publish >= timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    context = {
        "title": instance.title,
        "instance": instance,
    }
    if pk.exists():
        post_object = pk.first()  # grab the first item in the list if it exists
        view, created = View.objects.get_or_create(
            user=request.user,
            post=post_object
        )  # specify the fields for the View object to be created
        if view:
            view.views_count += 1  # add 1 view onto the view tally
            view.save()
        return post_object
    return render(request, "assets/through_hull_detail.html", context)


def equipment_model_detail(request, pk=None):
    instance = get_object_or_404(EquipmentModelType, pk=pk)
    # if instance.publish >= timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    context = {
        "title": instance.title,
        "instance": instance,
    }
    if pk.exists():
        post_object = pk.first()  # grab the first item in the list if it exists
        view, created = View.objects.get_or_create(
            user=request.user,
            post=post_object
        )  # specify the fields for the View object to be created
        if view:
            view.views_count += 1  # add 1 view onto the view tally
            view.save()
        return post_object
    return render(request, "assets/equipment_model_detail.html", context)


def marine_asset_detail(request, slug=None):
    instance = get_object_or_404(MarineVessel, slug=slug)
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
        if slug.exists():
            post_object = slug.first()  # grab the first item in the list if it exists
            view, created = View.objects.get_or_create(
                user=request.user,
                post=post_object
            )  # specify the fields for the View object to be created
            if view:
                view.views_count += 1  # add 1 view onto the view tally
                view.save()
            return post_object
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = instance.comments
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "assets/marine_detail.html", context)


def land_asset_detail(request, slug=None):
    instance = get_object_or_404(Automobile, slug=slug)
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
    if slug.exists():
        post_object = slug.first()  # grab the first item in the list if it exists
        view, created = View.objects.get_or_create(
            user=request.user,
            post=post_object
        )  # specify the fields for the View object to be created
        if view:
            view.views_count += 1  # add 1 view onto the view tally
            view.save()
        return post_object
    return render(request, "assets/land_detail.html", context)


def equipment_asset_detail(request, slug=None):
    instance = get_object_or_404(Equipment, slug=slug)
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
        if slug.exists():
            post_object = slug.first()  # grab the first item in the list if it exists
            view, created = View.objects.get_or_create(
                user=request.user,
                post=post_object
            )  # specify the fields for the View object to be created
            if view:
                view.views_count += 1  # add 1 view onto the view tally
                view.save()
            return post_object
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = instance.comments
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "assets/equipment_detail.html", context)


def asset_list(request):
    today = timezone.now().date()
    asset = Asset.objects.filter(user=request.user)

    # queryset_list = TypeOfAsset.objects.all()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = TypeOfAsset.objects.filter(user__is_active=True)
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
            "engine_list": asset
        }
        return render(request, "assets/asset_list.html", context)


def marine_asset_list(request):
    today = timezone.now().date()
    engine = Asset.objects.filter(user=request.user)

    # queryset_list = TypeOfAsset.objects.all()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = MarineVessel.objects.all()
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
            "title": "Marine Vessel List",
            "page_request_var": page_request_var,
            "today": today,
            "engine_list": engine
        }
        return render(request, "assets/marine_asset_list.html", context)


def land_asset_list(request):
    today = timezone.now().date()
    engine = Engines.objects.filter(user=request.user)

    # queryset_list = TypeOfAsset.objects.all()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Automobile.objects.all()
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
            "title": "Engineering Vehicle List",
            "page_request_var": page_request_var,
            "today": today,
            "engine_list": engine
        }
        return render(request, "assets/land_asset_list.html", context)


def equipment_asset_list(request):
    today = timezone.now().date()
    engine = Engines.objects.filter(user=request.user)

    # queryset_list = TypeOfAsset.objects.all()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Equipment.objects.all()
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
            "title": "Equipment List",
            "page_request_var": page_request_var,
            "today": today,
            "engine_list": engine
        }
        return render(request, "assets/equipment_asset_list.html", context)


def asset_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(TypeOfAsset, slug=slug)
    form = TypeOfAssetForm(request.POST or None, request.FILES or None, instance=instance)
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


def asset_asset_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Asset, pk=pk)
    form = AssetForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "odometer": instance.odometer,
        "instance": instance,
        "form": form,
    }
    return render(request, "assets/snippets/form-snippet.html", context)


def parts_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Parts, pk=pk)
    form = PartsForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "part_number": instance.part_number,
        "price": instance.price,
        "instance": instance,
        "form": form,
    }
    return render(request, "assets/snippets/form-snippet.html", context)


def marine_manufacturer_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(MarineVesselManufacturer, pk=pk)
    form = MarineVesselManufacturerForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def marine_model_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(MarineModelType, pk=pk)
    form = MarineModelTypeForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def car_manufacturer_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(CarManufacturer, pk=pk)
    form = CarManufacturerForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def car_model_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(CarModelType, pk=pk)
    form = CarModelTypeForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "assets/land_model_form.html", context)


def equipment_manufacturer_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(CarManufacturer, pk=pk)
    form = EquipmentManufacturerForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def through_hull_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(ThroughHull, pk=pk)
    form = ThroughHullForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def equipment_model_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(CarModelType, pk=pk)
    form = EquipmentModelTypeForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def marine_asset_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(MarineVessel, slug=slug)
    form = MarineAssetForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def land_asset_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Automobile, slug=slug)
    form = AutomobileAssetForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def equipment_asset_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Equipment, slug=slug)
    form = EquipmentAssetForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "assets/snippets/form-snippet.html", context)


def asset_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(TypeOfAsset, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:list")


def asset_asset_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Asset, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:list")


def parts_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Parts, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:list")


def marine_manufacturer_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(MarineVesselManufacturer, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:list")


def marine_model_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(MarineModelType, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:list")


def car_manufacturer_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(CarManufacturer, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:list")


def car_model_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(CarModelType, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:list")


def equipment_manufacturer_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(EquipmentManufacturer, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:list")


def equipment_model_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(EquipmentModelType, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:list")


def through_hull_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(ThroughHull, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:list")


def marine_asset_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(MarineVessel, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:marine_list")


def land_asset_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Automobile, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:land_list")


def equipment_asset_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Equipment, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("assets:equipment_list")


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
