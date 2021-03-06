# Generated by Django 2.2 on 2019-04-10 00:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('slug', models.SlugField(default='abc', unique=True)),
                ('active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['title', 'timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('embed_code', models.CharField(blank=True, max_length=500, null=True)),
                ('share_message', models.TextField(default='Check out this awesome video.')),
                ('order', models.PositiveIntegerField(default=1)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('free_preview', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='videos.Category')),
            ],
            options={
                'verbose_name': 'video',
                'verbose_name_plural': 'videos',
                'ordering': ['order', '-timestamp'],
                'unique_together': {('slug', 'category')},
            },
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.SlugField(choices=[('compost', 'compost'), ('Vermicompost', 'vermicompost'), ('bulk', 'bulk'), ('premium', 'premium'), ('other', 'other')])),
                ('object_id', models.PositiveIntegerField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='videos.Category')),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
                ('video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='videos.Video')),
            ],
        ),
    ]
