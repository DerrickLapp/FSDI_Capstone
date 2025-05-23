# Generated by Django 5.2.1 on 2025-05-21 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_remove_streamdata_start_time_streamdata_game_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamdata',
            name='game_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='streamdata',
            name='started_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='streamdata',
            name='thumbnail_url',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='streamdata',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='streamdata',
            name='user_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='streamdata',
            name='user_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='streamdata',
            name='viewer_count',
            field=models.IntegerField(),
        ),
    ]
