# Generated by Django 4.2 on 2024-05-23 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onions', '0005_onionversus_orange_embedding_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='onionversus',
            name='ov_title',
            field=models.CharField(default='No title', max_length=30),
        ),
    ]