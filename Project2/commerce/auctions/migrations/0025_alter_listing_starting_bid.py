# Generated by Django 5.0.6 on 2024-07-14 01:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_alter_listing_starting_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
