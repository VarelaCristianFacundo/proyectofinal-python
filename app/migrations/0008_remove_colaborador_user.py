# Generated by Django 4.2.4 on 2023-10-09 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_colaborador_user_alter_colaborador_apellido_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colaborador',
            name='user',
        ),
    ]
