# Generated by Django 2.1.5 on 2019-01-07 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20190107_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='author',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
