# Generated by Django 4.2 on 2024-05-20 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onions', '0003_onion_parent_onion'),
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='object_id',
        ),
        migrations.AddField(
            model_name='vote',
            name='onion',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, to='onions.onion'),
            preserve_default=False,
        ),
    ]
