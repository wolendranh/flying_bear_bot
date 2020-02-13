# Generated by Django 2.2.3 on 2020-02-07 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snow_camera', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='camera',
            old_name='url',
            new_name='url_en',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='url',
            new_name='url_en',
        ),
        migrations.AddField(
            model_name='camera',
            name='url_uk',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='url_uk',
            field=models.URLField(blank=True, null=True),
        ),
    ]
