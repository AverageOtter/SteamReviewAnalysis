# Generated by Django 5.0.3 on 2024-04-25 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SteamGames',
            fields=[
                ('json_response', models.TextField()),
                ('app_id', models.IntegerField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('TTL', models.DateTimeField()),
            ],
        ),
    ]
