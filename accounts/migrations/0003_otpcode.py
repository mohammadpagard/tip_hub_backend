# Generated by Django 4.1 on 2022-09-05 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_options_user_age_user_bio_user_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=11)),
                ('code', models.SmallIntegerField()),
                ('expiration_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
