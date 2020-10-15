from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta: #it shows which model to interact with when we do form.save() in views.py it saves in User model and fields show in which order to be displayed on form
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ] 

class SrcDestForm(forms.Form):
    source = forms.ChoiceField(choices = [
        ('delhi','Delhi'),
        ('mumbai','Mumbai'),
        ('jaipur','Jaipur'),
        ('kolkata','Kolkata'),
        ('hyderabad','Hyderabad')
    ])
    destination = forms.ChoiceField(choices = [
        ('delhi','Delhi'),
        ('mumbai','Mumbai'),
        ('jaipur','Jaipur'),
        ('kolkata','Kolkata'),
        ('hyderabad','Hyderabad')
    ])
    date = forms.DateField(widget = forms.widgets.DateInput(attrs = {'type': 'date'}))