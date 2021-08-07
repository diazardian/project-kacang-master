from django.db.models import fields
from rest_framework import serializers
from .models import *


class Discord_MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = tMember_Discord
        fields = "__all__"


class Member_GuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = tGuild_Discord
        fields = "__all__"


class Guild_ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = tGuild_Channel
        fields = "__all__"
