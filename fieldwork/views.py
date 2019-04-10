try:
    from urllib.parse import quote_plus  # python 3
except Exception as e:
    pass

import numpy as np
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from fieldwork.forms import FieldDataForm
from fieldwork.models import FieldData
from .utils import AjaxFormMixin
from analytics.models import View
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from comments.forms import CommentForm
from comments.models import Comment
from django.db.models import Min, Max


class AllUserRecentFieldWorkListView(ListView):
    template_name = 'fieldwork/field-data.html'

    def get_queryset(self):
        return FieldData.objects.filter(user__is_active=True)


class FieldWorkListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return FieldData.objects.filter(user=self.request.user)


class FieldWorkView(View):
    def __get__(self, request):
        if not request.user.is_authenticated:
            object_list = FieldData.objects.filter(user__is_active=True).order_by('-timestamp')

            return render(request, "fieldwork/fieldwork_list.html", {"object_list": object_list})

        user = request.user
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        qs = FieldData.objects.filter(user__id__in=is_following_user_ids, public=True).order_by("-updated")[:3]
        return render(request, "fieldwork/home-feed.html", {'object_list': qs})


def fieldwork_detail(request, slug=None):
    instance = get_object_or_404(FieldData, slug=slug)
    if instance.publish > timezone.now().date():
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
    return render(request, "fieldwork/fieldwork_detail.html", context)


class FieldWorkDetailView(LoginRequiredMixin, DetailView):
    template_name = 'fieldwork/fieldwork_detail.html'
    form_class = FieldDataForm
    model = FieldData

    def get_queryset_metric(self):
        post_slug = self.kwargs.get('slug')
        post_query = FieldData.objects.filter(slug=post_slug)
        if post_query:
            post_object = post_query.first()
            view, created = View.objects.get_or_create(
                user=self.request.user,
                post=post_object
            )
            if view:
                view.views_count += 1
                view.save()
                return post_object
        return Http404


def field_work_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = FieldDataForm(request.POST or None, request.FILES or None)
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
    return render(request, "fieldwork/snippets/form-snippet.html", context)


def fieldwork_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(FieldData, slug=slug)
    form = FieldDataForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='{% urls 'fieldwork:average' %}>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "fieldwork/snippets/form-snippet.html", context)


class FieldWorkCreateView(LoginRequiredMixin, AjaxFormMixin, CreateView):
    template_name = 'snippets/form-snippet.html'
    form_class = FieldDataForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(FieldWorkCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(FieldWorkCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return FieldData.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(FieldWorkCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Fieldwork'
        return context


class FieldWorkUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'fieldwork/detail-update.html'
    form_class = FieldDataForm

    def get_queryset(self):
        return FieldData.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(FieldWorkUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Pile Data'
        return context

    def get_form_kwargs(self):
        kwargs = super(FieldWorkUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


def fieldwork_average(request, slug):
    # Averages gathered in the field as a list(array).
    temperature = get_object_or_404(FieldData, slug=slug)
    qs = temperature
    qs.days = int(qs.days)
    # temperature
    ft = qs.core_temperature_readings
    array_ft = ft.split(',')
    ft_np = np.array(array_ft)
    numpy_ft = np.array(ft_np, int)
    qs.average_temperature = np.average(numpy_ft)

    if 70 <= qs.average_temperature and qs.days >= 7:
        qs.is_pile_ready = True
        print(qs.is_pile_ready)

    elif 131 >= qs.average_temperature <= 140 and qs.days >= 3:
        qs.must_turn_pile = True
        print(qs.average_temperature, qs.must_turn_pile)

    elif 141 >= qs.average_temperature <= 150 and qs.days >= 2:
        qs.must_turn_pile = True
        print(qs.average_temperature, qs.must_turn_pile)

    elif 151 >= qs.average_temperature <= 160 and qs.days >= 1:
        qs.must_turn_pile = True
        print(qs.average_temperature, qs.must_turn_pile)

    elif qs.average_temperature >= 161:
        qs.must_turn_pile = True
        print(qs.average_temperature, qs.must_turn_pile)

    # humidity
    fh = qs.core_humidity_readings
    array_fh = fh.split(',')
    fh_np = np.array(array_fh)
    numpy_fh = np.array(fh_np, int)
    qs.average_humidity = np.average(numpy_fh)
    if qs.average_humidity < 45:
        qs.must_water_now = True
        qs.save()
        print(qs.must_water_now)

    print(qs.average_temperature)
    print(qs.average_humidity)
    print(qs.is_pile_ready)
    print(qs.must_turn_pile)
    print(qs.days)
    bell_temp = FieldData.objects.aggregate(Max('average_temperature'), Min('average_temperature'))
    qs.bell_temperature = bell_temp
    print(qs.bell_temperature)
    bell_humid = FieldData.objects.aggregate(Max('average_humidity'), Min('average_humidity'))
    qs.bell_humid = bell_humid
    print(bell_humid)
    qs.save()
    context = {
        "title": qs.title,
        "instance": qs,
    }
    if qs.turned:
        qs.days = 0
        qs.turn_cycle += 1
        qs.save()
        print(qs.days)
        print(qs.turn_cycle)
    else:
        qs.days += 1
        qs.save()

    return render(request, "fieldwork/fieldwork_average_detail.html", context)
