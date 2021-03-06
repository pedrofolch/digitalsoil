# Generated by Django 2.2 on 2019-04-10 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('providers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fieldwork', '0001_initial'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fielddata',
            name='brand_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='providers.Supplier'),
        ),
        migrations.AddField(
            model_name='fielddata',
            name='pile_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.Recipe'),
        ),
        migrations.AddField(
            model_name='fielddata',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
