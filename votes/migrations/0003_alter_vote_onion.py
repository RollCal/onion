# Generated by Django 4.2 on 2024-05-22 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('onions', '0004_onion_color'),
        ('votes', '0002_remove_vote_content_type_remove_vote_object_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='onion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='onions.onion'),
        ),
    ]
