from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import employer_required
from ..forms import  EmployerSignUpForm
from ..models import Room, User


class EmployerSignUpView(CreateView):
    model = User
    form_class = EmployerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('employers:room_change_list')


@method_decorator([login_required, employer_required], name='dispatch')
class RoomListView(ListView):
    model = Room
    ordering = ('name', )
    context_object_name = 'rooms'
    template_name = 'hotel/employers/room_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.rooms \
            .select_related('roomnumber') \
            .annotate(taken_count=Count('taken_rooms', distinct=True))
        return queryset


@method_decorator([login_required, employer_required], name='dispatch')
class RoomCreateView(CreateView):
    model = Room
    fields = ('name', 'roomnumber', )
    template_name = 'hotel/employers/room_add_form.html'

    def form_valid(self, form):
        room = form.save(commit=False)
        room.owner = self.request.user
        room.save()
        messages.success(self.request, 'The room was created with success!.')
        return redirect('employers:room_change', room.pk)


@method_decorator([login_required, employer_required], name='dispatch')
class RoomUpdateView(UpdateView):
    model = Room
    fields = ('name', 'roomnumber', )
    context_object_name = 'room'
    template_name = 'hotel/employers/room_change_form.html'

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing roomss that belongs
        to the logged in user.
        '''
        return self.request.user.roomss.all()

    def get_success_url(self):
        return reverse('employers:room_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, employer_required], name='dispatch')
class RoomDeleteView(DeleteView):
    model = Room
    context_object_name = 'room'
    template_name = 'hotel/employers/room_delete_confirm.html'
    success_url = reverse_lazy('employers:room_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The room %s was deleted with success!' % room.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.rooms.all()


@method_decorator([login_required, employer_required], name='dispatch')
class RoomResultsView(DetailView):
    model = Room
    context_object_name = 'room'
    template_name = 'hotel/employers/room_results.html'

    def get_context_data(self, **kwargs):
        room = self.get_object()
        taken_rooms = room.taken_rooms.select_related('customer__user').order_by('-date')
        total_taken_rooms = taken_rooms.count()
        extra_context = {
            'taken_roomss': taken_roomss,
            'total_taken_rooms': total_taken_rooms,
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.rooms.all()

