# Generated by Django 4.1.7 on 2023-06-11 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0010_alter_workout_workout_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='descrizione',
            field=models.CharField(blank=True, default=' ', max_length=50, null=True),
        ),
    ]
