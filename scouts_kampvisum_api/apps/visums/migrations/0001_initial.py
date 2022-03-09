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
        ('scouts_auth', '0001_initial'),
        ('participants', '0001_initial'),
        ('locations', '0001_initial'),
        ('camps', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CampVisum',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('archived_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_archived', models.BooleanField(default=False)),
                ('description', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
            ],
            options={
                'ordering': ['index'],
            },
        ),
        migrations.CreateModel(
            name='CategoryPriority',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('owner', models.CharField(default='Verbond', max_length=32, unique=True)),
                ('priority', models.IntegerField(default=10)),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('archived_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_archived', models.BooleanField(default=False)),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('link', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=64)),
                ('is_multiple', models.BooleanField(default=False)),
                ('is_member', models.BooleanField(default=False)),
                ('change_handler', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=128)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CheckType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('check_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=32)),
            ],
            options={
                'ordering': ['check_type'],
            },
        ),
        migrations.CreateModel(
            name='LinkedCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('archived_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_archived', models.BooleanField(default=False)),
                ('archived_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_linkedcategory_archived', to=settings.AUTH_USER_MODEL, verbose_name='Archived by')),
            ],
            options={
                'ordering': ['parent__index'],
            },
        ),
        migrations.CreateModel(
            name='LinkedCheck',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('archived_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_archived', models.BooleanField(default=False)),
                ('archived_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_linkedcheck_archived', to=settings.AUTH_USER_MODEL, verbose_name='Archived by')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_linkedcheck_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.check')),
            ],
            options={
                'ordering': ['parent__index'],
            },
        ),
        migrations.CreateModel(
            name='LinkedCommentCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('value', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(blank=True, max_length=300)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedDateCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('value', scouts_auth.inuits.models.fields.datetype_aware_date_field.DatetypeAwareDateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedDurationCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('start_date', scouts_auth.inuits.models.fields.datetype_aware_date_field.DatetypeAwareDateField(blank=True, null=True)),
                ('end_date', scouts_auth.inuits.models.fields.datetype_aware_date_field.DatetypeAwareDateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedFileUploadCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedLocationCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('is_camp_location', models.BooleanField(default=False)),
                ('center_latitude', models.FloatField(blank=True, default=50.4956754, null=True)),
                ('center_longitude', models.FloatField(blank=True, default=3.3452037, null=True)),
                ('zoom', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=7)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedNumberCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('value', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedParticipantCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('participant_check_type', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('P', 'participant'), ('M', 'member'), ('C', 'cook'), ('L', 'leader'), ('R', 'responsible'), ('A', 'adult')], default='P', max_length=1)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='LinkedSimpleCheck',
            fields=[
                ('linkedcheck_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='visums.linkedcheck')),
                ('value', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultCharField(blank=True, choices=[('EMPTY', 'Empty'), ('UNCHECKED', 'Unchecked'), ('CHECKED', 'Checked'), ('NOT_APPLICABLE', 'Not applicable')], default='EMPTY', max_length=128)),
            ],
            options={
                'abstract': False,
            },
            bases=('visums.linkedcheck',),
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('archived_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_archived', models.BooleanField(default=False)),
                ('description', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('explanation', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('index', scouts_auth.inuits.models.fields.django_shorthand_model_fields.DefaultIntegerField(blank=True, default=0)),
                ('link', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('label', scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalTextField(blank=True)),
                ('name', scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(max_length=128)),
                ('archived_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_subcategory_archived', to=settings.AUTH_USER_MODEL, verbose_name='Archived by')),
                ('camp_types', models.ManyToManyField(to='camps.CampType')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='visums.category')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LinkedSubCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('archived_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_archived', models.BooleanField(default=False)),
                ('archived_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_linkedsubcategory_archived', to=settings.AUTH_USER_MODEL, verbose_name='Archived by')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='visums.linkedcategory')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_linkedsubcategory_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.subcategory')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_linkedsubcategory_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by')),
            ],
            options={
                'ordering': ['parent__index'],
            },
        ),
        migrations.AddField(
            model_name='linkedcheck',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='visums.linkedsubcategory'),
        ),
        migrations.AddField(
            model_name='linkedcheck',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_linkedcheck_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.CreateModel(
            name='LinkedCategorySet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('visum', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='category_set', to='visums.campvisum')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='linkedcategory',
            name='category_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='visums.linkedcategoryset'),
        ),
        migrations.AddField(
            model_name='linkedcategory',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_linkedcategory_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='linkedcategory',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.category'),
        ),
        migrations.AddField(
            model_name='linkedcategory',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_linkedcategory_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AddConstraint(
            model_name='checktype',
            constraint=models.UniqueConstraint(fields=('check_type',), name='unique_check_type'),
        ),
        migrations.AddField(
            model_name='check',
            name='archived_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_check_archived', to=settings.AUTH_USER_MODEL, verbose_name='Archived by'),
        ),
        migrations.AddField(
            model_name='check',
            name='camp_types',
            field=models.ManyToManyField(to='camps.CampType'),
        ),
        migrations.AddField(
            model_name='check',
            name='check_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visums.checktype'),
        ),
        migrations.AddField(
            model_name='check',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='visums.subcategory'),
        ),
        migrations.AddConstraint(
            model_name='categorypriority',
            constraint=models.UniqueConstraint(fields=('owner',), name='unique_owner'),
        ),
        migrations.AddConstraint(
            model_name='categorypriority',
            constraint=models.UniqueConstraint(fields=('priority',), name='unique_priority'),
        ),
        migrations.AddField(
            model_name='category',
            name='archived_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_category_archived', to=settings.AUTH_USER_MODEL, verbose_name='Archived by'),
        ),
        migrations.AddField(
            model_name='category',
            name='camp_types',
            field=models.ManyToManyField(to='camps.CampType'),
        ),
        migrations.AddField(
            model_name='category',
            name='camp_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='camps.campyear'),
        ),
        migrations.AddField(
            model_name='category',
            name='priority',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='visums.categorypriority'),
        ),
        migrations.AddField(
            model_name='campvisum',
            name='camp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='camps.camp'),
        ),
        migrations.AddField(
            model_name='campvisum',
            name='camp_types',
            field=models.ManyToManyField(to='camps.CampType'),
        ),
        migrations.AddField(
            model_name='campvisum',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_campvisum_created', to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='campvisum',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visums_campvisum_updated', to=settings.AUTH_USER_MODEL, verbose_name='updated by'),
        ),
        migrations.AlterUniqueTogether(
            name='subcategory',
            unique_together={('name', 'category')},
        ),
        migrations.AddField(
            model_name='linkedparticipantcheck',
            name='participants',
            field=models.ManyToManyField(related_name='checks', to='participants.VisumParticipant'),
        ),
        migrations.AddField(
            model_name='linkedlocationcheck',
            name='locations',
            field=models.ManyToManyField(to='locations.LinkedLocation'),
        ),
        migrations.AddField(
            model_name='linkedfileuploadcheck',
            name='value',
            field=models.ManyToManyField(related_name='checks', to='scouts_auth.PersistedFile'),
        ),
        migrations.AlterUniqueTogether(
            name='check',
            unique_together={('name', 'sub_category')},
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('name', 'camp_year'), name='unique_category_name_and_camp_year'),
        ),
    ]
