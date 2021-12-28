from django.contrib import admin

from scouts_auth.groupadmin.models import ScoutsUser

admin.site.register(ScoutsUser)
admin.register(ScoutsUser)
