# Generated by Django 3.0.4 on 2020-04-05 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0016_remove_membership_manager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Manager',
        ),
    ]
