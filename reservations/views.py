from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import calendar
from datetime import datetime, timedelta
from .models import Reservation
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'index.html')

def submit_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        message = "Usuário ou senha incorretos."
        
        if user is not None:
            login(request, user)
            return redirect('/calendar') 
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return redirect('/')
        
    return redirect('/')


def generate_calendar():
    current_date = datetime.now()
    current_month = current_date.month
    available_months = [current_month + i for i in range(3)]
    
    calendars = []
    for month in available_months:
        month_name = calendar.month_name[month]
        _, num_days = calendar.monthrange(current_date.year, month)
        days = [day for day in range(1, num_days + 1)]
        
        month_data = {
            'month_name': month_name,
            'days': days
        }
        calendars.append(month_data)
    
    return calendars

@login_required(login_url='/')
def calendar_view(request):
    calendars = generate_calendar()
    context = {
        'calendars': calendars,
    }
    return render(request, 'calendar.html', context)

def edit_user(request):
    return render(request, 'edit_user.html')

@login_required(login_url='/')
def edit_reservations(request):
    if request.method == "POST":
        day = request.POST.get('day')
        month = request.POST.get('month')
        reservation_date = datetime.now().date()
        calendars = generate_calendar()
        
        context = {
            'event_day': day,
            'event_month': month,
            'reservation_date': reservation_date,
            'calendars': calendars
        }
        return render(request, 'edit_reservations.html', context)

def submit_reservation(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        event_date = request.POST.get('event_date')
        
        user = User.objects.get(id=user_id)
        
        reservation = Reservation(user=user, event_date=event_date)
        reservation.save()
        
        return redirect('/calendar/')  
        
    return redirect('/edit_reservations')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')