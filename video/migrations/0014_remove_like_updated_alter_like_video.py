# Generated by Django 4.1 on 2022-08-19 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0013_alter_comment_options_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='updated',
        ),
        migrations.AlterField(
            model_name='like',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_likes', to='video.video', verbose_name='ویدئو'),
        ),
    ]
