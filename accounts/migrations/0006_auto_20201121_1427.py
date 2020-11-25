# Generated by Django 3.1.3 on 2020-11-21 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20201121_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(help_text='Required: Username. 50 characters or less.', max_length=50, unique=True),
        ),
    ]
