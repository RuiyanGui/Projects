# Generated by Django 5.0.6 on 2024-08-01 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0015_alter_archived_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archived',
            name='archive',
            field=models.ManyToManyField(blank=True, null=True, related_name='archived_location', to='network.archive'),
        ),
    ]
