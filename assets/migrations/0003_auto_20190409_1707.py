# Generated by Django 2.2 on 2019-04-10 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0002_auto_20190409_1707'),
        ('providers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='marinevessel',
            name='insurance_provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='providers.Supplier'),
        ),
        migrations.AddField(
            model_name='marinevessel',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.MarineModelType'),
        ),
        migrations.AddField(
            model_name='marinevessel',
            name='number_of_through_holes',
            field=models.ManyToManyField(blank=True, to='assets.ThroughHull'),
        ),
        migrations.AddField(
            model_name='marinevessel',
            name='user',
            field=models.ForeignKey(blank=True, help_text='person responsible for', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='equipment',
            name='asset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.EquipmentManufacturer'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.EquipmentModelType'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='user',
            field=models.ForeignKey(blank=True, help_text='person responsible for', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='automobile',
            name='asset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='automobile',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.CarManufacturer'),
        ),
        migrations.AddField(
            model_name='automobile',
            name='insurance_provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='providers.Supplier'),
        ),
        migrations.AddField(
            model_name='automobile',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.CarModelType'),
        ),
        migrations.AddField(
            model_name='automobile',
            name='user',
            field=models.ForeignKey(blank=True, help_text='person responsible for', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asset',
            name='user',
            field=models.ForeignKey(blank=True, help_text='person responsible for', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
