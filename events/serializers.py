from django.contrib.auth import get_user_model
from rest_framework import serializers

from events.models import Event, Attendance


User = get_user_model()

class EventSerializer(serializers.HyperlinkedModelSerializer):
    attendees = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')

    class Meta:
        model = Event
        fields = [
            'id',
            'url',
            'name',
            'description',
            'type',
            'capacity',
            'attendees',
            'event_start',
            'event_end',
        ]
        # DRF's __all__ field doesn't include somehow both the id and url
        # it's dependent on serializer class


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        user.email = validated_data['email']

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
