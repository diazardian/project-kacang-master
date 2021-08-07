from kacang.viewsets import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register("DiscordMember", Discord_MemberViewset)
router.register("MemberGuild", Member_GuildViewset)
router.register("GuildChannel", Guild_ChannelViewset)
