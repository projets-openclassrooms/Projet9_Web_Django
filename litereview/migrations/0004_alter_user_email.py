# Generated by Django 5.0.2 on 2024-04-03 15:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("litereview", "0003_alter_ticket_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="email address"
            ),
        ),
    ]
