from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import customer_required
from ..forms import CustomerInterestsForm, CustomerSignUpForm
from ..models import Room, Customer, TakenRoom, User


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customers:room_list')


@method_decorator([login_required, customer_required], name='dispatch')
class CustomerInterestsView(UpdateView):
    model = Customer
    form_class = CustomerInterestsForm
    template_name = 'hotel/customers/interests_form.html'
    success_url = reverse_lazy('customers:quiz_list')

    def get_object(self):
        return self.request.user.customer

    def form_valid(self, form):
        messages.success(self.request, 'Interests updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, customer_required], name='dispatch')
class RoomListView(ListView):
    model = Room
    ordering = ('name', )
    context_object_name = 'rooms'
    template_name = 'hotel/customers/room_list.html'

    def get_queryset(self):
        customer = self.request.user.customer
        customer_interests = customer.interests.values_list('pk', flat=True)
        taken_rooms = customer.rooms.values_list('pk', flat=True)
        queryset = Room.objects.filter(roomnumber__in=customer_interests) \
            .exclude(pk__in=taken_rooms) \


@method_decorator([login_required, customer_required], name='dispatch')
class TakenRoomListView(ListView):
    model = TakenRoom
    context_object_name = 'taken_rooms'
    template_name = 'hotel/customers/taken_room_list.html'

    def get_queryset(self):
        queryset = self.request.user.customer.taken_rooms \
            .select_related('room', 'room__rooomnumber') \
            .order_by('room__name')
        return queryset



