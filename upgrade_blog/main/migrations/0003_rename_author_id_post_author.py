# Generated by Django 4.2.3 on 2023-07-20 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_post_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author_id',
            new_name='author',
        ),
    ]
