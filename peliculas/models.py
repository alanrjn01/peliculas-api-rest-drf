from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    weight = models.FloatField()
    story = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=300)
    release_date = models.DateField(blank=True)
    rate = models.IntegerField()

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class CharacterMovie(models.Model):
    character_id = models.ForeignKey(Character, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "CharacterMovie"
        verbose_name_plural = "CharacterMovies"

    def __str__(self):
        return f'Movie: {self.movie_id} - Character: {self.character_id}'
