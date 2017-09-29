"""Forms for gathering login and registration information."""


from django import forms

from django.contrib.auth.models import User


class register_form(forms.ModelForm):
    password = forms.CharField(label='Password:', min_length=8, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password:', widget=forms.PasswordInput())
    first_name = forms.CharField(label='Name')
    username = forms.CharField()
    # first_name = forms.CharField(label='Name', min_length=3)
    # username = forms.CharField(min_length=3)

    class Meta:
        model = User
        fields = ['first_name', 'username', 'password']


    def clean(self):
        cleaned_data = super(register_form, self).clean()
        password = cleaned_data.get('password')
        username = cleaned_data.get('username')
        confirm_password = cleaned_data.get('confirm_password')
        first_name = cleaned_data.get('first_name')

        if password != confirm_password:
            raise forms.ValidationError('Password and confirmaiton must match.')
        if len(password) < 8:
            raise forms.ValidationError('Password must be 8 or more characters.')
        if len(username) < 3 or len(first_name) < 3:
            raise forms.ValidationError('Name and username must be three or more characters.')

class signin_form(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password:', widget=forms.PasswordInput())
