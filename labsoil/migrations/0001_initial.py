# Generated by Django 2.2 on 2019-04-10 00:07

import django.core.validators
from django.db import migrations, models
import labsoil.models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Bio-Assesment', max_length=120)),
                ('slug', models.SlugField(blank=True, help_text='leave blank or your-brand-name', null=True, unique=True)),
                ('sample_id', models.CharField(max_length=60)),
                ('collected_by', models.CharField(max_length=120)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('date_collected', models.DateField(help_text='yyyy/mm/dd')),
                ('date_observed', models.DateField(blank=True, help_text='yyyy/mm/dd')),
                ('coverlip_size', models.CharField(choices=[('2038', '18 x 18'), ('2491', '22 x 18'), ('3044', '22 x 22')], default='2038', max_length=120)),
                ('number_of_drops_placed', models.DecimalField(decimal_places=0, default=2, max_digits=8)),
                ('drops_per_ml', models.DecimalField(decimal_places=3, default=0.0, max_digits=8)),
                ('nematodes_bacterial_feeders', models.PositiveIntegerField(default=0)),
                ('nematodes_fungal_feeders', models.PositiveIntegerField(default=0)),
                ('nematodes_predatory', models.PositiveIntegerField(default=0)),
                ('nematodes_switchers', models.PositiveIntegerField(default=0)),
                ('nematodes_root_feeders', models.PositiveIntegerField(default=0)),
                ('nematodes_omnivores', models.PositiveIntegerField(default=0)),
                ('total_nematodes', models.PositiveIntegerField(default=0)),
                ('total_beneficial', models.PositiveIntegerField(default=0)),
                ('total_detrimentals', models.PositiveIntegerField(default=0)),
                ('nematodes_total_num_p_gram', models.DecimalField(decimal_places=3, default=0.0, max_digits=8)),
                ('nematodes_dilution', models.DecimalField(decimal_places=3, default=5, help_text='in multiple of 5, up to 2000', max_digits=8)),
                ('nematodes_expected_range', models.CharField(choices=[('UN', 'unknown'), ('3-3', '300 - 3000'), ('3-12', '3 - 12'), ('1-200', '100 - 2000')], default='1-200', max_length=5)),
                ('comments_nematodes', models.TextField(blank=True, verbose_name='comments on nematodes')),
                ('ciliates', models.CharField(blank=True, help_text='comma separated, no white space', max_length=300, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('ciliates_mean', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('flagellates', models.CharField(blank=True, help_text='comma separated, no white space', max_length=300, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('flagellates_mean', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('amoeba', models.CharField(blank=True, help_text='comma separated, no white space', max_length=300, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('amoeba_mean', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('oomycetes', models.CharField(blank=True, help_text='comma separated', max_length=300, null=True)),
                ('oomycetes_mean', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('oomy_diameter', models.CharField(blank=True, default=0, help_text='comma separated', max_length=300)),
                ('oomy_diameter_mean', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('oomy_color', models.CharField(default='none', max_length=380)),
                ('fungi', models.CharField(blank=True, help_text='comma separated', max_length=380, null=True)),
                ('fungi_mean', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('fungi_diameter', models.CharField(blank=True, default=0, help_text='comma separated', max_length=300)),
                ('fungi_diameter_mean', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('fungi_color', models.CharField(default='none', max_length=380)),
                ('actinobacteria', models.CharField(blank=True, help_text='comma separated', max_length=300, null=True)),
                ('actinobacteria_mean', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('bacteria', models.CharField(blank=True, help_text='comma separated', max_length=300, null=True)),
                ('bacteria_mean', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('ciliates_total_mg_per_g', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('ciliates_dilution', models.DecimalField(decimal_places=0, default=5, help_text='integers of 5', max_digits=9)),
                ('comments_ciliates', models.TextField(blank=True, verbose_name='comments')),
                ('ciliates_expected_range', models.CharField(choices=[('UN', 'unknown'), ('3-3', '300 - 3000'), ('3-12', '3 - 12'), ('1-200', '100 - 2000')], default='3-3', max_length=5)),
                ('ciliates_st_diviation', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('actinobacteria_total_mg_per_g', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('actinobacteria_dilution', models.PositiveIntegerField(default=5)),
                ('comments_actinobacteria', models.TextField(blank=True, verbose_name='comments')),
                ('actinobacteria_expected_range', models.CharField(choices=[('UN', 'unknown'), ('3-3', '300 - 3000'), ('3-12', '3 - 12'), ('1-200', '100 - 2000')], default='3-3', max_length=5)),
                ('actinobacteria_st_diviation', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('oomycetes_total_mg_per_g', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('oomycetes_dilution', models.PositiveIntegerField(default=5)),
                ('comments_oomycetes', models.TextField(blank=True, verbose_name='comments')),
                ('oomycetes_expected_range', models.CharField(choices=[('UN', 'unknown'), ('3-3', '300 - 3000'), ('3-12', '3 - 12'), ('1-200', '100 - 2000')], default='3-3', max_length=5)),
                ('oomycetes_st_diviation', models.DecimalField(decimal_places=3, default=0.0, max_digits=7)),
                ('fungi_total_mg_per_g', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('fungi_dilution', models.PositiveIntegerField(default=5)),
                ('comments_fungi', models.TextField(blank=True, verbose_name='comments')),
                ('fungi_expected_range', models.CharField(choices=[('UN', 'unknown'), ('3-3', '300 - 3000'), ('3-12', '3 - 12'), ('1-200', '100 - 2000')], default='3-3', max_length=5)),
                ('fungi_st_diviation', models.DecimalField(decimal_places=3, default=0.0, max_digits=7)),
                ('de_av_hyphal_dia', models.DecimalField(decimal_places=3, default=0.0, max_digits=6)),
                ('comments_de_av_hyphal_dia', models.TextField(blank=True)),
                ('de_av_hyphal_dia_expected_range', models.CharField(choices=[('UN', 'unknown'), ('3-3', '300 - 3000'), ('3-12', '3 - 12'), ('1-200', '100 - 2000')], default='3-12', max_length=5)),
                ('de_av_hyphal_dia_mean', models.DecimalField(decimal_places=3, default=0.0, max_digits=6)),
                ('bacteria_total_mg_per_g', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('bacteria_dilution', models.PositiveIntegerField(default=5)),
                ('bacteria_expected_range', models.CharField(choices=[('UN', 'unknown'), ('3-3', '300 - 3000'), ('3-12', '3 - 12'), ('1-200', '100 - 2000')], default='3-3', max_length=5)),
                ('bacteria_st_diviation', models.DecimalField(decimal_places=3, default=0.0, max_digits=7)),
                ('comments_bacteria', models.TextField(blank=True, verbose_name='comments')),
                ('bn_av_hyphal_dia', models.DecimalField(decimal_places=3, default=0.0, max_digits=6)),
                ('comments_bn_av_hyphal_dia', models.TextField(blank=True)),
                ('bn_av_hyphal_dia_expected_range', models.CharField(choices=[('UN', 'unknown'), ('3-3', '300 - 3000'), ('3-12', '3 - 12'), ('1-200', '100 - 2000')], default='3-12', max_length=5)),
                ('bn_av_hyphal_dia_mean', models.DecimalField(decimal_places=3, default=0.0, max_digits=6)),
                ('flagellates_total_mg_per_g', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('flagellates_dilution', models.PositiveIntegerField(default=5)),
                ('comments_flagellates', models.TextField(blank=True, verbose_name='comments')),
                ('flagellates_expected_range', models.CharField(choices=[('UN', 'unknown'), ('3-3', '300 - 3000'), ('3-12', '3 - 12'), ('1-200', '100 - 2000')], default='3-3', max_length=5)),
                ('flagellates_st_diviation', models.DecimalField(decimal_places=3, default=0.0, max_digits=7)),
                ('amoeba_total_mg_per_g', models.DecimalField(decimal_places=3, default=0.0, max_digits=9)),
                ('amoeba_dilution', models.PositiveIntegerField(default=5)),
                ('comments_amoeba', models.TextField(blank=True, verbose_name='comments')),
                ('amoeba_expected_range', models.CharField(choices=[('UN', 'unknown'), ('3-3', '300 - 3000'), ('3-12', '3 - 12'), ('1-200', '100 - 2000')], default='3-3', max_length=5)),
                ('amoeba_st_diviation', models.DecimalField(decimal_places=3, default=0.0, max_digits=7)),
                ('cocci', models.BooleanField(default=False)),
                ('cocci_chains', models.BooleanField(default=False)),
                ('bacillus', models.BooleanField(default=False)),
                ('bacili_chains', models.BooleanField(default=False)),
                ('cocobacili', models.BooleanField(default=False)),
                ('spirochetes', models.BooleanField(default=False)),
                ('spirilla', models.BooleanField(default=False)),
                ('comments_hyphal', models.TextField(blank=True, verbose_name='hyphal comments')),
                ('aggregates_humics', models.TextField(blank=True)),
                ('comments_humics', models.TextField(blank=True, verbose_name='humics comments')),
                ('aggregates_fulvics', models.TextField(blank=True)),
                ('comments_fulvics', models.TextField(blank=True, verbose_name='fulvics comments')),
                ('earthworms', models.CharField(choices=[('D', 'dead'), ('A', 'alive'), ('UN', 'unknown')], default='UN', max_length=2)),
                ('comments_earthworms', models.TextField(blank=True, verbose_name='earthworms comments')),
                ('insect_larvae', models.CharField(choices=[('D', 'dead'), ('A', 'alive'), ('UN', 'unknown')], default='UN', max_length=2)),
                ('comments_insect_larvae', models.TextField(blank=True, verbose_name='insect larvae comments')),
                ('microarthropods', models.CharField(choices=[('D', 'dead'), ('A', 'alive'), ('UN', 'unknown')], default='UN', max_length=2)),
                ('comments_microarthropods', models.TextField(blank=True, verbose_name='microarthropods comments')),
                ('rotifers', models.CharField(choices=[('D', 'dead'), ('A', 'alive'), ('UN', 'unknown')], default='UN', max_length=2)),
                ('comments_rotifers', models.TextField(blank=True, verbose_name='rotifer comments')),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=labsoil.models.upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('content', models.TextField(blank=True)),
                ('read_time', models.IntegerField(default=0)),
                ('video_url', models.CharField(max_length=200)),
                ('draft', models.BooleanField(default=False)),
                ('publish', models.DateField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('comments_general', models.TextField(blank=True, verbose_name='comments')),
                ('other_notes', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['-timestamp', '-updated'],
            },
        ),
    ]
