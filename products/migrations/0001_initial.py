# Generated by Django 2.2 on 2019-04-10 00:07

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('AG', 'Agriculture'), ('M', 'Merchandise'), ('A', 'Asset'), ('S', 'service'), ('O', 'other'), ('B', 'bath & body'), ('AM', 'auto'), ('H', 'heavy equipment'), ('MA', 'marine'), ('AC', 'air')], default='B&B', max_length=2)),
                ('sub_category', models.CharField(blank=True, max_length=25, null=True)),
                ('title', models.CharField(help_text='name of the product', max_length=120)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('quantity', models.IntegerField(default=1)),
                ('pim', models.CharField(default='SRL099138', help_text='serial', max_length=20, verbose_name='product information management')),
                ('in_stock', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=products.models.upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('content', models.TextField()),
                ('draft', models.BooleanField(default=False)),
                ('publish', models.DateField()),
                ('read_time', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-publish', '-updated'],
            },
        ),
    ]
