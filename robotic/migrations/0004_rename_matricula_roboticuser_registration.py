# Generated by Django 4.2.8 on 2024-03-15 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robotic', '0003_alter_roboticuser_is_active_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roboticuser',
            old_name='matricula',
            new_name='registration',
        ),
    ]
