# Raymond Hernandez
# raymondhernandez@outlook.com
# June 11, 2024
# C:\Users\Owner\assettracker\main\views.py


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connections
from django.db.utils import OperationalError
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def main_view(request):
    return HttpResponse("Hello Raymond Hernandez!")


def home_view(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT * FROM `refurbs` WHERE 1")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    return render(request, 'main/home.html', {'rows': rows, 'columns': columns})


def is_admin(user):
    return user.is_superuser or user.has_perm('main.view_technician')


@login_required
def users_view(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("SELECT * FROM technicians WHERE 1")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    return render(request, 'main/users.html', {'rows': rows, 'columns': columns})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_privilege(request):
    if request.method == 'POST':
        tech_id = request.POST.get('update')
        new_privilege = request.POST.get(f'privilege-{tech_id}')
        Technician.objects.filter(id=tech_id).update(privilege=new_privilege)
    return redirect('/your-redirect-url/')


def is_admin(user):
    return user.is_superuser or user.has_perm('main.view_technician')


def login_view(request):
    db_conn = connections['default']
    connected = True
    try:
        db_conn.cursor()
    except OperationalError:
        connected = False

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'main/login.html', {'error': 'Invalid username or password', 'connected': connected})
    else:
        return render(request, 'main/login.html', {'connected': connected})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/login/')


def create_account_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                return render(request, 'main/create_account.html', {'error': 'Email already exists'})
            else:
                user = User.objects.create_user(username=email, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'main/create_account.html', {'error': 'Passwords do not match'})

    return render(request, 'main/create_account.html')


