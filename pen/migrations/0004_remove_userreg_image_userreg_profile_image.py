# Generated by Django 5.0.2 on 2024-06-26 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pen', '0003_alter_userreg_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userreg',
            name='image',
        ),
        migrations.AddField(
            model_name='userreg',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
