# Generated by Django 4.2.6 on 2023-11-02 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='created_time',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='published_time',
            new_name='published_at',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='updated_time',
            new_name='updated_at',
        ),
    ]
