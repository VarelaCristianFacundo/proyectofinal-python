# Generated by Django 4.2.4 on 2023-10-06 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_presupuesto_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='vencido',
            field=models.BooleanField(default=False),
        ),
    ]
