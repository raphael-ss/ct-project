# Generated by Django 4.2.7 on 2024-01-25 17:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0004_alter_socialmediametric_network"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="campaignmetric",
            name="funnel_position",
        ),
        migrations.AddField(
            model_name="campaignmetric",
            name="objective",
            field=models.CharField(
                choices=[("Exposição", "Exposição de Marca"), ("Vendas", "Vendas")],
                default="Vendas",
                max_length=20,
            ),
        ),
    ]