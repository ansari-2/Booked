# Generated by Django 3.2.12 on 2023-03-08 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sliderimage', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='phone',
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
