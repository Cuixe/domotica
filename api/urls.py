from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from views import SocketListView, SocketDetailsView

urlpatterns = [
    url(r'^sockets/$', SocketListView.as_view(), name='sockets'),
    url(r'^sockets/(?P<pk>[0-9]+)/$', SocketDetailsView.as_view(), name='socketDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)