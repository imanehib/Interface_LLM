# Generated by Django 5.1.6 on 2025-03-18 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_analysis', '0010_rename_text_usertyping_text_progression_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedtext',
            name='list_position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='savedtext',
            name='list_progression',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='savedtext',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
