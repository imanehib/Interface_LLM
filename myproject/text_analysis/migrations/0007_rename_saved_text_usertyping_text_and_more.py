# Generated by Django 5.1.6 on 2025-03-17 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_analysis', '0006_remove_savedtext_score_savedtext_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usertyping',
            old_name='saved_text',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='savedtext',
            name='list_position',
        ),
        migrations.RemoveField(
            model_name='savedtext',
            name='list_progression',
        ),
        migrations.RemoveField(
            model_name='usertyping',
            name='list_position',
        ),
        migrations.RemoveField(
            model_name='usertyping',
            name='list_progression',
        ),
        migrations.RemoveField(
            model_name='usertyping',
            name='user',
        ),
        migrations.AddField(
            model_name='savedtext',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
