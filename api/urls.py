from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from views import *

urlpatterns = [
    url(r'^sockets/$', SocketListView.as_view(), name='sockets'),
    url(r'^sockets/(?P<pk>[0-9]+)/$', SocketDetailsView.as_view(), name='socketDetail'),
    url(r'^pin/$', PinListView.as_view(), name='pins'),
    url(r'^pin/(?P<pk>[0-9]+)/$', PinUpdateView.as_view(), name='pinDetails'),
]

urlpatterns = format_suffix_patterns(urlpatterns)