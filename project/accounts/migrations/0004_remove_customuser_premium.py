# Generated by Django 4.2.4 on 2023-08-29 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_stripe_sub_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='premium',
        ),
    ]
