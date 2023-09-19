from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

def user_name(request):
    return request.user.first_name.upper()+' '+request.user.last_name.upper()

# Create your views here.
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'dashboard.html', {'user_name': user_name(request), 'activetab':'dashboard'})

    
def users(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        users = User.objects.all().order_by('-created_at')[:5]
        return render(request, 'users/users.html', {'activetab':'users', 'user_name': user_name(request), 'users': users})

    
def artists(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'artists/artists.html', {'activetab':'artists', 'user_name': user_name(request)})