import discord
from discord.ext import commands
import json
import os
import random
import datetime
import asyncio
import requests
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from barcode import EAN13
from barcode.writer import ImageWriter
from urllib import request
from gtts import gTTS
from models import *

# os.chdir("E:\\DIaz\\WORK\\BOT\\project-kacang-master\\project-kacang")


class Users(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot Siap!")

    @commands.command()
    async def start(self, ctx):
        aidi = str(ctx.guild.id)
        name = ctx.guild.name
        if not Init().guild_register(aidi, name):
            await ctx.send("Server anda sudah terdaftar")
        else:
            await ctx.send(f"Server {ctx.guild.name} berhasil di daftarkan!")

    @commands.command()
    async def daftar(self, ctx):
        aidi = str(ctx.author.id)
        name = ctx.author.name
        avatar = str(ctx.author.avatar_url)
        user_join = str(ctx.author.joined_at)
        user_create = str(ctx.author.created_at)
        guild_id = str(ctx.guild.id)
        if not Init().member_register(
            aidi, name, avatar, user_join, user_create, guild_id
        ):
            await ctx.send(f"Anda sudah terdaftar pada game ini")
        else:
            await ctx.send(f"Anda berhasil mendaftar!")

    @commands.command()
    async def setup(self, ctx, channel: discord.TextChannel):
        aidi = str(channel.id)
        name = str(channel.name)
        status = 1
        if Init().setup(aidi, name, status):
            await ctx.send(f"Channel {channel.name} telah di set!")
        else:
            await ctx.send(f"Channel {channel.name} sudah di set sebelumnya!")

    @commands.command()
    async def profile(self, ctx):
        param_id = str(ctx.author.id)
        URL = f"http://127.0.0.1:8000/api/DiscordMember/{param_id}/"
        data = requests.get(url=URL).json()
        if data["detail"] == "Not found.":
            embed = discord.Embed(description="Data Tidak Ditemukan!")
            await ctx.send(embed=embed)
        else:
            user = ctx.author
            date_format = "%a, %d %b %Y %I:%M %p"
            embed = discord.Embed(
                title=f"Data Kependudukan Warga {ctx.guild.name}",
                color=0x00FF00,
                description="Data diri dari : " + user.mention,
            )
            # embed.set_author(name=str(user), icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(
                name="Bergabung di server ini",
                value=user.joined_at.strftime(date_format),
            )
            members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            # embed.add_field(name="Join position", value=str(members.index(user)+1))
            embed.add_field(
                name="Terdaftar di discord",
                value=user.created_at.strftime(date_format),
            )
            if len(user.roles) > 1:
                role_string = " ".join([r.mention for r in user.roles][1:])
            embed.add_field(
                name="Kekuasaan saat ini [{}]".format(len(user.roles) - 1),
                value=role_string,
                inline=False,
            )
            # perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
            # embed.add_field(name="Guild permissions", value=perm_string, inline=False)
            embed.set_footer(text="ID: " + str(user.id) + "| Created by Kacang Team")
            await ctx.send(embed=embed)

    @commands.command()
    async def ktp(self, ctx, *, user: discord.Member = None):
        await open_profil(ctx.author)
        users = await get_user_data()
        if user is None:
            user = ctx.author
        date_format = "%d %b %Y"
        users_id = str(user.id)

        ktp = Image.open("image/ktp/ktp.png")
        draw = ImageDraw.Draw(ktp)
        font_bold = ImageFont.truetype("image/font/Roboto-Bold.ttf", 24)
        font_nama = ImageFont.truetype("image/font/Roboto-Bold.ttf", 40)
        font_medium = ImageFont.truetype("image/font/Roboto-Medium.ttf", 14)
        font_req = ImageFont.truetype("image/font/Roboto-Regular.ttf", 20)
        font_kecil = ImageFont.truetype("image/font/Roboto-Thin.ttf", 12)

        judul = f"{ctx.guild.name} CITY"
        card_id = f"{users_id}\nCARD ID"

        nama = ctx.author.name
        nama = nama.upper()
        nama = f"{nama}\n"
        nama_sub = "NAME"

        nation = ctx.guild.name
        nation = nation.upper()
        nation = f"{nation}\nNATIONALITY"

        bod = user.created_at.strftime(date_format)
        bod = bod.upper()
        bod = f"{bod}\nDATE OF BIRTHDAY"

        issue = user.joined_at.strftime(date_format)
        issue = issue.upper()
        issue = f"{issue}\nDATE OF ISSUED"

        role = users[str(user.id)]["role"]
        status = role
        public_status = f"{status}\nPUBLIC STATUS"
        draw.text((541, 95), judul, (255, 255, 255), font=font_bold)
        draw.text((330, 225), card_id, (0, 0, 0), font=font_bold)
        draw.text((700, 225), issue, (0, 0, 0), font=font_bold)
        draw.text((330, 300), nama, (100, 149, 237), font=font_nama)
        draw.text((330, 345), nama_sub, (0, 0, 0), font=font_bold)
        draw.text((330, 400), bod, (0, 0, 0), font=font_bold)
        draw.text((330, 490), public_status, (0, 0, 0), font=font_bold)
        draw.text((700, 400), nation, (0, 0, 0), font=font_bold)

        foto_ktp = user.avatar_url_as(size=128)
        data_foto = BytesIO(await foto_ktp.read())
        pfp = Image.open(data_foto)
        # pfp = pfp.resize((198,241))
        pfp = pfp.resize((198, 198))
        ktp.paste(pfp, (87, 225))
        # ktp.save("image/ktp/"+"ktp"+users_id+".png")

        barcode = users_id
        barcode = EAN13(barcode, writer=ImageWriter())
        barcode.save(f"image/barcode/bar{users_id}")

        foto_bar = Image.open(f"image/barcode/bar{users_id}.png")
        bar = foto_bar.resize((238, 90))
        ktp.paste(bar, (70, 450))
        ktp.save("image/ktp/" + "ktp" + users_id + ".png")

        # embed = discord.Embed(color = discord.Color.blue())
        # embed.set_image(url = "image/ktp/"+"ktp"+users_id+".png")
        # await ctx.send(embed = embed)
        await ctx.send(file=discord.File("image/ktp/" + "ktp" + users_id + ".png"))

    @commands.command(name="con", help="Status maintenance!")
    async def con(self, ctx, *, user: discord.Member = None):
        await open_profil(ctx.author)
        users = await get_user_data()
        if user is None:
            user = ctx.author
        health = users[str(user.id)]["health"]
        embed = discord.Embed(
            title=f"{user.name}'s, Heatlh Condition",
            description=f"Kondisi kesehatan harian kamu adalah **{health}%**",
            color=discord.Color.green(),
        )
        # embed.add_field(name = "Health", value = "Kosong")
        embed.set_footer(
            text=f"Project Kacang 1.0.0 | Under Development by Kacang Team"
        )

        nama = user.name
        content = f"Halo {nama}, Kondisi kesehatan harian kamu adalah {health}%"
        tts = gTTS(f"{content}", lang="id", slow=False)
        tts.save(f"audio/{nama}-kondisi.mp3")
        data = discord.File(f"audio/{nama}-kondisi.mp3")

        await ctx.send(embed=embed)
        await ctx.send(file=data)


async def open_profil(user):
    profil = await get_user_data()

    if str(user.id) in profil:
        return False
    else:
        profil[str(user.id)] = {}
        profil[str(user.id)]["role"] = "WARGA"
        profil[str(user.id)]["health"] = 100

    with open("cogs/profil.json", "w") as prof:
        json.dump(profil, prof)
    return True


async def get_user_data():
    with open("cogs/profil.json", "r") as prof:
        profil = json.load(prof)
    return profil


def setup(client):
    client.add_cog(Users(client))
