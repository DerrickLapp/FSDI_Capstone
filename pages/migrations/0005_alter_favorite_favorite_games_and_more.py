# Generated by Django 5.2.1 on 2025-05-28 01:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_rename_favorites_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='favorite_games',
            field=models.ForeignKey(blank=True, default='N/A', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorite_games', to='pages.game'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='favorite_streamers',
            field=models.ForeignKey(blank=True, default='N/A', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorite_streamers', to='pages.streamdata'),
        ),
    ]
