# Generated by Django 3.1.3 on 2020-11-13 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_blogpost_slug_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
