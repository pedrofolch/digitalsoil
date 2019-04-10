try:
    from urllib.parse import quote_plus # python 3
except:
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import View, ListView, DetailView as DetailsView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from comments.forms import CommentForm
from comments.models import Comment
from recipes.forms import RecipeCreateForm
from recipes.models import Recipe
from django.http import JsonResponse


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


def recipes_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = RecipeCreateForm(request.POST or None, request.FILES or None)
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
    return render(request, "recipes/recipe_form.html", context)


class RecipeDetailView(LoginRequiredMixin, DetailsView):
    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)


class RecipeCreateView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    template_name = 'recipes/snippets/form-snippet.html'
    form_class = RecipeCreateForm
    success_url = "/recipes/"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(RecipeCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(RecipeCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Create pile of compost'
        return context


def recipe_detail(request, slug=None):
    instance = get_object_or_404(Recipe, slug=slug)
    if instance.publish > timezone.now() or instance.draft:
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
        "title": instance.recipe_name,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "recipes/recipe_detail.html", context)


class RecipeListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = Recipe.objects.filter(
                Q(pile_name__icontains=slug) |
                Q(content__icontains=slug) |
                Q(user__first_name__icontains=slug) |
                Q(user__last_name__icontains=slug)
            )
            return queryset
        else:
            return Recipe.objects.filter(user=self.request.user)


def recipe_list(request):
    today = timezone.now().date()
    queryset_list = Recipe.objects.all().order_by("-publish")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Recipe.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(producer__icontains=query) |
                Q(recipe_name__icontains=query) |
                Q(pile_name__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()

    paginator = Paginator(queryset_list, 4)  # Show 25 contacts per page
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
        "title": "Recipe List",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "recipes/recipe_list.html", context)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'recipes/detail-update.html'
    form_class = RecipeCreateForm

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(RecipeUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Pile of compost recipe'
        return context

    def get_form_kwargs(self):
        kwargs = super(RecipeUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# def recipe_update(request, slug=None):
#     if not request.user.is_staff or not request.user.is_superuser:
#         raise Http404
#     instance = get_object_or_404(Recipe, slug=slug)
#     form = RecipeCreateForm(request.POST or None, request.FILES or None, instance=instance)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.save()
#         messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
#         return HttpResponseRedirect(instance.get_absolute_url())
#
#     context = {
#         "title": instance.title,
#         "instance": instance,
#         "form": form,
#     }
#     return render(request, "recipes/recipe_form.html", context)


def recipe_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Recipe, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("recipes:list")


class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy


class AllUserRecentRecipeListView(ListView):
    template_name = 'recipes/home-feed.html'

    def get_queryset(self):
        return Recipe.objects.filter(user__is_active=True)
