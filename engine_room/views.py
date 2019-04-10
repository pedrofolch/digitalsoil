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

from .api.serializers import EnginesSerializer
from comments.forms import CommentForm
from comments.models import Comment
from engine_room.forms import EnginesForm, MainEngineForm, CenterEngineForm, \
    PortEngineForm, PortEngine2Form, PortEngine3Form, StarboardEngineForm, StarboardEngine2Form, StarboardEngine3Form, \
    AuxiliaryEngineForm, GenSetForm, GenSet2Form, ToolsForm
from engine_room.models import Engines, MainEngine, CenterEngine, PortEngine, \
    PortEngine2, PortEngine3, StarboardEngine, StarboardEngine2, StarboardEngine3, Auxiliary, GenSet, GenSet2, Tools
from .permissions import IsOwnerOrReadOnly


def engine_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/engine_room/')
    else:
        return redirect('/login/')


def user_gains_perms(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.has_perm('engine_room.engine_create')

    content_type = ContentType.objects.get_for_model(Engines)
    permission = Permission.objects.get(
        codename='engine_create',
        content_type=content_type,
    )
    user.user_permissions.add(permission)

    user.has_perm('engine_room.engine_create')

    user = get_object_or_404(User, pk=user_id)

    user.has_perm('engine_room.engine_create')


def engine_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = EnginesForm(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/engine_form.html", context)


def main_engine_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = MainEngineForm(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/main_engine_form.html", context)


def center_engine_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = CenterEngineForm(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/center_engine_form.html", context)


def port_engine_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PortEngineForm(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/port_engine_form.html", context)


def port_engine2_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PortEngine2Form(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/port_engine2_form.html", context)


def port_engine3_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PortEngine3Form(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/port_engine3_form.html", context)


def starboard_engine_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = StarboardEngineForm(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/starboard_engine_form.html", context)


def starboard_engine2_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = StarboardEngine2Form(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/starboard_engine2_form.html", context)


def starboard_engine3_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = StarboardEngine3Form(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/starboard_engine3_form.html", context)


def auxiliary_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = AuxiliaryEngineForm(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/auxiliary_form.html", context)


def genset_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = GenSetForm(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/genset_engine_form.html", context)


def genset2_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = GenSet2Form(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/genset_engine2_form.html", context)


def tools_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = ToolsForm(request.POST or None, request.FILES or None)
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
    return render(request, "engine_room/tool_form.html", context)


def engine_detail(request, slug=None):
    instance = get_object_or_404(Engines, slug=slug)
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
        except ContentType.DoesNotExist:
            parent_id = None
            content_type = ContentType.objects.get(model=c_type)

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
    return render(request, "engine_room/engine_detail.html", context)


def main_engine_detail(request, pk=None):
    instance = get_object_or_404(MainEngine, pk=pk)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    return render(request, "engine_room/main_engine_detail.html", context)


def center_engine_detail(request, pk=None):
    instance = get_object_or_404(CenterEngine, pk=pk)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    return render(request, "engine_room/center_engine_detail.html", context)


def port_engine_detail(request, pk=None):
    instance = get_object_or_404(PortEngine, pk=pk)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    return render(request, "engine_room/port_engine_detail.html", context)


def port_engine2_detail(request, pk=None):
    instance = get_object_or_404(PortEngine2, pk=pk)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    return render(request, "engine_room/port_engine2_detail.html", context)


def port_engine3_detail(request, pk=None):
    instance = get_object_or_404(PortEngine3, pk=pk)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    return render(request, "engine_room/port_engine3_detail.html", context)


def starboard_engine_detail(request, pk=None):
    instance = get_object_or_404(StarboardEngine, pk=pk)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    return render(request, "engine_room/starboard_engine_detail.html", context)


def starboard_engine2_detail(request, pk=None):
    instance = get_object_or_404(StarboardEngine2, pk=pk)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    return render(request, "engine_room/starboard_engine2_detail.html", context)


def starboard_engine3_detail(request, pk=None):
    instance = get_object_or_404(StarboardEngine3, pk=pk)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    return render(request, "engine_room/starboard_engine3_detail.html", context)


def auxiliary_engine_detail(request, pk=None):
    instance = get_object_or_404(Auxiliary, pk=pk)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    return render(request, "engine_room/auxiliary_engine_detail.html", context)


def genset_engine_detail(request, pk=None):
    instance = get_object_or_404(GenSet, pk=pk)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    return render(request, "engine_room/genset_engine_detail.html", context)


def genset_engine2_detail(request, pk=None):
    instance = get_object_or_404(GenSet2, pk=pk)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    return render(request, "engine_room/genset_engine2_detail.html", context)


def tool_detail(request, pk=None):
    instance = get_object_or_404(Tools, pk=pk)
    # if instance.publish > timezone.now().date() or instance.draft:
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    context = {
        "title": instance.serial_number,
        "instance": instance,
    }
    return render(request, "engine_room/tools_engine_detail.html", context)


def engine_list(request):
    today = timezone.now().date()
    queryset_list = Engines.objects.all()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Engines.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(engine_model__icontains=query) |
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
        "title": "Engine List",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "engine_room/engine_list.html", context)


def engine_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Engines, slug=slug)
    form = EnginesForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "engine_room/engine_form.html", context)


def main_engine_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(MainEngine, pk=pk)
    form = MainEngineForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "instance": instance,
        "form": form,
    }
    return render(request, "engine_room/main_engine_form.html", context)


def center_engine_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(CenterEngine, pk=pk)
    form = CenterEngineForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "instance": instance,
        "form": form,
    }
    return render(request, "engine_room/center_engine_form.html", context)


def port_engine_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(PortEngine, pk=pk)
    form = PortEngineForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "instance": instance,
        "form": form,
    }
    return render(request, "engine_room/port_engine_form.html", context)


def port_engine2_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(PortEngine2, pk=pk)
    form = PortEngine2Form(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "instance": instance,
        "form": form,
    }
    return render(request, "engine_room/port_engine2_form.html", context)


def port_engine3_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(PortEngine3, pk=pk)
    form = PortEngine3Form(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "instance": instance,
        "form": form,
    }
    return render(request, "engine_room/port_engine3_form.html", context)


def starboard_engine_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(StarboardEngine, pk=pk)
    form = StarboardEngineForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "instance": instance,
        "form": form,
    }
    return render(request, "engine_room/starboard_engine_form.html", context)


def starboard_engine2_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(StarboardEngine2, pk=pk)
    form = StarboardEngine2Form(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "instance": instance,
        "form": form,
    }
    return render(request, "engine_room/starboard_engine2_form.html", context)


def starboard_engine3_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(StarboardEngine3, pk=pk)
    form = StarboardEngine3Form(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "instance": instance,
        "form": form,
    }
    return render(request, "engine_room/starboard_engine3_form.html", context)


def auxiliary_engine_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Auxiliary, pk=pk)
    form = AuxiliaryEngineForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "instance": instance,
        "form": form,
    }
    return render(request, "engine_room/auxiliary_engine_form.html", context)


def genset_engine_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(GenSet, pk=pk)
    form = GenSetForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "instance": instance,
        "form": form,
    }
    return render(request, "engine_room/genset_engine_form.html", context)


def genset_engine2_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(GenSet2, pk=pk)
    form = GenSet2Form(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "instance": instance,
        "form": form,
    }
    return render(request, "engine_room/genset_engine2_form.html", context)


def tool_engine_update(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Tools, pk=pk)
    form = ToolsForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.serial_number,
        "instance": instance,
        "form": form,
    }
    return render(request, "engine_room/tool_form.html", context)


def engine_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Engines, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:engine_list")


def main_engine_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(MainEngine, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:mainengine_list")


def center_engine_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(CenterEngine, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:centerengine_list")


def port_engine_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(PortEngine, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:portengine_list")


def port_engine2_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(PortEngine2, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:portengine2_list")


def port_engine3_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(PortEngine3, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:portengine3_list")


def starboard_engine_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(StarboardEngine, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:starboard_list")


def starboard_engine2_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(StarboardEngine2, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:starboard2_list")


def starboard_engine3_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(StarboardEngine3, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:starboard3_list")


def auxiliary_engine_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Auxiliary, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:auxiliary_list")


def genset_engine_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(GenSet, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:genset_list")


def genset_engine2_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(GenSet2, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:genset2_list")


def tool_engine_delete(request, pk=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Tools, pk=pk)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("engine_room:tool_list")


class EnginePageNumberPagination(pagination.PageNumberPagination):
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


class EngineDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Engines.objects.all()
    serializer_class = EnginesSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class EngineListCreateAPIView(generics.ListCreateAPIView):
    queryset = Engines.objects.all()
    serializer_class = EnginesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = EnginePageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
