# Generated by Django 5.0.4 on 2024-04-16 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_alter_course_options_remove_chapter_lessons_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='chapters_count',
            field=models.IntegerField(default=0),
        ),
    ]
