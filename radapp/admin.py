from django.contrib import admin
from .models import (
    Radcheck, Radreply, Radgroupcheck, Radgroupreply,
    Radusergroup, Radacct, Radpostauth, Nas
)

@admin.register(Radcheck)
class RadcheckAdmin(admin.ModelAdmin):
    list_display = ('username', 'attribute', 'op', 'value')
    search_fields = ('username',)
    inlines = []


@admin.register(Radreply)
class RadreplyAdmin(admin.ModelAdmin):
    list_display = ('username', 'attribute', 'value')
    search_fields = ('username__username',)


@admin.register(Radgroupcheck)
class RadgroupcheckAdmin(admin.ModelAdmin):
    list_display = ('groupname', 'attribute', 'value')
    search_fields = ('groupname',)


@admin.register(Radgroupreply)
class RadgroupreplyAdmin(admin.ModelAdmin):
    list_display = ('groupname', 'attribute', 'value')
    search_fields = ('groupname',)


@admin.register(Radusergroup)
class RadusergroupAdmin(admin.ModelAdmin):
    list_display = ('username', 'groupname', 'priority')
    search_fields = ('username__username', 'groupname__groupname')


@admin.register(Radacct)
class RadacctAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'nasipaddress', 'acctstarttime',
        'acctstoptime', 'acctsessiontime', 'acctterminatecause'
    )
    search_fields = ('username__username', 'acctsessionid', 'nasipaddress')
    list_filter = ('acctterminatecause',)
    readonly_fields = [f.name for f in Radacct._meta.fields]

    # Make read-only (log data)
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Radpostauth)
class RadpostauthAdmin(admin.ModelAdmin):
    list_display = ('username', 'reply', 'authdate')
    search_fields = ('username__username',)
    list_filter = ('reply',)
    readonly_fields = [f.name for f in Radpostauth._meta.fields]

    # Make read-only (log data)
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Nas)
class NasAdmin(admin.ModelAdmin):
    list_display = ('nasname', 'shortname', 'type', 'description')
    search_fields = ('nasname', 'shortname')
