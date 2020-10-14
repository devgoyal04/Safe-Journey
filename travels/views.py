from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def indexView(request):
    return render(request,'base.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('travels:index')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)   #created a from with values that we filled
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created!You are now able to login!')
            return redirect('travels:login')
    else:
        form = UserRegisterForm() #creates a form
    return render(request, 'register.html', {'form': form}) 

@login_required
def dashboard(request):
    return HttpResponse("<h1>Logged In!</h1>")