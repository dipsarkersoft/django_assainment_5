# Generated by Django 5.1.4 on 2025-01-06 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_borrowmodel_isreturn'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowmodel',
            name='rturn_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
