from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserRegisterForm,SrcDestForm,BookingForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User

from datetime import datetime

from .safeApi import get_available_seats, book_ticket, get_history

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
        date = request.POST.get('date')
        
        if src==dest:
            messages.info(request, 'Source and Destination cannot be same!')
            return redirect('travels:dashboard')

        if date < str(datetime.now().date()):
            messages.info(request, 'Enter valid booking date')
            return redirect('travels:dashboard')            

        return redirect('travels:booking', src=src, dest=dest, date=date)
    form = SrcDestForm()

    return render(request, 'dashboard.html', {'form':form})

@login_required
def booking(request, src, dest, date):
    seatsA = get_available_seats(src, dest, src+'-'+dest+'-Express', date)
    seatsB = get_available_seats(src, dest, src+'-'+dest+'-Superfast', date)
    seatsC = get_available_seats(src, dest, src+'-'+dest+'-GaribRath', date)

    context = {
        'src': src,
        'dest': dest,
        'date': date,
        'seatsA': seatsA,
        'seatsB': seatsB,
        'seatsC': seatsC,
        'trainA': src+'-'+dest+'-Express',
        'trainB': src+'-'+dest+'-Superfast',
        'trainC': src+'-'+dest+'-GaribRath',
    }
    return render(request, 'booking.html', context)


@login_required
def bookingDetails(request, src,dest,train,date):
    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            passenger1 = request.POST.get('passenger1')
            passenger2 = request.POST.get('passenger2')
            passenger3 = request.POST.get('passenger3')
            age1 = request.POST.get('age1')
            age2 = request.POST.get('age2')
            age3 = request.POST.get('age3')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            finalDest = request.POST.get('finalDest')

            formDetails = [{
                'name': passenger1,
                'age': age1,
                'email': email,
                'contact': phone,
                'final_des': finalDest,
                'userId': request.user.username
            }]

            if passenger2:
                dict2 = {
                    'name': passenger2,
                    'age': age2,
                    'email': email,
                    'contact': phone,
                    'final_des': finalDest,
                    'userId': request.user.username
                }
                formDetails.append(dict2)

            if passenger3:
                dict3 = {
                    'name': passenger3,
                    'age': age3,
                    'email': email,
                    'contact': phone,
                    'final_des': finalDest,
                    'userId': request.user.username
                }
                formDetails.append(dict3) 

            ticket = book_ticket(src, dest, train, date, formDetails)
            print(ticket)       

    form = BookingForm()
    return render(request, 'detail.html', {'form': form})  

@login_required
def bookingHistory(request):
    histories = get_history(request.user.username)
    print(histories)

    return render(request, 'history.html', {'histories': histories})
