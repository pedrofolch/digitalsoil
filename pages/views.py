from django.views.generic import CreateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin

from newsletter.forms import SignUpForm
from .models import Page

# Create your views here.


class HomeView(SuccessMessageMixin, CreateView):
    template_name = 'pages/digitalsoil.html'
    form_class = SignUpForm
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data( **kwargs)
        context['page_obj'] = Page.objects.all().first()
        # Page.objects.all().order_by("?").first()  # will order page randomly
        return context

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return "Thank you for joining!"


class PageDetailView(DetailView):
    queryset = Page.objects.filter(active=True)
    model = Page
    template_name = 'pages/digitalsoil.html'
