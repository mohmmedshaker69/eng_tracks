# Generated by Django 5.0.4 on 2024-04-30 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_paymentmethod_payment_delete_enrollment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='course',
        ),
    ]
