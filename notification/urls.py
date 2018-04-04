from django.conf.urls import url
from django.urls import path

from .views import AppointmentListView, AppointmentCreateView, AppointmentDetailView, AppointmentUpdateView, AppointmentDeleteView
from .views import AppointmentList,AppointmentDetail,UserDetail,UserList,create_auth

urlpatterns = [
    # List and detail views
    url(r'^$', AppointmentListView.as_view(), name='list_appointments'),
    url(r'^/(?P<pk>[0-9]+)$', AppointmentDetailView.as_view(), name='view_appointment'),

    # Create, update, delete
    url(r'^/new$', AppointmentCreateView.as_view(), name='new_appointment'),
    url(r'^/(?P<pk>[0-9]+)/edit$', AppointmentUpdateView.as_view(), name='edit_appointment'),
    url(r'^/(?P<pk>[0-9]+)/delete$', AppointmentDeleteView.as_view(), name='delete_appointment'),
    path('notification/',AppointmentList.as_view()),
    url(r'^notification/(?P<pk>[0-9]+)/$', AppointmentDetail.as_view()),
path('users/', UserList.as_view()),
url(r'^users/(?P<pk>[0-9]+)/$',UserDetail.as_view()),

path('users/register',create_auth),
]
