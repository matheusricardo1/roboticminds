# Generated by Django 4.2.8 on 2024-03-15 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robotic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roboticuser',
            name='data_nasc',
            field=models.DateField(null=True),
        ),
    ]
