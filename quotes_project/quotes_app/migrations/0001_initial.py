# Generated by Django 4.2 on 2023-04-14 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=150)),
                ('born_date', models.DateField()),
                ('born_location', models.CharField(max_length=100)),
                ('description', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.CharField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotes_app.author')),
                ('tags', models.ManyToManyField(to='quotes_app.tag')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
