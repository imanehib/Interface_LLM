# Generated by Django 5.0.1 on 2025-04-08 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_analysis', '0011_savedtext_list_position_savedtext_list_progression_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savedtext',
            name='list_position',
        ),
        migrations.RemoveField(
            model_name='savedtext',
            name='list_progression',
        ),
        migrations.AlterField(
            model_name='savedtext',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
