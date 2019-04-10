# Generated by Django 2.2 on 2019-04-10 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import repairs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personnel', '0001_initial'),
        ('providers', '0001_initial'),
        ('engine_room', '0002_auto_20190409_1707'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0002_auto_20190409_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepairOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='main problem', max_length=250)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('purchase_order', models.BooleanField(default=False)),
                ('estimate', models.BooleanField(default=False)),
                ('po_number', models.CharField(default='0001', max_length=25, unique=True)),
                ('problem_found', models.TextField()),
                ('publish', models.DateTimeField(auto_now_add=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('approved', models.BooleanField(default=False)),
                ('approved_by', models.CharField(default='myself', max_length=25)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='providers.Supplier')),
                ('on_asset', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.TypeOfAsset')),
                ('preferred_engineer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='personnel.Engineer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp', '-publish'],
            },
        ),
        migrations.CreateModel(
            name='RepairFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Name of Task or Repair')),
                ('slug', models.SlugField(blank=True, help_text='leave blank or your-brand-name', null=True, unique=True)),
                ('date_of_invoice', models.DateTimeField(blank=True, null=True)),
                ('estimate_number', models.CharField(blank=True, max_length=15, null=True)),
                ('quoted_price', models.CharField(blank=True, max_length=5, null=True)),
                ('invoice_number', models.CharField(blank=True, max_length=10, null=True)),
                ('work_order', models.CharField(blank=True, help_text='work order number', max_length=10, null=True)),
                ('odometer', models.DecimalField(decimal_places=2, default=0.0, help_text='odometer actual reading', max_digits=9)),
                ('tax_id', models.CharField(blank=True, max_length=20, null=True)),
                ('return_parts', models.BooleanField(default=False)),
                ('due_price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('price_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(blank=True, help_text='order detail', null=True, verbose_name='Maintenance/Service Performed')),
                ('part_no', models.CharField(blank=True, max_length=20, null=True)),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('labor_costs', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=repairs.models.upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0, null=True)),
                ('width_field', models.IntegerField(default=0, null=True)),
                ('asset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.TypeOfAsset')),
                ('engine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='engine_room.Engines')),
                ('service_provider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='providers.Supplier')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp', '-update'],
            },
        ),
    ]
