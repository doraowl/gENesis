# Generated by Django 3.0.7 on 2020-06-19 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='tag',
            field=models.TextField(default=''),
        ),
    ]
