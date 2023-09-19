from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

# Create your views here.
def logout(request):
    auth_logout(request)
    return redirect ('/')

def createNewUser(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    else:
        if request.method == 'POST':
            try:
                first_name = request.POST.get('first_name').strip()
                last_name = request.POST.get('last_name').strip()
                email = request.POST.get('email').strip()
                password = request.POST.get('password').strip()
                phone = request.POST.get('phone').strip()
                dob = request.POST.get('dob').strip()
                gender = request.POST.get('gender').strip()
                address = request.POST.get('address').strip()

                fields = [first_name, last_name, email, password, phone, dob, gender, address]
                
                #Validating user info
                if len(password) < 6:
                    return render(request, 'accounts/createuser.html',{'error':'Password should be at least 6 characters.', 'activetab': 'createuser', 'fields': fields})
                if list(User.objects.filter(email=email)) != []:
                    return render(request, 'accounts/createuser.html',{'error':'Email already exists.', 'activetab': 'createuser', 'fields': fields})
                if len(phone) == 0:
                    return render(request, 'accounts/createuser.html', {'error':'Phone number cannot be empty.', 'activetab': 'createuser', 'fields': fields})
                if list(User.objects.filter(phone=phone)) != []:
                    return render(request, 'accounts/createuser.html', {'error':'Phone number already exists.', 'activetab': 'createuser', 'fields': fields})
                try:
                    dob = datetime.strptime(dob, '%Y-%m-%d').date()
                    if dob > datetime.now().date():
                        return render(request, 'accounts/createuser.html', {'error':'Enter correct date of birth.', 'activetab': 'createuser', 'fields': fields})
                except:
                    return render(request, 'accounts/createuser.html', {'error':'Enter correct date of birth.', 'activetab': 'createuser', 'fields': fields})

                #Creating the user            
                user = User.objects.create_superuser(email=email, password=password, phone=phone)
                user.first_name = first_name
                user.last_name = last_name
                user.dob = dob
                user.gender = gender
                user.address = address
                user.save()
                request.session['success'] = 'Account Created Successfully'
                return redirect('/')
            except:
                return render(request, 'accounts/createuser.html',{'error':'Fill out all the fields correctly.', 'activetab': 'createuser', 'fields': fields})
        else:
            return render(request, 'accounts/createuser.html', {'activetab': 'createuser'})

def login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                user = authenticate(email = email, password = password)
            except:
                user = None
            if user:
                auth_login(request, user)
                return redirect('/dashboard/')
            else:
                return render(request, 'accounts/login.html', {'error':'Invalid email or password!', 'activetab': 'login'})
        else:
            if request.session.get('success') != None:
                success = request.session.get('success')
                request.session['success'] = None
            else:
                success = ''
            return render(
                request, 
                'accounts/login.html', 
                {
                    'message':'',
                    'success':success,
                    'activetab': 'login',
                }
                )
