# Generated by Django 4.1 on 2022-08-15 16:03

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_alter_category_options_alter_video_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='about_video',
            field=ckeditor.fields.RichTextField(verbose_name='درباره ویدئو'),
        ),
    ]
