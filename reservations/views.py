from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import calendar
from datetime import datetime
from babel.dates import format_date
from babel import Locale
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
    locale = Locale('pt', 'BR')
    
    for month in available_months:
        month_name = format_date(datetime(current_date.year, month, 1), "MMMM", locale=locale)
        _, num_days = calendar.monthrange(current_date.year, month)
        days = [day for day in range(1, num_days + 1)]
        
        month_data = {
            'month_name': month_name.title(),
            'days': days
        }
        calendars.append(month_data)
    
    return calendars

@login_required(login_url='/')
def calendar_view(request):
    calendars = generate_calendar()
    
    all_reservations = Reservation.objects.all()

    all_dates = []

    for reservation in all_reservations:
        all_dates.append(reservation.event_date)
    
    context = {
        'calendars': calendars,
        'done_reservations': all_dates,
    }
    return render(request, 'calendar.html', context)

@login_required(login_url='/')
def edit_user(request):
    user = User.objects.get(username=request.user.username) 
    
    context = {
        'user': user
    }
    
    return render(request, 'edit_user.html', context)

def submit_user(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        user = User.objects.get(id=user_id)
        
        calendars = generate_calendar()
        
        if first_name or last_name:
            user.first_name = first_name
            user.last_name = last_name
        
        if password:
            user.set_password(password)
            
        user.save()
        
        context = {
            'user': user
        }
        
        
        return render(request, 'edit_user.html', context)

    else:
        return render(request, 'edit_user.html', context)

@login_required(login_url='/')
def edit_reservations(request):
    if request.method == "POST":
        event_day = request.POST.get('event_day')
        event_month = request.POST.get('event_month')
        reservation_date = datetime.now().date()
        calendars = generate_calendar()
        
        context = {
            'event_day': event_day,
            'event_month': event_month,
            'reservation_date': reservation_date,
            'calendars': calendars
        }
        return render(request, 'edit_reservations.html', context)

def submit_reservation(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        event_day = request.POST.get('event_day')
        event_month = request.POST.get('event_month')
        event_year = datetime.now().year
        reservation_date = request.POST.get('reservation_date')
        
        month_map = {
            'Janeiro': 1,
            'Fevereiro': 2,
            'Março': 3,
            'Abril': 4,
            'Maio': 5,
            'Junho': 6,
            'Julho': 7,
            'Agosto': 8,
            'Setembro': 9,
            'Outubro': 10,
            'Novembro': 11,
            'Dezembro': 12,
        }
    
        event_month_num = month_map.get(event_month)
        event_date = datetime.strptime(f"{event_year} {event_month_num} {event_day}", "%Y %m %d").date()
        
        user = User.objects.get(id=user_id)
        
        reservation = Reservation(user=user, event_date=event_date, reservation_date=reservation_date)
        reservation.save()
        
        messages.success(request, 'Reserva feita com sucesso.')
        return redirect('/calendar/')  
        
    return redirect('/edit_reservations')

@login_required(login_url='/')
def my_reservations(request):
    user_reservations = Reservation.objects.filter(user=request.user)
    user = User.objects.get(id=request.user.id)
    
    context = {
        'user_reservations': user_reservations.order_by('event_date'),
        'user': user
    }
    
    return render(request, 'my_reservations.html', context)
    

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def custom_logout(request):
    logout(request)
    return render(request, 'index.html')