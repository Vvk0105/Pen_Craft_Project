# Generated by Django 3.2.6 on 2024-07-05 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pen', '0009_contactformsubmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]