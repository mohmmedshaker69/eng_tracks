# Generated by Django 5.0.4 on 2024-04-16 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_alter_course_chapters_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='chapters_count',
            field=models.IntegerField(),
        ),
    ]
