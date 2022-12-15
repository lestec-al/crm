from settings.models import UserSalesShowing
from django.utils import timezone
from settings.models import UserTimeZone
import zoneinfo


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            tzname = UserTimeZone.objects.get(user=request.user)
            if tzname and tzname.timezone_field in zoneinfo.available_timezones():
                timezone.activate(zoneinfo.ZoneInfo(tzname.timezone_field))
        except:
            timezone.deactivate()
        return self.get_response(request)


def get_fields_names(request_user):
    """Get 'Sale' showing fields in list_view or search_view"""
    fields = UserSalesShowing.objects.get(user=request_user)
    f_1 = fields._meta.get_fields()
    sale_fields = []
    for field in f_1:
        if field.name != "id" and field.name != "user":
            value = getattr(fields, field.name)
            if value == True:
                name = field.name[:-5]
                sale_fields.append(name)
    return sale_fields