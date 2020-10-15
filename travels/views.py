from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserRegisterForm,SrcDestForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.contrib import messages

def indexView(request):
    # if request.user.is_authenticated:
    #     return redirect('travels:dashboard')
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)   #created a from with values that we filled
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created!')
            return redirect('travels:login')
    else:
        form = UserRegisterForm() #creates a form
    return render(request, 'register.html', {'form': form}) 

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('travels:dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect!')
            return redirect('travels:login')
    
    return render(request, 'login.html')


@login_required
def dashboard(request):
    if request.method == 'POST':
        src = request.POST.get('source')
        dest = request.POST.get('destination')
        if src==dest:
            messages.info(request, 'Source and Destination cannot be same!')
            return redirect('travels:dashboard')
    form = SrcDestForm()

    return render(request, 'dashboard.html',{'form':form})