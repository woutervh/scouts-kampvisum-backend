# Generated by Django 3.2.6 on 2021-08-25 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import inuits.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Camp',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
                ('start_date', inuits.models.OptionalDateField(blank=True, null=True)),
                ('end_date', inuits.models.OptionalDateField(blank=True, null=True)),
            ],
            options={
                'ordering': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='CampYear',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('year', models.IntegerField(verbose_name='year')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.AddConstraint(
            model_name='campyear',
            constraint=models.UniqueConstraint(fields=('year',), name='unique_year'),
        ),
        migrations.AddField(
            model_name='camp',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='camps_camp_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='camp',
            name='sections',
            field=models.ManyToManyField(to='groups.Section'),
        ),
        migrations.AddField(
            model_name='camp',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camps.campyear'),
        ),
    ]
