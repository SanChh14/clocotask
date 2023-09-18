from django.db import models
    
class Artist(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    name = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.CharField(max_length=50)
    first_release_date = models.DateField(null=True, blank=True)
    no_of_albums_released = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def first_release_year(self):
        return self.first_release_date.year

    def __str__(self):
        return self.name
    
class Music(models.Model):
    GENRE_CHOICES = (
        ('rnb', 'Rhythm and Blues'),
        ('country', 'Country'),
        ('classic', 'Classic'),
        ('rock', 'Rock'),
        ('jazz', 'Jazz'),
    )
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    album_name = models.CharField(max_length=50)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def artist_id(self):
        return self.artist.id
    
    def __str__(self):
        return self.title+'('+self.album_name+')'

