# Generated by Django 4.0 on 2024-06-03 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='images/default.png', upload_to='users/%Y/%m/%d'),
        ),
    ]
