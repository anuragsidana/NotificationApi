from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Appointment

class AppointmentListView(ListView):
    """Shows users a list of appointments"""

    model = Appointment


class AppointmentDetailView(DetailView):
    """Shows users a single appointment"""

    model = Appointment


class AppointmentCreateView(SuccessMessageMixin, CreateView):
    """Powers a form to create a new appointment"""

    model = Appointment
    fields = ['name', 'phone_number', 'time', 'time_zone']
    success_message = 'Appointment successfully created.'


class AppointmentUpdateView(SuccessMessageMixin, UpdateView):
    """Powers a form to edit existing appointments"""

    model = Appointment
    fields = ['name', 'phone_number', 'time', 'time_zone']
    success_message = 'Appointment successfully updated.'


class AppointmentDeleteView(DeleteView):
    """Prompts users to confirm deletion of an appointment"""

    model = Appointment
    success_url = reverse_lazy('list_appointments')



# API
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework import generics,permissions
from .permisssions import IsOwnerOrReadOnly

class AppointmentList(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = Appointment
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


from  .serializers import UserSerializer
# USER
from django.contrib.auth.models import User
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
@api_view(['POST'])
def create_auth(request):
    serialized = UserSerializer(data=request.data)
    email=request.data['email']

    if serialized.is_valid():

        User.objects.create_user(
            request.data['username'],
            request.data['email'],
            request.data['password']
        )
        # User.objects.create_user(
        #     serialized.init_data['email'],
        #     serialized.init_data['username'],
        #     serialized.init_data['password']
        # )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)