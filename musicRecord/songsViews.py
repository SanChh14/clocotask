from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import Artist, Music
from django.db import connection

User = get_user_model()
current_year = str(datetime.now())[:4]

def user_name(request):
    return request.user.first_name.upper()+' '+request.user.last_name.upper()

def artist_songs(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
        page_end = page*8
        page_start = page_end - 8
        # songs = Music.objects.all().filter(artist_id=pk).order_by('-created_at')
        songs = Music.objects.raw(f'select * from musicRecord_Music where artist_id={pk} order by created_at desc')
        pages = int(len(songs)/8)
        if len(songs)%8 != 0:
            pages = pages+1
        return render(request, 
                      'songs/artistsongs.html',
                      {'user_name':user_name(request), 
                       'songs':songs[page_start:page_end], 
                       'pages':range(1,pages+1), 
                       'page':page, 
                       'artist_id':pk,
                       }
                       )
    
def song_detail(request, pk=None, spk=None):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        try:
            # song = Music.objects.get(pk=spk)
            song = Music.objects.raw(f'select * from musicRecord_Music where id={spk} LIMIT 1')[0]
        except:
            song = None
        try:
            page = request.GET.get('page')
        except:
            page = None
        return render(request, 'songs/songdetail.html', {'user_name':user_name(request), 'page':page, 'song':song})
    
def add_song(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            try:
                try:
                    artist = Artist.objects.get(pk=pk)
                except:
                    return render(request, 'songs/addsong.html',{'user_name':user_name(request), 'error':'Artist Not Found.', 'artist_id':pk})
                title = request.POST.get('title').strip()
                album_name = request.POST.get('album_name').strip()
                genre = request.POST.get('genre').strip()
           
                fields = [title, album_name, genre]
                
                #Validating artist info
                if len(title)==0 or len(album_name)==0 or len(genre)==0:
                    return render(request, 'songs/addsong.html',{'user_name':user_name(request), 'error':'No field should be empty.', 'fields': fields, 'artist_id':pk})
                if genre not in ['rnb', 'country', 'classic', 'rock', 'jazz']:
                    return render(request, 'songs/addsong.html',{'user_name':user_name(request), 'error':'Invalid Genre.', 'fields': fields, 'artist_id':pk})
                #Creating song using ORM as Artist itself is a foreign key
                song = Music.objects.create(artist=artist, title=title, album_name=album_name, genre=genre)
                song.save()

                request.session['success'] = 'Song Added Successfully.'
                redirecturl = '/dashboard/artists/'+str(pk)+'/addnewsong/'
                return redirect(redirecturl)
            except Exception as e:
                print(e)
                return render(request, 'songs/addsong.html',{'user_name':user_name(request), 'error':'Fill out all the fields correctly.', 'fields': fields, 'artist_id':pk})
        else:
            if request.session.get('success') != None:
                success = request.session.get('success')
                request.session['success'] = None
            else:
                success = ''
            return render(request, 'songs/addsong.html', {'user_name':user_name(request), 'success':success, 'artist_id':pk})

def modify_songs(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1
        page_end = page*8
        page_start = page_end - 8
        # songs = Music.objects.all().filter(artist_id=pk).order_by('-created_at')
        songs = Music.objects.raw(f'select * from musicRecord_Music where artist_id={pk} order by created_at desc')
        pages = int(len(songs)/8)
        if len(songs)%8 != 0:
            pages = pages+1
        if request.session.get('success') != None:
                success = request.session['success'] 
                request.session['success'] = None
        else:
            success = ''
        return render(request, 
                      'songs/modifysong.html',
                      {'user_name':user_name(request), 
                       'songs':songs[page_start:page_end], 
                       'pages':range(1,pages+1), 
                       'page':page, 
                       'artist_id':pk,
                       'success':success
                       }
                       )
    
def update_song(request, pk=None, spk=None):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        try:
            page = request.GET.get('page')
        except:
            page = ''
        if request.method == 'POST':
            try:
                try:
                    delete = request.POST.get('delete').strip()
                    if delete == 'yes':
                        # song = Music.objects.get(pk=int(spk))
                        # song.delete()

                        #Deleting using raw query
                        sql_query = """
                            DELETE FROM musicRecord_Music
                            WHERE id = %s
                        """
                        value = spk
                        with connection.cursor() as cursor:
                            cursor.execute(sql_query, [value])
                        
                        request.session['success'] = 'Song deleted successfully.'
                        redirecturl = '/dashboard/artists/'+str(pk)+'/modifysong/'
                        return redirect(redirecturl)
                except:
                    pass
                try:
                    artist = Artist.objects.get(pk=pk)
                except:
                    return render(request, 'songs/updatesong.html',{'user_name':user_name(request), 'error':'Artist Not Found.', 'artist_id':pk, 'page':page})
                title = request.POST.get('title').strip()
                album_name = request.POST.get('album_name').strip()
                genre = request.POST.get('genre').strip()
           
                fields = [title, album_name, genre]
                
                #Validating artist info
                if len(title)==0 or len(album_name)==0 or len(genre)==0:
                    return render(request, 'songs/updatesong.html',{'user_name':user_name(request), 'error':'No field should be empty.', 'fields': fields, 'artist_id':pk, 'page':page})
                if genre not in ['rnb', 'country', 'classic', 'rock', 'jazz']:
                    return render(request, 'songs/updatesong.html',{'user_name':user_name(request), 'error':'Invalid Genre.', 'fields': fields, 'artist_id':pk, 'page':page})
                #Updating song using ORM
                # song = Music.objects.get(pk=spk)
                # song.title = title
                # song.album_name = album_name
                # song.genre = genre
                # song.updated_at = datetime.now()
                # song.save()

                #Updating song using raw query
                sql_query = """
                    UPDATE musicRecord_Music
                    SET title = %s, album_name = %s, genre = %s, updated_at = %s
                    WHERE id = %s
                """

                values = [title, album_name, genre, datetime.now(), spk]

                with connection.cursor() as cursor:
                    cursor.execute(sql_query, values)
                
                success = 'Info Updated Successfully.'
                return render(request, 'songs/updatesong.html',{'user_name':user_name(request), 'success':success, 'fields': fields, 'artist_id':pk, 'page':page})
            except:
                return render(request, 'songs/updatesong.html',{'user_name':user_name(request), 'error':'Fill out all the fields correctly.', 'fields': fields, 'artist_id':pk, 'page':page})
        else:
            try:
                # song = Music.objects.get(pk=spk)
                song = Music.objects.raw(f'select * from musicRecord_Music where id={spk} LIMIT 1')[0]
                fields = [song.title, song.album_name, song.genre]
            except:
                return render(request, 'songs/updatesong.html', {'user_name':user_name(request), 'artist_id':pk, 'error':'Song not found.', 'page':page})
            return render(request, 'songs/updatesong.html', {'user_name':user_name(request), 'artist_id':pk, 'fields': fields, 'page':page})