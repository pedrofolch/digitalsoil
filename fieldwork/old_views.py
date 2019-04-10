import numpy as np
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from django.db.models import Q
from django.http import JsonResponse

from fieldwork.forms import FieldWorkCreateForm
from fieldwork.models import FieldWork


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class AllUserRecentFieldWorkListView(ListView):
    template_name = 'fieldwork/list.html'

    def get_queryset(self):
        return FieldWork.objects.filter(user__is_active=True)


class FieldWorkListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return FieldWork.objects.filter(user=self.request.user)


class FieldWorkView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            object_list = FieldWork.objects.filter(public=True).order_by('-timestamp')
            return render(request, "folch2iot.html", {"object_list": object_list})

        user = request.user
        is_following_user_ids = [x.user.id for x in user.is_following.all()]
        qs = FieldWork.objects.filter(user__id__in=is_following_user_ids, public=True).order_by("-updated")[:3]
        return render(request, "home-feed.html", {'object_list': qs})


class FieldWorkDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):
        return FieldWork.objects.filter(user=self.request.user)


class FieldWorkCreateView(LoginRequiredMixin, CreateView):
    template_name = 'snippets/form-snippet.html'
    form_class = FieldWorkCreateForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(FieldWorkCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(FieldWorkCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return FieldWork.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(FieldWorkCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Field work data'
        return context


class FieldWorkUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'fieldwork/detail-update.html'
    form_class = FieldWorkCreateForm

    def get_queryset(self):
        return FieldWork.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(FieldWorkUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Update Pile Data'
        return context

    def get_form_kwargs(self):
        kwargs = super(FieldWorkUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
