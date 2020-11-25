# Generated by Django 3.1.3 on 2020-11-12 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_biography'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='biography',
            field=models.TextField(blank=True, help_text='Tell us about yourself.', null=True),
        ),
    ]
