# Generated by Django 4.2.7 on 2024-01-07 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemuser',
            name='role',
            field=models.CharField(choices=[('ASS', 'Assessor(a)'), ('CON', 'Consultor(a)'), ('GER', 'Gerente'), ('DIR', 'Diretor(a)'), ('PRE', 'Presidente')], max_length=20),
        ),
    ]