# Generated by Django 5.1.4 on 2025-01-07 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_borrowmodel_rturn_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Reviews',
        ),
    ]
