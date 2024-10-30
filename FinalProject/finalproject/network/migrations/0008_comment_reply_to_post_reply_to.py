# Generated by Django 5.0.6 on 2024-07-31 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reply_comment', to='network.comment'),
        ),
        migrations.AddField(
            model_name='post',
            name='reply_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reply', to='network.post'),
        ),
    ]