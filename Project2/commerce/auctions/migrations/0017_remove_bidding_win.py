# Generated by Django 5.0.6 on 2024-07-10 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_bidding_win'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bidding',
            name='win',
        ),
    ]
