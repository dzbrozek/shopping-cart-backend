# Generated by Django 3.0.9 on 2020-08-10 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baskets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='updated',
            field=models.BooleanField(
                default=False, help_text='Indicates that basket has been updated since last check'
            ),
        ),
    ]