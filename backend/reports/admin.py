from django.contrib import admin
from . models import Region, Report


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_type_display', 'parent')

admin.site.register(Region, RegionAdmin)
admin.site.register(Report)
