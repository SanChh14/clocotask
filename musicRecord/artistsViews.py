from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import Artist

User = get_user_model()
current_year = str(datetime.now())[:4]

def user_name(request):
    return request.user.first_name.upper()+' '+request.user.last_name.upper()

def show_all_artists(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
        page_end = page*8
        page_start = page_end - 8
        artists = Artist.objects.all().order_by('-created_at')
        pages = int(len(artists)/8)
        if len(artists)%8 != 0:
            pages = pages+1
        return render(request, 'artists/allartists.html',{'user_name':user_name(request), 'artists':artists[page_start:page_end], 'pages':range(1,pages+1), 'page':page})

def artist_detail(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        try:
            artist = Artist.objects.get(pk = pk)
        except:
            artist = None
        try:
            page = request.GET.get('page')
        except:
            page = None
        return render(request, 'artists/artistdetail.html', {'user_name':user_name(request), 'user':artist, 'page':page})

def create_artist(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            try:
                name = request.POST.get('name').strip()
                dob = request.POST.get('dob').strip()
                gender = request.POST.get('gender').strip()
                address = request.POST.get('address').strip()
                first_release_year = str(request.POST.get('first_release_year')).strip()+'-01-01'
                no_of_albums_released = request.POST.get('no_of_albums_released')
           
                fields = [name, dob, gender, address, first_release_year[:4], no_of_albums_released]
                
                #Validating artist info
                try:
                    dob = datetime.strptime(dob, '%Y-%m-%d').date()
                    if dob > datetime.now().date():
                        return render(request, 'artists/createartist.html', {'user_name':user_name(request), 'error':'Enter correct date of birth.', 'current_year':current_year, 'fields':fields})
                except:
                    return render(request, 'artists/createartist.html', {'user_name':user_name(request), 'error':'Enter correct date of birth.', 'current_year':current_year, 'fields':fields})
                try:
                    first_release_year = datetime.strptime(first_release_year, '%Y-%m-%d').date()
                    if first_release_year > datetime.now().date():
                        return render(request, 'artists/createartist.html', {'user_name':user_name(request), 'error':'Enter correct first release year.', 'current_year':current_year, 'fields':fields})
                except:
                    return render(request, 'artists/createartist.html', {'user_name':user_name(request), 'error':'Enter correct first release year.', 'current_year':current_year, 'fields':fields})
                
                #Creating the user 
                user = Artist.objects.create(name = name, dob=dob)
                user.gender = gender
                user.address = address
                user.first_release_date = first_release_year
                user.no_of_albums_released = int(no_of_albums_released)
                user.save()
                request.session['success'] = 'Artist Added Successfully.'
                return redirect('/dashboard/artists/addnewartist/')
            except:
                return render(request, 'artists/createartist.html',{'user_name':user_name(request), 'error':'Fill out all the fields correctly.', 'current_year':current_year, 'fields': fields})
        else:
            if request.session.get('success') != None:
                success = request.session.get('success')
                request.session['success'] = None
            else:
                success = ''
            return render(request, 'artists/createartist.html', {'user_name':user_name(request), 'success':success, 'current_year':current_year})
        
def modify_artist(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
        page_end = page*8
        page_start = page_end - 8
        users = Artist.objects.all().order_by('-created_at')
        pages = int(len(users)/8)
        if len(users)%8 != 0:
            pages = pages+1
        if request.session.get('success') != None:
                success = request.session['success'] 
                request.session['success'] = None
        else:
            success = ''
        return render(request, 'artists/modifyartist.html',{'user_name':user_name(request), 'user_pk':request.user.id, 'users':users[page_start:page_end], 'pages':range(1,pages+1), 'page':page, 'success':success})

def update_artist(request, pk=None):
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
                        user = Artist.objects.get(pk=int(pk))
                        user.delete()
                        request.session['success'] = 'Artist deleted successfully.'
                        return redirect('/dashboard/artists/modifyartist/')

                except:
                    pass
                pk = request.POST.get('pk').strip()
                name = request.POST.get('name').strip()
                dob = request.POST.get('dob').strip()
                gender = request.POST.get('gender').strip()
                address = request.POST.get('address').strip()
                first_release_year = request.POST.get('first_release_year').strip()
                no_of_albums_released = request.POST.get('no_of_albums_released').strip()
                fields = [name, dob, gender, address, first_release_year, no_of_albums_released, pk]
                print(first_release_year)
                #Validating artist info
                try:
                    dob = datetime.strptime(dob, '%Y-%m-%d').date()
                    if dob > datetime.now().date():
                        return render(request, 'artists/updateartist.html', {'user_name':user_name(request), 'error':'Enter correct date of birth.', 'page': page, 'current_year':current_year,  'fields':fields})
                except:
                    return render(request, 'artists/updateartist.html', {'user_name':user_name(request), 'error':'Enter correct date of birth.', 'page': page, 'current_year':current_year,  'fields':fields})
                try:
                    first_release_year = datetime.strptime(first_release_year+'-01-01', '%Y-%m-%d').date()
                    if first_release_year > datetime.now().date():
                        return render(request, 'artists/updateartist.html', {'user_name':user_name(request), 'error':'Enter correct first release year.', 'current_year':current_year, 'fields':fields})
                except:
                    return render(request, 'artists/updateartist.html', {'user_name':user_name(request), 'error':'Enter correct first release year.', 'current_year':current_year, 'fields':fields})
                
                #Updating artist info
                user = Artist.objects.get(pk = int(pk))
                user.name = name
                user.dob = dob
                user.gender = gender
                user.address = address
                user.first_release_date = first_release_year
                user.no_of_albums_released = int(no_of_albums_released)
                user.save()
                return render(request, 'artists/updateartist.html',{'user_name':user_name(request), 'success':'Info Updated Successfully.','page': page, 'current_year':current_year, 'fields': fields})
            except:
                page = None
                fields = None
                return render(request, 'artists/updateartist.html',{'user_name':user_name(request), 'error':'Artist not found.','page': page,  'current_year':current_year, 'fields': fields})
        else:
            error = ''
            try:
                user = Artist.objects.get(pk = int(pk))
                fields = [user.name, str(user.dob), user.gender, user.address, user.first_release_year, user.no_of_albums_released, user.id]
            except:
                user = None
                fields = None
                error = 'User not found.'
            try:
                page = request.GET.get('page')
            except:
                page = None
            return render(request, 'artists/updateartist.html', {'user_name':user_name(request), 'user':user, 'page':page, 'fields': fields,  'current_year':current_year, 'error': error})