# Generated by Django 4.2.1 on 2024-02-04 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crudinn', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='innmodel',
            name='anonymization',
            field=models.BooleanField(default=False),
        ),
    ]