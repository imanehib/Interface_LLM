# Generated by Django 5.1.6 on 2025-03-17 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text_analysis', '0008_usertyping_cursor_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypingEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=255)),
                ('cursor_position', models.IntegerField()),
                ('text_progression', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
