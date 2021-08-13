# Generated by Django 3.2.6 on 2021-08-13 09:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScoutsGroup',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScoutsGroupType',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('type', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['type'],
            },
        ),
        migrations.CreateModel(
            name='ScoutsSectionName',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScoutsSection',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scouts_groups.scoutsgroup')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='scouts_groups.scoutssectionname')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='scoutsgroup',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scouts_groups.scoutsgrouptype'),
        ),
        migrations.CreateModel(
            name='DefaultScoutsSectionName',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scouts_groups.scoutssectionname')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scouts_groups.scoutsgrouptype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
