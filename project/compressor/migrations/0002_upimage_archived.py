# Generated by Django 4.2.4 on 2023-08-27 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compressor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upimage',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
