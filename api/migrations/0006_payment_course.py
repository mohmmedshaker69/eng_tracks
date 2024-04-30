# Generated by Django 5.0.4 on 2024-04-30 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_payment_course'),
        ('course', '0013_course_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='course',
            field=models.ManyToManyField(related_name='payment', to='course.course'),
        ),
    ]
