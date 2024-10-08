# Generated by Django 5.0.7 on 2024-09-19 13:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('math', 'Mathematics'), ('science', 'Science'), ('history', 'History'), ('tech', 'Technology')], max_length=20)),
                ('instructor', models.ForeignKey(limit_choices_to={'role': 'instructor'}, on_delete=django.db.models.deletion.CASCADE, to='edu_app.profile')),
            ],
        ),
    ]
