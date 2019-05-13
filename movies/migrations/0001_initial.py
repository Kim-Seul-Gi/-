# Generated by Django 2.1.8 on 2019-05-13 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('imageurl', models.CharField(max_length=100)),
                ('birthday', models.CharField(blank=True, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('imageurl', models.CharField(max_length=100)),
                ('release_date', models.CharField(max_length=20)),
                ('overview', models.CharField(default='', max_length=1000)),
                ('director', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='movies.Director')),
                ('genres', models.ManyToManyField(blank=True, related_name='genre_movies', to='movies.Genre')),
            ],
        ),
    ]
