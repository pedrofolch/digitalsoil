import requests
from django.contrib.auth.decorators import login_required
from datetime import timedelta, timezone, datetime
from iotsensor.models import Headline, UserProfile
from django.shortcuts import render
from posts.models import Post
from assets.models import TypeOfAsset
from recipes.models import Recipe
from providers.models import Supplier
from fieldwork.models import FieldData
from engine_room.models import Engines
from labsoil.models import Lab
from products.models import Product


@login_required
def home_news(request):
    # user_p = UserProfile.objects.filter(user=request.user).first()
    # now = datetime.now(timezone.utc)
    # time_difference = now - user_p.last_scrape
    # time_difference_in_hours = time_difference / timedelta(minutes=60)
    # next_scrape = 24 - time_difference_in_hours
    #
    # if time_difference_in_hours <= 24:
    #     hide_me = True
    # else:
    #     hide_me = False

    asset = TypeOfAsset.objects.filter(user=request.user)
    engine = Engines.objects.filter(user=request.user)
    provider = Supplier.objects.filter(user=request.user)
    product = Product.objects.filter(user=request.user)

    labsoil = Lab.objects.filter(user=request.user)
    recipe_compost = Recipe.objects.filter(user=request.user)

    field_data = FieldData.objects.filter(user=request.user)

    # seed = Seedling.objects.filter(user=request.user)

    # notes = Note.objects.filter(user=request.user)

    post = Post.objects.filter(user=request.user)

    # form = NoteModelForm(request.POST or None, request.FILES or None)

    # if form.is_valid():
    #     form.instance.user = request.user
    #     form.save()
    #     return redirect('/home_news/')

    context = {
        # 'form': form,
        # 'notes_list': notes,
        'object_list': labsoil,
        'engine_list': engine,
        'pile_list': recipe_compost,
        'field_data': field_data,
        # 'hide_me': hide_me,
        # 'next_scrape': math.ceil(next_scrape),
        # 'seed_list': seed,
        'post_list': post,
        'supplier_list': provider,
        'product_list': product,
        'asset_list': asset
    }

    return render(request, "news/webiot.html", context)
