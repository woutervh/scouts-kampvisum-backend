# Generated by Django 3.2.12 on 2022-02-28 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import scouts_auth.inuits.models.fields.datetype_aware_date_field
import scouts_auth.inuits.models.fields.django_shorthand_model_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('camps', '0001_initial'),
        ('visums', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_deadline_created', to=settings.AUTH_USER_MODEL, verbose_name='Instance created by')),
            ],
        ),
        migrations.CreateModel(
            name='DefaultDeadline',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('is_important', models.BooleanField(default=False)),
                ('deadline_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('D', 'Deadline'), ('C', 'LinkedCheck deadline'), ('S', 'LinkedSubCategory deadline'), ('M', 'Mix of linked checks and sub categories deadline')], default='D', max_length=1)),
                ('checks', models.ManyToManyField(to='visums.Check')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_defaultdeadline_created', to=settings.AUTH_USER_MODEL, verbose_name='Instance created by')),
                ('sub_categories', models.ManyToManyField(to='visums.SubCategory')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_defaultdeadline_updated', to=settings.AUTH_USER_MODEL, verbose_name='Instance last update by')),
            ],
            options={
                'ordering': ['due_date__date_year', 'due_date__date_month', 'due_date__date_day', 'is_important', 'name'],
            },
        ),
        migrations.CreateModel(
            name='DefaultDeadlineFlag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('flag', models.BooleanField(default=False)),
                ('default_deadline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='default_flags', to='deadlines.defaultdeadline')),
            ],
            options={
                'ordering': ['index', 'name'],
            },
        ),
        migrations.CreateModel(
            name='DeadlineFlag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('flag', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_deadlineflag_created', to=settings.AUTH_USER_MODEL, verbose_name='Instance created by')),
                ('deadline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flags', to='deadlines.deadline')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deadlines.defaultdeadlineflag')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_deadlineflag_updated', to=settings.AUTH_USER_MODEL, verbose_name='Instance last update by')),
            ],
        ),
        migrations.CreateModel(
            name='DeadlineDate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_day', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
                ('date_month', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
                ('date_year', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
                ('calculated_date', scouts_auth.inuits.models.fields.datetype_aware_date_field.DatetypeAwareDateField()),
                ('default_deadline', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='due_date', to='deadlines.defaultdeadline')),
            ],
            options={
                'ordering': ['date_year', 'date_month', 'date_day'],
            },
        ),
        migrations.AddField(
            model_name='deadline',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadline', to='deadlines.defaultdeadline'),
        ),
        migrations.AddField(
            model_name='deadline',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_deadline_updated', to=settings.AUTH_USER_MODEL, verbose_name='Instance last update by'),
        ),
        migrations.AddField(
            model_name='deadline',
            name='visum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadlines', to='visums.campvisum'),
        ),
        migrations.CreateModel(
            name='MixedDeadline',
            fields=[
                ('deadline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='deadlines.deadline')),
                ('linked_checks', models.ManyToManyField(to='visums.LinkedCheck')),
                ('linked_sub_categories', models.ManyToManyField(to='visums.LinkedSubCategory')),
            ],
            options={
                'abstract': False,
            },
            bases=('deadlines.deadline',),
        ),
        migrations.CreateModel(
            name='LinkedSubCategoryDeadline',
            fields=[
                ('deadline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='deadlines.deadline')),
                ('linked_sub_categories', models.ManyToManyField(to='visums.LinkedSubCategory')),
            ],
            options={
                'abstract': False,
            },
            bases=('deadlines.deadline',),
        ),
        migrations.CreateModel(
            name='LinkedCheckDeadline',
            fields=[
                ('deadline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='deadlines.deadline')),
                ('linked_checks', models.ManyToManyField(to='visums.LinkedCheck')),
            ],
            options={
                'abstract': False,
            },
            bases=('deadlines.deadline',),
        ),
        migrations.CreateModel(
            name='DefaultDeadlineSet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('camp_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='default_deadline_set', to='camps.camptype')),
                ('camp_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='default_deadline_set', to='camps.campyear')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_defaultdeadlineset_created', to=settings.AUTH_USER_MODEL, verbose_name='Instance created by')),
                ('default_deadlines', models.ManyToManyField(to='deadlines.DefaultDeadline')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_defaultdeadlineset_updated', to=settings.AUTH_USER_MODEL, verbose_name='Instance last update by')),
            ],
            options={
                'unique_together': {('camp_year', 'camp_type')},
            },
        ),
        migrations.AddConstraint(
            model_name='defaultdeadlineflag',
            constraint=models.UniqueConstraint(fields=('default_deadline', 'name'), name='unique_default_deadline_and_name_for_flag'),
        ),
        migrations.AlterUniqueTogether(
            name='defaultdeadline',
            unique_together={('name', 'deadline_type')},
        ),
        migrations.AlterUniqueTogether(
            name='deadlineflag',
            unique_together={('parent', 'deadline')},
        ),
        migrations.AddConstraint(
            model_name='deadlinedate',
            constraint=models.UniqueConstraint(fields=('default_deadline',), name='unique_default_deadline'),
        ),
        migrations.AlterUniqueTogether(
            name='deadline',
            unique_together={('parent', 'visum')},
        ),
    ]
