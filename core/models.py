from django.db import models

class SteamGames(models.Model):
    name_of_game = models.CharField(max_length=50)