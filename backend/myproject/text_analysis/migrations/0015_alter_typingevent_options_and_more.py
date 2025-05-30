# Generated by Django 5.0.1 on 2025-05-15 06:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_analysis', '0014_remove_exercise_xml_content_exercise_content'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='typingevent',
            options={'ordering': ['timestamp']},
        ),
        migrations.RemoveField(
            model_name='typingevent',
            name='session_id',
        ),
        migrations.AddField(
            model_name='typingevent',
            name='action',
            field=models.CharField(choices=[('insert', 'insert'), ('delete', 'delete')], default='insert', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='typingevent',
            name='char',
            field=models.CharField(default='', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='typingevent',
            name='exercise',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='text_analysis.exercise'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='typingevent',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exercise',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='typingevent',
            name='cursor_position',
            field=models.PositiveIntegerField(),
        ),
    ]
