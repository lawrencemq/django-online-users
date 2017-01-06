from django.contrib import admin

from online_users.models import OnlineUserActivity


class OnlineUserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_activity',)
    search_fields = ['user__username', ]
    list_filter = ['last_activity']

    def get_ordering(self, request):
        return ['last_activity']

admin.site.register(OnlineUserActivity, OnlineUserActivityAdmin)
