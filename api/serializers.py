from rest_framework.serializers import ModelSerializer
from models import Socket


class SocketSerializer(ModelSerializer):
    class Meta:
        model = Socket
        fields = '__all__'
