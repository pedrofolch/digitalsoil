try:
    from urllib.parse import quote_plus  # python 3
except:
    pass

import numpy as np
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from labsoil.forms import LabForm
from labsoil.models import Lab


def labsoil_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = LabForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "LabSoil",
        "form": form,
    }
    return render(request, "labsoil/snippets/form-snippet.html", context)


def labsoil_detail(request, slug=None):
    instance = get_object_or_404(Lab, slug=slug)
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
    return render(request, "labsoil/lab_detail.html", context)


def labsoil_list(request):
    today = timezone.now().date()
    queryset_list = Lab.objects.all()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Lab.objects.all()

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
        "title": "LabSoil List",
        "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "labsoil/lab_list.html", context)


def labsoil_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Lab, slug=slug)
    form = LabForm(request.POST or None, request.FILES or None, instance=instance)
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
    return render(request, "labsoil/snippets/form-snippet.html", context)


def labsoil_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Lab, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("labsoil:delete")


def lab_soil_result(request, slug):  # Gather Data from Lab file and create a list.
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    lab_file = get_object_or_404(Lab, slug=slug)
    qs = lab_file
    drop = 20.00
    drops_placed = qs.number_of_drops_placed
    cover_clip = qs.coverlip_size
    size_selected = float(cover_clip)
    dilution_ciliates = qs.ciliates_dilution
    dilution_flagellates = qs.flagellates_dilution
    dilution_amoeba = qs.amoeba_dilution
    dilution_oomycetes = qs.oomycetes_dilution
    dilution_fungi = qs.fungi_dilution
    dilution_actinobacteria = qs.actinobacteria_dilution
    dilution_bacteria = qs.bacteria_dilution
    nematodes_dilution = qs.nematodes_dilution
    ciliates_dilution = dilution_ciliates
    flagellates_dilution = dilution_flagellates
    amoeba_dilution = dilution_amoeba
    oomycetes_dilution = dilution_oomycetes
    fungi_dilution = dilution_fungi
    actinobacteria_dilution = dilution_actinobacteria
    bacteria_dilution = dilution_bacteria
    switchers = qs.nematodes_switchers
    root_feeders = qs.nematodes_root_feeders
    omnivores = qs.nematodes_omnivores
    ciliates = qs.ciliates
    flagellates = qs.flagellates
    amoeba = qs.amoeba
    oomycetes = qs.oomycetes
    fungi = qs.fungi
    actinobacteria = qs.actinobacteria
    bacteria = qs.bacteria
    bacterial_feeders = qs.nematodes_bacterial_feeders
    fungal_feeders = qs.nematodes_fungal_feeders
    predatory = qs.nematodes_predatory
    total_nematodes = bacterial_feeders + fungal_feeders + predatory + switchers + root_feeders + omnivores
    nematodes_total_num_p_gram = float(total_nematodes * nematodes_dilution) * 20
    total_beneficial = bacterial_feeders + fungal_feeders + predatory + omnivores
    total_detrimentals = switchers + root_feeders
    qs.total_beneficial = total_beneficial
    qs.total_detrimentals = total_detrimentals
    qs.total_nematodes = total_nematodes
    qs.nematodes_total_num_p_gram = nematodes_total_num_p_gram

    ci = ciliates
    fu = fungi
    fl = flagellates
    ao = amoeba
    oo = oomycetes
    act = actinobacteria
    bac = bacteria

    drops_per_ml = int(20 / int(float(drops_placed)))

    if ci != 0:
        array_ci = ci.split(',')
        ci_np = np.array(array_ci)
        numpy_ci = np.array(ci_np, float)
        ciliates_mean = np.average(numpy_ci)
        ciliates_st_diviation = np.std(numpy_ci)
        ciliates_total_mg_per_g = float(float(ciliates_mean) * float(ciliates_dilution)) * float(drops_per_ml) * float(size_selected)

        qs.ciliates_mean = float(ciliates_mean)
        qs.ciliates_st_diviation = float(ciliates_st_diviation)
        qs.ciliates_total_mg_per_g = float(ciliates_total_mg_per_g)
        qs.drops_per_ml = float(drops_per_ml)

        array_fu = fu.split(',')
        fu_np = np.array(array_fu)
        numpy_fu = np.array(fu_np, float)
        fungi_mean = np.average(numpy_fu)
        fungi_st_diviation = np.std(numpy_fu)

        total_fungi_mg_per_g = float(fungi_mean) * float(fungi_dilution)
        total_mg_per_g = total_fungi_mg_per_g
        fungi_total_mg_per_g = float(total_mg_per_g) * float(drops_per_ml) * float(size_selected)

        fungi_dia = qs.fungi_diameter
        array_fungi_dia = fungi_dia.split(',')
        fungi_dia_np = np.array(array_fungi_dia)
        numpy_fungi_dia = np.array(fungi_dia_np, float)
        fungi_diameter_mean = np.average(numpy_fungi_dia)

        qs.fungi_mean = float(fungi_mean)
        qs.fungi_st_diviation = float(fungi_st_diviation)
        qs.fungi_total_mg_per_g = float(fungi_total_mg_per_g)
        qs.fungi_diameter_mean = float(fungi_diameter_mean)

        array_fl = fl.split(',')
        fl_np = np.array(array_fl)
        numpy_fl = np.array(fl_np, float)
        flagellates_mean = np.average(numpy_fl)
        flagellates_st_diviation = np.std(numpy_fl)

        total_flagellates_mg_per_g = float(flagellates_mean) * float(flagellates_dilution)
        total_mg_per_g = total_flagellates_mg_per_g
        flagellates_total_mg_per_g = float(total_mg_per_g) * float(drops_per_ml) * float(size_selected)

        qs.flagellates_mean = float(flagellates_mean)
        qs.flagellates_st_diviation = float(flagellates_st_diviation)
        qs.flagellates_total_mg_per_g = float(flagellates_total_mg_per_g)

        array_ao = ao.split(',')
        ao_np = np.array(array_ao)
        numpy_ao = np.array(ao_np, float)
        amoeba_mean = np.average(numpy_ao)
        amoeba_st_diviation = np.std(numpy_ao)

        total_amoeba_mg_per_g = float(amoeba_mean) * float(amoeba_dilution)
        total_mg_per_g = total_amoeba_mg_per_g
        amoeba_total_mg_per_g = float(total_mg_per_g) * float(drops_per_ml) * float(size_selected)

        qs.amoeba_mean = float(amoeba_mean)
        qs.amoeba_st_diviation = float(amoeba_st_diviation)
        qs.amoeba_total_mg_per_g = float(amoeba_total_mg_per_g)

        array_oo = oo.split(',')
        oo_np = np.array(array_oo)
        numpy_oo = np.array(oo_np, float)
        oomycetes_mean = np.average(numpy_oo)
        oomycetes_st_diviation = np.std(numpy_oo)

        total_oomycetes_mg_per_g = float(oomycetes_mean) * float(oomycetes_dilution)
        total_mg_per_g = total_oomycetes_mg_per_g
        oomycetes_total_mg_per_g = float(total_mg_per_g) * float(drops_per_ml) * float(size_selected)

        oomy_dia = qs.oomy_diameter
        array_oomy_dia = oomy_dia.split(',')
        oomy_dia_np = np.array(array_oomy_dia)
        numpy_oomy_dia = np.array(oomy_dia_np, float)
        oomy_diameter_mean = np.average(numpy_oomy_dia)


        qs.oomycetes_mean = float(oomycetes_mean)
        qs.oomycetes_st_diviation = float(oomycetes_st_diviation)
        qs.oomycetes_total_mg_per_g = float(oomycetes_total_mg_per_g)
        qs.oomy_diameter_mean = float(oomy_diameter_mean)

        array_act = act.split(',')
        act_np = np.array(array_act)
        numpy_act = np.array(act_np, float)
        actinobacteria_mean = np.average(numpy_act)
        actinobacteria_st_diviation = np.std(numpy_act)

        total_actinobacteria_mg_per_g = float(actinobacteria_mean) * float(actinobacteria_dilution)
        total_mg_per_g = total_actinobacteria_mg_per_g
        actinobacteria_total_mg_per_g = float(total_mg_per_g) * float(drops_per_ml) * float(size_selected)

        qs.actinobacteria_mean = float(actinobacteria_mean)
        qs.actinobacteria_st_diviation = float(actinobacteria_st_diviation)
        qs.actinobacteria_total_mg_per_g = float(actinobacteria_total_mg_per_g)

        array_bac = bac.split(',')
        bac_np = np.array(array_bac)
        numpy_bac = np.array(bac_np, float)
        bacteria_mean = np.average(numpy_bac)
        bacteria_st_diviation = np.std(numpy_bac)

        total_bacteria_mg_per_g = float(bacteria_mean) * float(bacteria_dilution)
        total_mg_per_g = total_bacteria_mg_per_g
        bacteria_total_mg_per_g = float(total_mg_per_g) * float(drops_per_ml) * float(size_selected)

        qs.bacteria_mean = float(bacteria_mean)
        qs.bacteria_st_diviation = float(bacteria_st_diviation)
        qs.bacteria_total_mg_per_g = float(bacteria_total_mg_per_g)

    context = {
        "title": qs.sample_id,
        "instance": qs,
    }
    return render(request, "labsoil/lab_detail.html", context)




    # elif bac != 0:
    #     array_bac = bac.split(',')
    #     bac_np = np.array(array_bac)
    #     numpy_bac = np.array(bac_np, float)
    #     bacteria_mean = np.average(numpy_bac)
    #     bacteria_st_diviation = np.std(numpy_bac)
    #
    #     total_bacteria_mg_per_g = float(bacteria_mean) * float(bacteria_dilution)
    #     total_mg_per_g = total_bacteria_mg_per_g * size_selected
    #     bacteria_total_mg_per_g = float(total_mg_per_g) * float(drops_per_ml) * float(size_selected)
    #
    #     qs.bacteria_mean = float(bacteria_mean)
    #     qs.bacteria_st_diviation = float(bacteria_st_diviation)
    #     qs.bacteria_total_mg_per_g = float(bacteria_total_mg_per_g)
    #     qs.save()
    # else:
    #     qs.save()
