# Generated by Django 3.0.9 on 2020-08-10 09:46

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product', name='uuid', field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
