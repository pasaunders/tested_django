"""Form for adding new trip."""

from django import forms
from django.contrib.auth.models import User
from .models import Trip
from django.forms.fields import DateField
from datetime import date


class NewTripForm(forms.ModelForm):
    date_from = forms.DateField(label='Travel Date From', widget=forms.SelectDateWidget)
    date_to = forms.DateField(label='Travel Date To', widget=forms.SelectDateWidget)

    class Meta:
        model = Trip
        fields = ['destination', 'description', 'date_from', 'date_to']


    def clean(self):
        cleaned_data = super(NewTripForm, self).clean()
        first_date = cleaned_data.get('date_from')
        second_date = cleaned_data.get('date_to')


        if second_date < first_date:
            raise forms.ValidationError('End date may not be before start date.')
        elif first_date < date.today():
            raise forms.ValidationError('Dates must not be in the past.')