from django.db import models

class SteamGames(models.Model):
    json_response = models.TextField()
    app_id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    TTL = models.DateTimeField(auto_now=False, auto_now_add=False)