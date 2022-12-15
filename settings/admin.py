from django.contrib import admin
from settings.models import UserSalesShowing, UserTimeZone


admin.site.register(UserSalesShowing)
admin.site.register(UserTimeZone)
admin.site.site_title = 'ACRM'
admin.site.site_header = 'ACRM administration'