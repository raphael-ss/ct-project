# Generated by Django 4.2.5 on 2023-11-12 14:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0007_rename_client_id_company_client_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="company",
            old_name="client",
            new_name="client_id",
        ),
        migrations.RenameField(
            model_name="contract",
            old_name="client",
            new_name="client_id",
        ),
        migrations.RenameField(
            model_name="service",
            old_name="client",
            new_name="client_id",
        ),
        migrations.RenameField(
            model_name="service",
            old_name="contract",
            new_name="contract_id",
        ),
        migrations.RenameField(
            model_name="service",
            old_name="member",
            new_name="member_id",
        ),
    ]
