from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

def user_name(request):
    return request.user.first_name.upper()+' '+request.user.last_name.upper()

def show_all_users(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
        page_end = page*8
        page_start = page_end - 8
        users = User.objects.all().order_by('-created_at')
        pages = int(len(users)/8)
        if len(users)%8 != 0:
            pages = pages+1
        return render(request, 'users/allusers.html',{'user_name':user_name(request) ,'users':users[page_start:page_end], 'pages':range(1,pages+1), 'page':page})

def user_detail(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        try:
            user = User.objects.get(pk = pk)
        except:
            user = None
        try:
            page = request.GET.get('page')
        except:
            page = None
        return render(request, 'users/userdetail.html', {'user_name':user_name(request), 'user':user, 'page':page})

def create_user(request):
    if not request.user.is_authenticated:
        return redirect('/')
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
                    return render(request, 'users/createuser.html',{'user_name':user_name(request), 'error':'Password should be at least 6 characters.', 'activetab': 'createuser', 'fields':fields})
                if list(User.objects.filter(email=email)) != []:
                    return render(request, 'users/createuser.html',{'user_name':user_name(request), 'error':'Email already exists.', 'activetab': 'createuser', 'fields':fields})
                if len(phone) == 0:
                    return render(request, 'users/createuser.html', {'user_name':user_name(request), 'error':'Phone number cannot be empty.', 'activetab': 'createuser', 'fields':fields})
                if list(User.objects.filter(phone=phone)) != []:
                    return render(request, 'users/createuser.html', {'user_name':user_name(request), 'error':'Phone number already exists.', 'activetab': 'createuser', 'fields':fields})
                try:
                    dob = datetime.strptime(dob, '%Y-%m-%d').date()
                    if dob > datetime.now().date():
                        return render(request, 'users/createuser.html', {'user_name':user_name(request), 'error':'Enter correct date of birth.', 'activetab': 'createuser', 'fields':fields})
                except:
                    return render(request, 'users/createuser.html', {'user_name':user_name(request), 'error':'Enter correct date of birth.', 'activetab': 'createuser', 'fields':fields})

                #Creating the user 
                user = User.objects.create_superuser(email=email, password=password, phone=phone)
                user.first_name = first_name
                user.last_name = last_name
                user.dob = dob
                user.gender = gender
                user.address = address
                user.save()
                request.session['success'] = 'Account Created Successfully'
                return redirect('/dashboard/users/createnewuser/')
            except:
                return render(request, 'users/createuser.html',{'user_name':user_name(request), 'error':'Fill out all the fields correctly.', 'activetab': 'createuser', 'fields': fields})
        else:
            if request.session.get('success') != None:
                success = request.session.get('success')
                request.session['success'] = None
            else:
                success = ''
            return render(request, 'users/createuser.html', {'user_name':user_name(request), 'success':success})
        
def modify_user(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
        page_end = page*8
        page_start = page_end - 8
        users = User.objects.all().order_by('-created_at')
        pages = int(len(users)/8)
        if len(users)%8 != 0:
            pages = pages+1
        if request.session.get('success') != None:
                success = request.session['success'] 
                request.session['success'] = None
        else:
            success = ''
        return render(request, 'users/modifyuser.html',{'user_name':user_name(request) ,'users':users[page_start:page_end], 'pages':range(1,pages+1), 'page':page, 'success':success})

def update_user(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            try:
                try:
                    page = request.POST.get('page').strip()
                except:
                    page = None
                try:
                    delete = request.POST.get('delete').strip()
                    if delete == 'yes':
                        pk = request.POST.get('pk').strip()
                        user = User.objects.get(pk=int(pk))
                        user.delete()
                        request.session['success'] = 'User deleted successfully.'
                        return redirect('/dashboard/users/modifyuser/')

                except:
                    pass
                pk = request.POST.get('pk').strip()
                print(pk)
                first_name = request.POST.get('first_name').strip()
                last_name = request.POST.get('last_name').strip()
                email = request.POST.get('email').strip()
                password = request.POST.get('password').strip()
                phone = request.POST.get('phone').strip()
                dob = request.POST.get('dob').strip()
                gender = request.POST.get('gender').strip()
                address = request.POST.get('address').strip()
                fields = [first_name, last_name, email, password, phone, dob, gender, address, pk]
                
                #Validating user info
                if len(password) < 6 and password != '':
                    return render(request, 'users/updateuser.html',{'user_name':user_name(request), 'error':'Password should be at least 6 characters.', 'page': page, 'fields':fields})
                if list(User.objects.filter(email=email)) != []:
                    if User.objects.filter(email=email)[0].id != int(pk):
                        return render(request, 'users/updateuser.html',{'user_name':user_name(request), 'error':'Email already exists.', 'page': page, 'fields':fields})
                if len(phone) == 0:
                    return render(request, 'users/updateuser.html', {'user_name':user_name(request), 'error':'Phone number cannot be empty.', 'page': page, 'fields':fields})
                if list(User.objects.filter(phone=phone)) != []:
                    if User.objects.filter(phone=phone)[0].id != int(pk):
                        return render(request, 'users/updateuser.html',{'user_name':user_name(request), 'error':'Phone number already exists.', 'page': page, 'fields':fields})
                try:
                    dob = datetime.strptime(dob, '%Y-%m-%d').date()
                    if dob > datetime.now().date():
                        return render(request, 'users/updateuser.html', {'user_name':user_name(request), 'error':'Enter correct date of birth.', 'page': page, 'fields':fields})
                except:
                    return render(request, 'users/updateuser.html', {'user_name':user_name(request), 'error':'Enter correct date of birth.', 'page': page, 'fields':fields})

                #Updating the user 
                user = User.objects.get(pk=int(pk))
                user.email = email
                if password != '':
                    user.set_password(password)
                user.phone = phone
                user.first_name = first_name
                user.last_name = last_name
                user.dob = dob
                user.gender = gender
                user.address = address
                user.save()
                return render(request, 'users/updateuser.html',{'user_name':user_name(request), 'success':'Info Updated Successfully.','page': page, 'fields': fields})
            except:
                page = None
                fields = None
                return render(request, 'users/updateuser.html',{'user_name':user_name(request), 'error':'User not found.','page': page, 'fields': fields})
        else:
            error = ''
            try:
                user = User.objects.get(pk = pk)
                fields = [user.first_name, user.last_name, user.email, '', user.phone, str(user.dob), user.gender, user.address, user.id]
            except:
                user = None
                fields = None
                error = 'User not found.'
            try:
                page = request.GET.get('page')
            except:
                page = None
            return render(request, 'users/updateuser.html', {'user_name':user_name(request), 'user':user, 'page':page, 'fields': fields, 'error': error})