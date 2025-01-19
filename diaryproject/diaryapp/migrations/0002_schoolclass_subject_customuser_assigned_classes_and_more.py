# Generated by Django 5.1.4 on 2025-01-19 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaryapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='assigned_classes',
            field=models.ManyToManyField(blank=True, to='diaryapp.schoolclass'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='assigned_subjects',
            field=models.ManyToManyField(blank=True, to='diaryapp.subject'),
        ),
    ]
