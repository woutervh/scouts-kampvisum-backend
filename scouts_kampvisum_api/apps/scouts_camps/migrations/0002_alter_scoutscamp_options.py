# Generated by Django 3.2.6 on 2021-08-21 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scouts_camps', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scoutscamp',
            options={'ordering': ['start_date']},
        ),
    ]
