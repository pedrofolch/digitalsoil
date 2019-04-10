from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from shopping_cart.models import Order
from .models import Profile
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, View
from accounts.forms import RegisterForm

from products.models import Product
from posts.models import Post


User = get_user_model()


def my_profile(request):
    my_user_profile = Profile.objects.filter(user=request.user).first()
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    context = {
        'my_orders': my_orders
    }

    return render(request, "profile.html", context)


def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated = True
                profile.activation_key = None
                profile.save()
        return redirect("/login/")


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'
    success_message = "Your account was created successfully. Please check your email."

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("/logout")
        return super(RegisterView, self).dispatch(*args, **kwargs)


class ProfileFollowToggle(LoginRequiredMixin, View):
    def profile(self, request):
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)
        return redirect(f"/u/{profile_.user.username}/")


class RandomProfileDetailView(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self, *args):
        return User.objects.filter(is_active=True, item__isnull=False).order_by("?").first()  # / gives a random item.

    def get_context_data(self, *args, **kwargs):
        context = super(RandomProfileDetailView, self).get_context_data(**kwargs)
        user = context['user']
        is_following = False
        if self.request.user.is_authenticated:
            if user.profile in self.request.user.is_following.all():
                is_following = True
        context['is_following'] = is_following
        query = self.request.GET.get('q')
        items_exists = Product.objects.filter(user=user).exists()
        qs = Post.objects.filter(user=user).search(query)
        if items_exists and qs.exists():
            context['locations'] = qs
        return context


class ProfileDetailView(DetailView):
    template_name = 'profiles/user.html'

    def get_object(self, *args):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        user = context['user']
        is_following = False
        if self.request.user.is_authenticated:
            if user.profile in self.request.user.is_following.all():
                is_following = True
        context['is_following'] = is_following
        query = self.request.GET.get('q')
        items_exists = Product.objects.filter(user=user).exists()
        qs = Post.objects.filter(user=user).search(query)
        if items_exists and qs.exists():
            context['locations'] = qs
        return context
