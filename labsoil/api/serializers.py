from rest_framework import serializers

from labsoil.models import Lab


class LabPostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Lab
        fields = [
            'pk',
            'url',
            'user',
            'title',
            'pile_name',

            'collected_by',
            'date_collected',
            'date_observed',

            # number of drops per *1 ml of water is 10
            'coverlip_size',
            'number_of_drops_placed',
            'drops_per_ml',

            'nematodes_bacterial_feeders',
            'nematodes_fungal_feeders',
            'nematodes_predatory',
            'nematodes_switchers',
            'nematodes_root_feeders',
            'nematodes_omnivores',
            'comments_nematodes',
            'nematodes_dilution',
            'total_nematodes',
            'total_beneficial',
            'total_detrimentals',

            'ciliates',
            'ciliates_mean',
            'ciliates_st_diviation',
            'ciliates_dilution',

            'flagellates',
            'flagellates_mean',
            'flagellates_st_diviation',
            'flagellates_dilution',

            'amoeba',
            'amoeba_mean',
            'amoeba_st_diviation',
            'amoeba_dilution',

            'oomycetes',
            'oomycetes_mean',
            'oomycetes_st_diviation',
            'oomycetes_dilution',

            'oomy_diameter',
            'oomy_diameter_mean',
            'oomycetes_st_diviation',
            'oomy_color',
            'oomycetes_dilution',

            'fungi',
            'fungi_mean',
            'fungi_st_diviation',
            'fungi_diameter',
            'fungi_diameter_mean',
            'fungi_color',
            'fungi_dilution',

            'actinobacteria',
            'actinobacteria_mean',
            'actinobacteria_st_diviation',
            'actinobacteria_dilution',

            'bacteria',
            'bacteria_mean',
            'bacteria_st_diviation',
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
        read_only_fields = ['user']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    # def validate_sample_id(self, value):
    #     """We want the title to be unique"""
    #     qs = Lab.objects.filter(sample_id__iexact=value)  # including instance
    #     if self.instance:
    #         qs = qs.exclude(pk=self.instance.pk)
    #         if qs.exists():
    #             raise serializers.ValidationError("This sample id has already been used")
    #     return value
