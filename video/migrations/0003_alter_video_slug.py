# Generated by Django 4.1 on 2022-08-15 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True, unique=True),
        ),
    ]
