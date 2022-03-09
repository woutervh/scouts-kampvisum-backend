# Generated by Django 3.2.12 on 2022-03-09 19:33

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
            ],
            options={
                'ordering': ['date_year', 'date_month', 'date_day'],
            },
        ),
        migrations.CreateModel(
            name='DeadlineFlag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('flag', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeadlineItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
            ],
            options={
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='DefaultDeadline',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('is_important', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['index', 'due_date__date_year', 'due_date__date_month', 'due_date__date_day', 'is_important', 'name'],
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
            ],
            options={
                'ordering': ['index', 'name'],
            },
        ),
        migrations.CreateModel(
            name='DefaultDeadlineItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('deadline_item_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('D', 'Deadline'), ('C', 'LinkedCheck deadline'), ('S', 'LinkedSubCategory deadline')], default='D', max_length=1)),
                ('item_check', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='visums.check')),
                ('item_flag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_deadline_item', to='deadlines.defaultdeadlineflag')),
                ('item_sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='visums.subcategory')),
            ],
            options={
                'ordering': ['index'],
            },
        ),
        migrations.AddConstraint(
            model_name='defaultdeadlineflag',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_default_deadline_flag_name'),
        ),
        migrations.AddField(
            model_name='defaultdeadline',
            name='camp_types',
            field=models.ManyToManyField(related_name='deadlines', to='camps.CampType'),
        ),
        migrations.AddField(
            model_name='defaultdeadline',
            name='camp_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='default_deadline_set', to='camps.campyear'),
        ),
        migrations.AddField(
            model_name='defaultdeadline',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_defaultdeadline_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='defaultdeadline',
            name='items',
            field=models.ManyToManyField(to='deadlines.DefaultDeadlineItem'),
        ),
        migrations.AddField(
            model_name='defaultdeadline',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_defaultdeadline_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AddField(
            model_name='deadlineitem',
            name='flag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deadline_item', to='deadlines.deadlineflag'),
        ),
        migrations.AddField(
            model_name='deadlineitem',
            name='linked_check',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deadline_items', to='visums.linkedcheck'),
        ),
        migrations.AddField(
            model_name='deadlineitem',
            name='linked_sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deadline_items', to='visums.linkedsubcategory'),
        ),
        migrations.AddField(
            model_name='deadlineitem',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadline_item', to='deadlines.defaultdeadlineitem'),
        ),
        migrations.AddField(
            model_name='deadlineflag',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_deadlineflag_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='deadlineflag',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deadlines.defaultdeadlineflag'),
        ),
        migrations.AddField(
            model_name='deadlineflag',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_deadlineflag_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AddField(
            model_name='deadlinedate',
            name='default_deadline',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='due_date', to='deadlines.defaultdeadline'),
        ),
        migrations.AddField(
            model_name='deadline',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_deadline_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='deadline',
            name='items',
            field=models.ManyToManyField(related_name='deadline', to='deadlines.DeadlineItem'),
        ),
        migrations.AddField(
            model_name='deadline',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadline', to='deadlines.defaultdeadline'),
        ),
        migrations.AddField(
            model_name='deadline',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deadlines_deadline_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AddField(
            model_name='deadline',
            name='visum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deadlines', to='visums.campvisum'),
        ),
        migrations.AddConstraint(
            model_name='defaultdeadline',
            constraint=models.UniqueConstraint(fields=('name', 'camp_year'), name='unique_name__camp_year'),
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
