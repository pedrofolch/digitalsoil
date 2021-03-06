# Generated by Django 2.2 on 2019-04-10 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='first name', max_length=35)),
                ('last_name', models.CharField(default='last name', max_length=35)),
                ('title', models.CharField(blank=True, help_text='position', max_length=30, null=True)),
                ('slug', models.SlugField(blank=True, help_text='leave blank, or unique name', null=True, unique=True)),
                ('license_no', models.CharField(default='123456789', max_length=17, unique=True, verbose_name='license number')),
                ('is_crew', models.BooleanField(default=False)),
                ('is_service_provider', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.IntegerField(blank=True, help_text='include all numbers', null=True)),
                ('is_mechanic', models.BooleanField(default=False)),
                ('content', models.TextField(blank=True, help_text='specializes on', null=True)),
                ('rate', models.PositiveIntegerField(blank=True, default='65', null=True)),
            ],
            options={
                'ordering': ['user', '-rate'],
            },
        ),
    ]
