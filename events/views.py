from django.http import HttpRequest
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from events.models import Event, Attendance
from events.serializers import EventSerializer, UserSerializer, RegisterUserSerializer
from events.filters import EventFilter


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'], permission_classes=[IsAuthenticated])
    def change_attendance(self, request: HttpRequest, **kwargs):
        event: Event = self.get_object()
        user = request.user
        if event.attendees.filter(user=user).exists():
            event.attendees.filter(event=event, user=user).delete()
            return Response({"status": "unregistered"})
        else:
            if event.attendees.count() < event.capacity:
                Attendance.objects.create(event=event, user=user)
                return Response({"status": "registered"})
            else:
                return Response({"status": "unable to register, max capacity reached"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
