from rest_framework import generics
from serializers import SocketSerializer, PinSerializer
from models import Socket, Pin


class SocketListView(generics.ListCreateAPIView):
    queryset = Socket.objects.all()
    serializer_class = SocketSerializer


class SocketDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Socket.objects.all()
    serializer_class = SocketSerializer

    def put(self, request, *args, **kwargs):
        return generics.RetrieveUpdateDestroyAPIView.put(self, request=request, args= args, kwargs = kwargs)


class PinListView(generics.ListCreateAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer


class PinUpdateView(generics.UpdateAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)