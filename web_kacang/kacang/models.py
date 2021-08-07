from django.db import models
from django.db.models.deletion import CASCADE, PROTECT

# Create your models here.
class tMember_Discord(models.Model):
    id_discord = models.CharField(
        max_length=100, primary_key=True, null=False, unique=True
    )
    name = models.CharField(max_length=100)
    avatar = models.CharField(max_length=255)
    user_join = models.CharField(max_length=100)
    user_create = models.CharField(max_length=100)
    guild_id = models.ForeignKey("tGuild_Discord", on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class tGuild_Discord(models.Model):
    id_guild = models.CharField(
        max_length=100, primary_key=True, null=False, unique=True
    )
    name = models.CharField(max_length=100)
    channel_id = models.ForeignKey("tGuild_Channel", on_delete=CASCADE, null=True)

    def __str__(self):
        return self.name


class tGuild_Channel(models.Model):
    id_channel = models.CharField(
        max_length=100, primary_key=True, null=False, unique=True
    )
    name = models.CharField(max_length=100)
    status = models.IntegerField(null=True)

    def __str__(self):
        return self.name
