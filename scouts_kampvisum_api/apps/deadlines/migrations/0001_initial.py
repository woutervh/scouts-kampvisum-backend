# Generated by Django 3.2.10 on 2022-02-07 07:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import scouts_auth.inuits.models.fields.django_shorthand_model_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
                ('description', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('is_important', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_deadline_created', to=settings.AUTH_USER_MODEL, verbose_name='Instance created by')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_deadline_updated', to=settings.AUTH_USER_MODEL, verbose_name='Instance last update by')),
                ('visum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadlines', to='visums.campvisum')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeadlineDate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_day', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
                ('date_month', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
                ('date_year', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_deadlinedate_created', to=settings.AUTH_USER_MODEL, verbose_name='Instance created by')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_deadlinedate_updated', to=settings.AUTH_USER_MODEL, verbose_name='Instance last update by')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubCategoryDeadline',
            fields=[
                ('deadline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='deadlines.deadline')),
                ('deadline_sub_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadline', to='visums.linkedsubcategory')),
            ],
            options={
                'abstract': False,
            },
            bases=('deadlines.deadline',),
        ),
        migrations.CreateModel(
            name='DeadlineDependentDeadline',
            fields=[
                ('deadline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='deadlines.deadline')),
                ('deadline_due_after_deadline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadline', to='deadlines.deadline')),
            ],
            options={
                'abstract': False,
            },
            bases=('deadlines.deadline',),
        ),
        migrations.CreateModel(
            name='CheckDeadline',
            fields=[
                ('deadline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='deadlines.deadline')),
                ('deadline_check', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.linkedcheck')),
            ],
            options={
                'abstract': False,
            },
            bases=('deadlines.deadline',),
        ),
    ]
