# Generated by Django 3.0.4 on 2020-04-03 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booky', '0007_auto_20200330_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='forGrade',
        ),
        migrations.AddField(
            model_name='book',
            name='forGrades',
            field=models.ManyToManyField(related_name='books', to='booky.Grade'),
        ),
    ]
