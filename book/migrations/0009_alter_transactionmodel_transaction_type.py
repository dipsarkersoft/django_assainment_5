# Generated by Django 5.1.4 on 2025-01-07 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_transactionmodel_delete_transactionsmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionmodel',
            name='transaction_type',
            field=models.IntegerField(choices=[(1, 'Deposit'), (2, 'Borrow'), (3, 'RETURN')], null=True),
        ),
    ]
