# Generated by Django 5.0.6 on 2024-07-25 05:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_post_poster_likeship'),
    ]

    operations = [
        migrations.AddField(
            model_name='likeship',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='liked_post', to='network.post'),
        ),
        migrations.AlterField(
            model_name='likeship',
            name='liker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='liker', to=settings.AUTH_USER_MODEL),
        ),
    ]
