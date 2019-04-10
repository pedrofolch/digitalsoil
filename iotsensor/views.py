import requests
import os
import shutil
import scrapy
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
from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from django.views.generic import DetailView
from iotsensor.api.serializers import SensorIoTSerializer
from comments.forms import CommentForm
from comments.models import Comment
from iotsensor.forms import SensorIoTForm
from iotsensor.models import SensorIoT
from .permissions import IsOwnerOrReadOnly
from analytics.models import View
from datetime import timezone, datetime
from bs4 import BeautifulSoup
from django.shortcuts import redirect
from .models import SensorIoT


from .models import Headline, UserProfile
requests.urllib3.disable_warnings()


def sensoriot_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    sensor = SensorIoT.objects.first()

    if user is not None:
        login(request, user)
        return redirect('/sensor/')
    else:
        return redirect('/login/')


def user_gains_perms(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.has_perm('iotsensor.sensoriot_create')

    content_type = ContentType.objects.get_for_model(SensorIoT)
    permission = Permission.objects.get(
        codename='sensoriot_create',
        content_type=content_type,
    )
    user.user_permissions.add(permission)

    user.has_perm('iotsensor.sensoriot_create')

    user = get_object_or_404(User, pk=user_id)

    user.has_perm('iotsensor.sensoriot_create')


def sensoriot_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = SensorIoTForm(request.POST or None, request.FILES or None)
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
    return render(request, "iotsensor/sensoriot_form.html", context)


def sensoriot_detail(request, slug=None):
    instance = get_object_or_404(SensorIoT, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
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
        except Exception as e:
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
    return render(request, "iotsensor/sensoriot_detail.html", context)


def sensoriot_list(request):
    today = datetime.now()
    queryset_list = SensorIoT.objects.active()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = SensorIoT.objects.all()

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
    return render(request, "iotsensor/sensoriot_list.html", context)


def sensoriot_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(SensorIoT, slug=slug)
    form = SensorIoTForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "iotsensor/sensoriot_form.html", context)


def sensoriot_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(SensorIoT, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("iotsensor:list")


class SensorIoTPageNumberPagination(pagination.PageNumberPagination):
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


class SensorIoTDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SensorIoT.objects.all()
    serializer_class = SensorIoTSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class SensorIoTDetailView(DetailView):
    model = SensorIoT

    def get_object_sensor(self, *kwargs):
        post_slug = self.kwargs.get("slug")  # grab the primary key of the object
        post_query = SensorIoT.objects.filter(slug=post_slug)  # returns a list with the filtered results

        if post_query.exists():
            post_object = post_query.first()  # grab the first item in the list if it exists
            view, created = View.objects.get_or_create(
                user=self.request.user,
                post=post_query,
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


class SensorIoTListCreateAPIView(generics.ListCreateAPIView):
    queryset = SensorIoT.objects.all()
    serializer_class = SensorIoTSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = SensorIoTPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def scrape(request):
    user_p = UserProfile.objects.filter(user=request.user).first()
    user_p.last_scrape = datetime.now(timezone.utc)
    print(user_p.last_scrape)
    user_p.save()

    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
    url = 'https://www.theonion.com/'  # target site, to be scraped
    content = session.get(url, verify=False).content

    soup = BeautifulSoup(content, "html.parser")

    posts = soup.find_all('div', {'class': 'curation-module__item'})  # exact location of what you want or article
    print(len(posts))

    for i in posts:
        link = i.find_all('a', {'class': 'js_curation-click'})[1]['href']
        title = i.find_all('a', {'class': 'js_curation-click'})[1].text
        image_source = i.find('img', {'class': 'featured-image'})['data-src']

        media_root = './live-static/media-root/images/news'
        if not image_source.startswith(("data:image", "javascript")):
            local_filename = image_source.split('/')[-1].split("?")[0]
            r = session.get(image_source, stream=True, verify=False)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)

            current_image_absolute_path = os.path.abspath(local_filename)
            shutil.move(current_image_absolute_path, media_root)

        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = local_filename
        new_headline.save()

    return redirect('/home_news/')


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://192.168.43.23/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
