# Generated by Django 4.0.5 on 2023-07-22 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehiculo',
            options={'permissions': (('Visualizar_catalogo', 'Puede visualizar_catalogo'),)},
        ),
    ]