from datetime import datetime

from django_filters import rest_framework as filters

from events.models import Event


class EventFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='iexact')

    ongoing_events = filters.DateTimeFilter(field_name='event_start', label='Ongoing Events', method='ongoing')
    passed_events = filters.DateTimeFilter(field_name='event_end', label='Passed Events', method='passed')

    user_events = filters.BooleanFilter(field_name='created_by', label='Show Your/Others Events', method='user_event')

    def ongoing(self, queryset, field_name, value):
        return queryset.filter(event_start__gte=value)

    def passed(self, queryset, field_name, value):
        return queryset.filter(event_end__lte=value)

    def user_event(self, queryset, field_name, value):
        if value != None:
            if value:
                return queryset.filter(created_by=self.request.user)
            else:
                return queryset.exclude(created_by=self.request.user)


    class Meta:
        model = Event
        fields = ['name', 'type', 'event_start', 'event_end']
