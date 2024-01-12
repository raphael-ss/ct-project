# Generated by Django 4.2.7 on 2024-01-07 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_systemuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemuser',
            name='role',
            field=models.CharField(choices=[('Assessor', 'Assessor(a)'), ('Consultor', 'Consultor(a)'), ('Gerente', 'Gerente'), ('Diretor', 'Diretor(a)'), ('Presidente', 'Presidente')], max_length=20),
        ),
        migrations.AlterField(
            model_name='systemuser',
            name='sector',
            field=models.CharField(choices=[('Tecnologia', 'Tecnologia'), ('Civil', 'Construção Civil'), ('Comercial', 'Comercial'), ('RH', 'Recursos Humanos'), ('Financeiro', 'Adminstrativo Financeiro'), ('Consultoria', 'Consultoria'), ('DirEx', 'Diretoria Executiva')], max_length=20),
        ),
    ]