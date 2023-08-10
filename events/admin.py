from django.contrib import admin

from events.models import Event, Attendance


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    pass
