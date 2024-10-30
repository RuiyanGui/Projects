# Generated by Django 5.0.6 on 2024-08-03 03:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0019_comment_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(blank=True, default='empty', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='reply_comment', to='network.comment'),
        ),
    ]
