from rest_framework import viewsets, permissions
from . import models
from . import serializers


class Discord_MemberViewset(viewsets.ModelViewSet):
    queryset = models.tMember_Discord.objects.all()
    serializer_class = serializers.Discord_MemberSerializer
    # permission_classes = [permissions.IsAuthenticated]


class Member_GuildViewset(viewsets.ModelViewSet):
    queryset = models.tGuild_Discord.objects.all()
    serializer_class = serializers.Member_GuildSerializer
    # permission_classes = [permissions.IsAuthenticated]

class Guild_ChannelViewset(viewsets.ModelViewSet):
    queryset = models.tGuild_Channel.objects.all()
    serializer_class = serializers.Guild_ChannelSerializer