# Generated by Django 3.2.12 on 2022-03-10 21:02

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import scouts_auth.inuits.files.validators
import scouts_auth.inuits.models.fields.django_shorthand_model_fields
import scouts_auth.inuits.models.fields.timezone_aware_date_time_field
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScoutsUser",
            fields=[
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator
                        ],
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=150)),
                ("last_name", models.CharField(blank=True, max_length=150)),
                (
                    "email",
                    scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalEmailField(
                        blank=True, default="", max_length=254, null=True
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("password", models.CharField(max_length=128)),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                (
                    "group_admin_id",
                    models.CharField(blank=True, db_column="ga_id", max_length=48),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("F", "Female"),
                            ("I", "Mixed"),
                            ("M", "Male"),
                            ("X", "Other"),
                            ("U", "Unknown"),
                        ],
                        default="U",
                        max_length=16,
                    ),
                ),
                ("phone_number", models.CharField(blank=True, max_length=48)),
                ("membership_number", models.CharField(blank=True, max_length=48)),
                ("customer_number", models.CharField(blank=True, max_length=48)),
                ("birth_date", models.DateField(blank=True, null=True)),
                (
                    "last_authenticated",
                    scouts_auth.inuits.models.fields.timezone_aware_date_time_field.TimezoneAwareDateTimeField(
                        default=datetime.datetime.now
                    ),
                ),
                (
                    "last_refreshed",
                    scouts_auth.inuits.models.fields.timezone_aware_date_time_field.TimezoneAwareDateTimeField(
                        default=datetime.datetime.now
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
            ],
            options={
                "permissions": (
                    ("access_disabled_entities", "Access disabled entities"),
                ),
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="ScoutsGroup",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "group_admin_id",
                    scouts_auth.inuits.models.fields.django_shorthand_model_fields.RequiredCharField(
                        max_length=128
                    ),
                ),
                (
                    "number",
                    scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(
                        blank=True, max_length=128
                    ),
                ),
                (
                    "name",
                    scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(
                        blank=True, max_length=128
                    ),
                ),
                (
                    "group_type",
                    scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(
                        blank=True, max_length=128
                    ),
                ),
                ("default_sections_loaded", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="scouts_auth_scoutsgroup_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="scouts_auth_scoutsgroup_updated",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="updated by",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ScoutsFunction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "group_admin_id",
                    scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(
                        blank=True, max_length=128
                    ),
                ),
                (
                    "code",
                    scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(
                        blank=True, max_length=128
                    ),
                ),
                (
                    "type",
                    scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(
                        blank=True, max_length=128
                    ),
                ),
                (
                    "description",
                    scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalCharField(
                        blank=True, max_length=128
                    ),
                ),
                (
                    "begin",
                    scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalDateTimeField(
                        blank=True, null=True
                    ),
                ),
                (
                    "end",
                    scouts_auth.inuits.models.fields.django_shorthand_model_fields.OptionalDateTimeField(
                        blank=True, null=True
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="scouts_auth_scoutsfunction_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="functions",
                        to="scouts_auth.scoutsgroup",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="scouts_auth_scoutsfunction_updated",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="updated by",
                    ),
                ),
            ],
            options={
                "ordering": ["code"],
            },
        ),
        migrations.CreateModel(
            name="PersistedFile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_on", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="",
                        validators=[
                            scouts_auth.inuits.files.validators.validate_uploaded_file
                        ],
                    ),
                ),
                ("content_type", models.CharField(max_length=100)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="scouts_auth_persistedfile_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created by",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="scouts_auth_persistedfile_updated",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="updated by",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="scoutsuser",
            name="persisted_scouts_functions",
            field=models.ManyToManyField(
                related_name="user", to="scouts_auth.ScoutsFunction"
            ),
        ),
        migrations.AddField(
            model_name="scoutsuser",
            name="persisted_scouts_groups",
            field=models.ManyToManyField(
                related_name="user", to="scouts_auth.ScoutsGroup"
            ),
        ),
        migrations.AddField(
            model_name="scoutsuser",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.Permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.AddConstraint(
            model_name="scoutsgroup",
            constraint=models.UniqueConstraint(
                fields=("group_admin_id",), name="unique_group_admin_id_for_group"
            ),
        ),
        migrations.AddConstraint(
            model_name="scoutsfunction",
            constraint=models.UniqueConstraint(
                fields=("group_admin_id",), name="unique_group_admin_id"
            ),
        ),
    ]
