# Generated by Django 3.2.10 on 2022-01-03 11:41

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
            name='ScoutsSectionName',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('gender', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('F', 'Female'), ('I', 'Mixed'), ('M', 'Male'), ('O', 'Other'), ('U', 'Unknown')], default='U', max_length=1)),
                ('age_group', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, choices=[(10, 'Leeftijdsgroep 6-9: kapoenen en zeehondjes'), (15, 'Tussentak, leeftijdsgroep 6-9: startleeftijd 7 jaar'), (16, 'Tussentak, leeftijdsgroep 6-9: startleeftijd 8 jaar'), (17, 'Tussentak, leeftijdsgroep 6-9: startleeftijd 9 jaar'), (20, 'Leeftijdsgroep 8-11: kabouter en (zee)welp'), (25, 'Tussentak, leeftijdsgroep 8-11: startleeftijd 9 jaar'), (26, 'Tussentak, leeftijdsgroep 8-11: startleeftijd 10 jaar'), (27, 'Tussentak, leeftijdsgroep 8-11: startleeftijd 11 jaar'), (30, 'Leeftijdsgroep 11-14: jonggivers en scheepsmakkers'), (35, 'Tussentak, leeftijdsgroep 11-14: startleeftijd 12 jaar'), (36, 'Tussentak, leeftijdsgroep 11-14: startleeftijd 13 jaar'), (37, 'Tussentak, leeftijdsgroep 11-14: startleeftijd 14 jaar'), (40, 'Leeftijdsgroep 14-17: gidsen en (zee)verkenners'), (45, 'Tussentak, leeftijdsgroep 14-17: startleeftijd 15 jaar'), (46, 'Tussentak, leeftijdsgroep 14-17: startleeftijd 16 jaar'), (47, 'Tussentak, leeftijdsgroep 14-17: startleeftijd 17 jaar'), (50, 'Leeftijdsgroep 17-18: jins en loodsen'), (55, 'Tussentak, leeftijdsgroep 17-18: startleeftijd 18 jaar'), (60, 'Leeftijdsgroep ouder dan 18, bv. VIPS (akabe)'), (100, 'Leeftijdsgroep voor leiding, district, gouw, verbond'), (999, 'Onbekende leeftijdsgroep')], default=999)),
                ('hidden', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['age_group'],
                'unique_together': {('name', 'gender', 'age_group')},
            },
        ),
        migrations.CreateModel(
            name='ScoutsSection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('group_admin_id', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=64)),
                ('hidden', models.BooleanField(default=False)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='groups.scoutssectionname')),
            ],
            options={
                'ordering': ['name__age_group'],
            },
        ),
        migrations.CreateModel(
            name='ScoutsGroupType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('group_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=64)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.scoutsgrouptype')),
            ],
            options={
                'ordering': ['group_type'],
            },
        ),
        migrations.CreateModel(
            name='DefaultScoutsSectionName',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('group_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.scoutsgrouptype')),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='groups.scoutssectionname')),
            ],
        ),
        migrations.AddConstraint(
            model_name='scoutssection',
            constraint=models.UniqueConstraint(fields=('group_admin_id',), name='unique_section_group_admin_id'),
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
