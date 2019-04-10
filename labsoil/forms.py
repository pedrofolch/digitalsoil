from django import forms
from pagedown.widgets import PagedownWidget

from .models import Lab


class LabForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)
    date_collected = forms.DateField(widget=forms.SelectDateWidget)
    date_observed = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Lab
        fields = [
            'user',
            'title',
            'sample_id',
            'pile_name',

            'collected_by',
            'date_collected',
            'date_observed',

            # number of drops per *1 ml of water is 10
            'coverlip_size',
            'number_of_drops_placed',

            'nematodes_bacterial_feeders',
            'nematodes_fungal_feeders',
            'nematodes_predatory',
            'nematodes_switchers',
            'nematodes_root_feeders',
            'nematodes_omnivores',
            'comments_nematodes',
            'nematodes_dilution',

            'ciliates',
            'ciliates_dilution',
            'flagellates',
            'flagellates_dilution',
            'amoeba',
            'amoeba_dilution',
            'oomycetes',
            'oomy_diameter',
            'oomy_color',
            'oomycetes_dilution',
            'fungi',
            'fungi_diameter',
            'fungi_color',
            'fungi_dilution',
            'actinobacteria',
            'actinobacteria_dilution',
            'bacteria',
            'bacteria_dilution',

            # aggregates
            'aggregates_humics',
            'comments_humics',

            'aggregates_fulvics',
            'comments_fulvics',

            'earthworms',
            'comments_earthworms',

            'insect_larvae',
            'comments_insect_larvae',

            'microarthropods',
            'comments_microarthropods',

            'rotifers',
            'comments_rotifers',

            'image',
            'content',
            'video_url',
            'read_time',

            'draft',
            'publish',

            'comments_general',
            'other_notes'
        ]
