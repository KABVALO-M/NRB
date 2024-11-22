from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CitizenForm, DeceasedCitizenForm  
from .models import User, Citizen, DeceasedCitizen
from django.core import serializers
from django.db.models import Q
import requests
from django.utils import timezone
from datetime import timedelta

def home_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  
    else:
        return redirect('login')  

@login_required
def dashboard_view(request):
    # Statistics
    total_citizens = Citizen.objects.count()
    total_deceased = DeceasedCitizen.objects.count()
    total_users = User.objects.count()
    
    # Recent activities (for simplicity, this could be expanded with actual activity logs)
    recent_citizen_registrations = Citizen.objects.filter(date_of_birth__gte=timezone.now() - timedelta(days=30)).order_by('-date_of_birth')[:5]
    recent_deceased_registrations = DeceasedCitizen.objects.filter(date_of_death__gte=timezone.now() - timedelta(days=30)).order_by('-date_of_death')[:5]

    context = {
        'total_citizens': total_citizens,
        'total_deceased': total_deceased,
        'total_users': total_users,
        'recent_citizen_registrations': recent_citizen_registrations,
        'recent_deceased_registrations': recent_deceased_registrations,
    }

    return render(request, 'core/dashboard.html', context)

@login_required
def users_view(request):
    
    users = User.objects.all()
    return render(request, 'core/users/users.html', {'users': users})  

@login_required
def add_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user)  
            return redirect('users')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/users/add_user.html', {'form': form})

@login_required
def edit_user_view(request, user_id):
    pass

@login_required
def delete_user_view(request, user_id): 
    pass

@login_required
def citizens_view(request):
    citizens = Citizen.objects.exclude(Q(deceasedcitizen__isnull=False))
    return render(request, 'core/citizens/citizens.html', {'citizens': citizens})  


@login_required
def add_citizen_view(request):
    if request.method == 'POST':
        form = CitizenForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('citizens')  
    else:
        form = CitizenForm()
    return render(request, 'core/citizens/add_citizen.html', {'form': form})


@login_required
def edit_citizen_view(request, citizen_id):
    citizen = get_object_or_404(Citizen, id=citizen_id)
    if request.method == 'POST':
        form = CitizenForm(request.POST, instance=citizen)
        if form.is_valid():
            form.save()
            return redirect('citizens')  
    else:
        form = CitizenForm(instance=citizen)
    return render(request, 'core/citizens/edit_citizen.html', {'form': form})



@login_required
def delete_citizen_view(request, citizen_id):
    citizen = get_object_or_404(Citizen, id=citizen_id)
    if request.method == 'POST':
        citizen.delete()
        return redirect('citizens')  
    return render(request, 'core/citizens/delete_citizen_confirm.html', {'citizen': citizen})


@login_required
def deceased_citizens_view(request):
    deceased_citizens = DeceasedCitizen.objects.all()  
    return render(request, 'core/deceased_citizens/deceased_citizens.html', {'deceased_citizens': deceased_citizens})

@login_required
def add_deceased_citizen_view(request):
    if request.method == 'POST':
        form = DeceasedCitizenForm(request.POST)
        if form.is_valid():
            national_id = form.cleaned_data['national_id']
            try:  
                citizen = Citizen.objects.get(national_id=national_id) 
                deceased_citizen = DeceasedCitizen(
                    citizen=citizen,
                    date_of_death=form.cleaned_data['date_of_death'],
                    cause_of_death=form.cleaned_data['cause_of_death']
                )
                deceased_citizen.save()
                data = {
                    'national_id': deceased_citizen.citizen.national_id,
                    'full_name': deceased_citizen.citizen.full_name,
                    'date_of_birth': str(deceased_citizen.citizen.date_of_birth),
                    'date_of_death': str(deceased_citizen.date_of_death),
                    'cause_of_death': deceased_citizen.cause_of_death,
                }
                try:
                    response = requests.post('http://127.0.0.1:8001/api/add-deceased-citizen/', json=data)
                    response.raise_for_status()   
                    messages.success(request, "Deceased citizen added and synced with external system.")

                except requests.exceptions.RequestException as e:  
                    messages.error(request, f"Error syncing with external system: {e}")

                return redirect('deceased_citizens')

            except Citizen.DoesNotExist:
                
                form.add_error('national_id', 'Citizen with this National ID does not exist.')
    else:
        form = DeceasedCitizenForm()

    citizens = Citizen.objects.filter(deceasedcitizen__isnull=True)
    serialized_citizens = serializers.serialize('json', citizens)

    return render(request, 'core/deceased_citizens/add_deceased_citizen.html', {
        'form': form,
        'citizens': serialized_citizens  
    })

@login_required
def edit_deceased_citizen_view(request, id):
    deceased_citizen = get_object_or_404(DeceasedCitizen, id=id)
    if request.method == 'POST':
        form = DeceasedCitizenForm(request.POST, instance=deceased_citizen)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deceased citizen updated successfully!')
            return redirect('deceased_citizens')
        else:
            messages.error(request, 'Error updating deceased citizen. Please check the form.')
    else:
        form = DeceasedCitizenForm(instance=deceased_citizen)

    return render(request, 'core/deceased_citizens/edit_deceased_citizen.html', {'form': form})

@login_required
def delete_deceased_citizen_view(request, id):
    deceased_citizen = get_object_or_404(DeceasedCitizen, id=id)
    if request.method == 'POST':
        deceased_citizen.delete()
        messages.success(request, 'Deceased citizen deleted successfully!')
        return redirect('deceased_citizens')
    return render(request, 'core/deceased_citizens/delete_deceased_citizen_confirm.html', {'deceased_citizen': deceased_citizen})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')  


def logout_view(request):
    logout(request)
    return redirect('login')  
