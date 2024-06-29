# Generated by Django 5.0.2 on 2024-06-28 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pen', '0022_writingsubmission_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='writingsubmission',
            name='status',
            field=models.CharField(choices=[('submitted', 'Submitted'), ('open', 'Open'), ('completed', 'Completed')], default='submitted', max_length=20),
        ),
    ]