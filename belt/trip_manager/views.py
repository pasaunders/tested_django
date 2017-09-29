from django.shortcuts import render

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Trip
from .forms import NewTripForm


class ListTrips(LoginRequiredMixin, View):
    login_required = True
    login_url = reverse_lazy('login:signin')

    def get(self, request):
        context = {
            'user_trips': [x for x in Trip.objects.filter(
                planner=self.request.user)] 
                + [x for x in Trip.objects.filter(guests=self.request.user)],
            'other_trips': [x for x in Trip.objects.exclude(
                planner=self.request.user).exclude(guests=self.request.user
                )],
            'person': self.request.user.first_name,
        }
        return render(request, 'trip_manager/index.html', context)


class TripDetail(LoginRequiredMixin, DetailView):
    login_required = True
    login_url = reverse_lazy('login:signin')
    model = Trip


class NewTrip(LoginRequiredMixin, CreateView):
    login_required = True
    login_url = reverse_lazy('login:signin')
    form_class = NewTripForm
    template_name = 'trip_manager/new_trip.html'
    success_url = reverse_lazy('travel:list')

    def form_valid(self, form):
        form.instance.planner = self.request.user
        return super(NewTrip, self).form_valid(form)


class JoinTrip(LoginRequiredMixin, View):
    login_required = True
    login_url = reverse_lazy('login:signin')
    def get(self, request, pk):
        trip = Trip.objects.get(id=pk)
        trip.guests.add(self.request.user)
        trip.save()
        # import pdb; pdb.set_trace()
        return redirect('travel:list')