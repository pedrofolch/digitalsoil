# Generated by Django 2.2 on 2019-04-10 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('tag_line', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, help_text='leave blank or your-brand-name', null=True, unique=True)),
                ('headline', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=120)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=posts.models.upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0, null=True)),
                ('width_field', models.IntegerField(default=0, null=True)),
                ('content', models.TextField()),
                ('draft', models.BooleanField(default=False)),
                ('publish', models.DateField(auto_now_add=True)),
                ('read_time', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('n_comments', models.IntegerField(default=0)),
                ('n_ping_backs', models.IntegerField(default=0)),
                ('rating', models.IntegerField(default=0)),
                ('authors', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.Author')),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.Blog')),
                ('user', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp', '-updated'],
            },
        ),
    ]
