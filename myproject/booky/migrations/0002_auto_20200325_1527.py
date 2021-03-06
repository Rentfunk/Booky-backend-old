# Generated by Django 3.0.4 on 2020-03-25 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booky', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='books',
            field=models.ManyToManyField(related_name='authors', to='booky.Book'),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='books',
            field=models.ManyToManyField(related_name='classrooms', through='booky.OwnedByClass', to='booky.Book'),
        ),
        migrations.AlterField(
            model_name='order',
            name='forBook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='booky.Book'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='books',
            field=models.ManyToManyField(related_name='teachers', through='booky.OwnedByTeacher', to='booky.Book'),
        ),
    ]
