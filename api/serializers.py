from rest_framework import serializers
from models import Socket, Pin


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = '__all__'


class SocketSerializer(serializers.ModelSerializer):
    pin = PinSerializer(read_only=False)

    class Meta:
        model = Socket
        fields = '__all__'



