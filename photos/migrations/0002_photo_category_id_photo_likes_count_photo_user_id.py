# Generated by Django 5.2 on 2025-04-20 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='category_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='photo',
            name='likes_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='photo',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]
