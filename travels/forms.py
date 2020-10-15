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

    def __str__(self):
        return self.username    

class SrcDestForm(forms.Form):
    source = forms.ChoiceField(choices = [
        ('Delhi','Delhi'),
        ('Mumbai','Mumbai'),
        ('Jaipur','Jaipur'),
        ('Kolkata','Kolkata'),
        ('Hyderabad','Hyderabad')
    ])
    destination = forms.ChoiceField(choices = [
        ('Delhi','Delhi'),
        ('Mumbai','Mumbai'),
        ('Jaipur','Jaipur'),
        ('Kolkata','Kolkata'),
        ('Hyderabad','Hyderabad')
    ])
    date = forms.DateField(widget = forms.widgets.DateInput(attrs = {'type': 'date'}))

class BookingForm(forms.Form):
    passenger1 = forms.CharField(required=True)
    age1 = forms.IntegerField(required=True)
    passenger2 = forms.CharField(required=False)
    age2 = forms.CharField(required=False)
    passenger3 = forms.CharField(required=False)
    age3 = forms.CharField(required=False)
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$', error_messages={"invalid": "Enter a valid number"},required=True)
    email = forms.EmailField(required=True)   
    finalDest = forms.CharField(required=True)
