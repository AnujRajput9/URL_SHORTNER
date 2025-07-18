# Generated by Django 5.1.5 on 2025-07-18 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortcode', models.CharField(max_length=10, unique=True)),
                ('original_url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('click_count', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ClickAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('referrer', models.CharField(blank=True, max_length=255, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('short_url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortner.shorturl')),
            ],
        ),
    ]
