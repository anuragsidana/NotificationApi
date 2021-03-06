
from rest_framework import serializers
from django.contrib.auth.models import User
from  .models import Appointment

class UserSerializer(serializers.ModelSerializer):
    appointments = serializers.PrimaryKeyRelatedField(many=True, queryset=Appointment.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'appointments')


class AppointmentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Appointment
        fields = ('owner','user_id','name', 'message','date','time')

    # def create(self, validated_data):
    #     obj = Appointment.objects.create(**validated_data)
    #     return obj