# Generated by Django 3.2.11 on 2022-02-18 11:00

from django.db import migrations, models
import django.db.models.deletion
import scouts_auth.inuits.models.fields.django_shorthand_model_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultScoutsSectionName',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ScoutsGroupType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('group_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=64)),
            ],
            options={
                'ordering': ['group_type'],
            },
        ),
        migrations.CreateModel(
            name='ScoutsSection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('group_group_admin_id', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=64)),
                ('hidden', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name__age_group'],
            },
        ),
        migrations.CreateModel(
            name='ScoutsSectionName',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('gender', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('F', 'Female'), ('I', 'Mixed'), ('M', 'Male'), ('X', 'Other'), ('U', 'Unknown')], default='U', max_length=1)),
                ('age_group', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('hidden', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['age_group'],
            },
        ),
        migrations.AddConstraint(
            model_name='scoutssectionname',
            constraint=models.UniqueConstraint(fields=('name', 'gender', 'age_group'), name='unique_name_gender_and_age_group'),
        ),
        migrations.AddField(
            model_name='scoutssection',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='groups.scoutssectionname'),
        ),
        migrations.AddField(
            model_name='scoutsgrouptype',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.scoutsgrouptype'),
        ),
        migrations.AddField(
            model_name='defaultscoutssectionname',
            name='group_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.scoutsgrouptype'),
        ),
        migrations.AddField(
            model_name='defaultscoutssectionname',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='groups.scoutssectionname'),
        ),
        migrations.AddConstraint(
            model_name='scoutssection',
            constraint=models.UniqueConstraint(fields=('group_group_admin_id', 'name'), name='unique_section_group_group_admin_id_and_name'),
        ),
        migrations.AddConstraint(
            model_name='scoutsgrouptype',
            constraint=models.UniqueConstraint(fields=('group_type',), name='unique_group_type'),
        ),
        migrations.AlterUniqueTogether(
            name='defaultscoutssectionname',
            unique_together={('group_type', 'name')},
        ),
    ]
