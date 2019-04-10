# try:
#     from urllib.parse import quote_plus # python 3
# except:
#     pass
from django.shortcuts import render, redirect  # , get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
# from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from profiles.models import Profile
from maintenance.models import ServiceSchedule
from maintenance.forms import ServiceScheduleForm
from assets.models import TypeOfAsset
from engine_room.models import Engines


def schedules(request):

    user_s = Profile.objects.filter(user=request.user).first()
    service = ServiceSchedule.objects.all()
    engine = Engines.objects.all()
    # operator = OperatorOfTheAsset.objects.all()
    vehicle = TypeOfAsset.objects.all()

    form = ServiceScheduleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return redirect('/')

    context = {
        'form': form,
        'user_list': user_s,
        'service_list': service,
        'engine_list': engine,
        # 'operator_list': operator,
        'vehicle_list': vehicle,
    }

    return render(request, 'maintenance/schedule.html', context)


def schedule_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = ServiceScheduleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolut_url())


# def schedule_detail(request, pk=None):
#     if not request.user.is_staff or not request.user.is_superuser:
#         raise Http404
#     instance = get_object_or_404(VehicleDescription, pk=pk)
#     share_string = quote_plus(instance.content)
#
#     initial_data = {
#         "content_type": instance.get_content_type,
#         "object_id": instance.id
#     }
#     form = MaintenanceScheduleForm(request.POST or None, initial=initial_data)
#     if form.is_valid() and request.user.is_authenticated:
#         c_type = form.cleaned_data.get('content_type')
#         content_type = ContentType.objects.get(model=c_type)
#         obj_id = form.cleaned_data.get('object_id')
#         content_data = form.cleaned_data.get('content')
#         parent_obj = None
#         try:
#             parent_id = int(request.POST.get("parent_id"))
#         except:
#             parent_id = None
#
#         if parent_id:
#             parent_qs = MaintenanceScheduleForm.objects.filter(id=parent_id)
#             if parent_qs.exists() and parent_qs.count() == 1:
#                 parent_obj = parent_qs.first()
#
#         new_schedule, created = MaintenanceScheduleForm.objects.get_or_create(
#             user=request.user,
#             content_type=content_type,
#             object_id=obj_id,
#             content=content_data,
#             parent=parent_obj,
#         )
#         return HttpResponseRedirect(new_schedule.content_object.get_absolute_url())
#
#     schedule = instance.schedule
#     context = {
#         "owner": instance.owner,
#         "make": instance.make,
#         "model": instance.model,
#         "year": instance.year,
#         "image": instance.image,
#         "color": instance.color,
#         "vin": instance.vin,
#         "Tag": instance.license_plate,
#         "mileage": instance.mileage,
#         "fuel_capacity": instance.fuel_capacity,
#         "share_string": share_string,
#         'schedule': schedule,
#         'schedule_form': form
#     }
#     return render(request, "maintenance/schedule_detail.html", context)


def schedule_list(request):
    today = timezone.now().date()
    queryset_list = ServiceSchedule.objects.all()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = ServiceSchedule.objects.all()

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
        "title": "List",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "maintenance/schedule_list.html", context)
