from rest_framework import generics
from serializers import SocketSerializer
from models import Socket


class SocketListView(generics.ListCreateAPIView):
    queryset = Socket.objects.all()
    serializer_class = SocketSerializer


class SocketDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Socket.objects.all()
    serializer_class = SocketSerializer
