# Generated by Django 4.2 on 2024-05-16 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='onion',
            old_name='user',
            new_name='writer',
        ),
    ]
