# Generated by Django 2.2 on 2019-04-10 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import property.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shops', '0002_auto_20190330_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='ranch name', help_text='name of property', max_length=100)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=property.models.upload_property_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('content', models.TextField(verbose_name='description and condition')),
                ('publish', models.DateField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('draft', models.BooleanField(default=False)),
                ('acre', models.DecimalField(decimal_places=2, default=0, help_text='size of property', max_digits=10)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shops.Shop')),
            ],
        ),
        migrations.CreateModel(
            name='BuildingLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='name of the building', max_length=30, null=True)),
                ('slug', models.SlugField(blank=True, help_text='leave blank, or unique name', null=True, unique=True)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=property.models.upload_building_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('content', models.TextField(verbose_name='description and condition')),
                ('publish', models.DateField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('draft', models.BooleanField(default=False)),
                ('square_feet', models.IntegerField(help_text='building area')),
                ('on_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='property.Property')),
                ('user', models.ForeignKey(blank=True, help_text='person responsible for', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user', '-publish'],
            },
        ),
    ]
