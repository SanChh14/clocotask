from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'dashboard.html', {})