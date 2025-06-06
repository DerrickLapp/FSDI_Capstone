# Generated by Django 5.2.1 on 2025-06-07 18:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('game_id', models.CharField(max_length=255)),
                ('box_art_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='StreamData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('streamer_id', models.CharField(max_length=255)),
                ('user_name', models.CharField(max_length=255)),
                ('user_id', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('game_id', models.CharField(max_length=255)),
                ('game_name', models.CharField(max_length=255)),
                ('thumbnail_url', models.URLField()),
                ('viewer_count', models.IntegerField(blank=True, null=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('user_login', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Streamer',
                'verbose_name_plural': 'Streamers',
                'ordering': ['user_name', 'started_at'],
            },
        ),
        migrations.CreateModel(
            name='FavoriteGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('favorite_games', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorite_games', to='pages.game')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteStreamer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('favorite_streamers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorite_streamers', to='pages.streamdata')),
            ],
        ),
    ]
