# Generated by Django 5.0.2 on 2024-06-28 08:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pen', '0019_master_username_alter_master_address_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WritingSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Literature-Story', 'Literature-Story'), ('Poem', 'Poem'), ('Novel', 'Novel'), ('Article', 'Article'), ('Journals', 'Journals')], max_length=20)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to='submissions/')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('plagiarism_mark', models.IntegerField(default=0)),
                ('grammatical_mark', models.IntegerField(default=0)),
                ('master_check_mark', models.IntegerField(default=0)),
                ('total_mark', models.IntegerField(default=0)),
                ('reviewed_by', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
