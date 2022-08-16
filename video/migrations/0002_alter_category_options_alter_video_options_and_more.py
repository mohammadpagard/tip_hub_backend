# Generated by Django 4.1 on 2022-08-15 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'دسته بندی', 'verbose_name_plural': 'دسته بندی ها'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': 'ویدئو', 'verbose_name_plural': 'ویدئو ها'},
        ),
        migrations.AlterField(
            model_name='category',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت'),
        ),
        migrations.AlterField(
            model_name='category',
            name='is_child',
            field=models.BooleanField(default=False, verbose_name='فرزند است؟'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='video.category', verbose_name='فرزند'),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='video',
            name='about_video',
            field=models.TextField(verbose_name='درباره ویدئو'),
        ),
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.ManyToManyField(related_name='cvideos', to='video.category', verbose_name='دسته بندی ها'),
        ),
        migrations.AlterField(
            model_name='video',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت'),
        ),
        migrations.AlterField(
            model_name='video',
            name='image',
            field=models.ImageField(upload_to='videos/images/', verbose_name='عکس نمایشی'),
        ),
        migrations.AlterField(
            model_name='video',
            name='master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to=settings.AUTH_USER_MODEL, verbose_name='استاد'),
        ),
        migrations.AlterField(
            model_name='video',
            name='time',
            field=models.IntegerField(default=1, verbose_name='زمان ویدئو'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='عنوان ویدئو'),
        ),
        migrations.AlterField(
            model_name='video',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(upload_to='videos/', verbose_name='ویدئو'),
        ),
        migrations.AlterField(
            model_name='video',
            name='views',
            field=models.PositiveBigIntegerField(default=1, verbose_name='بازدید'),
        ),
    ]