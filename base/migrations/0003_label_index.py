# Generated by Django 5.0.3 on 2024-03-19 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_dataset_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='index',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
