import discord
from discord import colour
from discord.ext import commands
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
import json
import os
import random
import datetime
import asyncio
from asyncio import TimeoutError
import requests
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
from barcode import EAN13
from barcode.writer import ImageWriter
from urllib import request
from gtts import gTTS
import logging

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

# os.chdir("E:\\DIaz\\WORK\\BOT\\project-kacang-master\\project-kacang")
# os.chdir("/Users/laboratoriumaudit2/Public/Diaz/project-kacang")

client = commands.Bot(command_prefix="..")


@client.command(help="Dev ONLY!")
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command(help="Dev Only!")
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {client.latency}")


@client.command()
async def cmd(ctx):
    channel = discord.utils.get(guild.text_channels, name="help", topic="help channel")
    # channel = discord.TextChannel
    await ctx.send(f"Here's your mentioned channel ID: {channel}")


@client.command()
async def test(ctx):
    param_id = str(ctx.guild.owner_id)
    URL = f"http://127.0.0.1:8000/api/DiscordMember/{param_id}/"
    data = requests.get(url=URL).json()
    if data["id_discord"] == str(ctx.author.id):
        embed = discord.Embed(description="Pemilik Server!", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        # guild_owner = client.get_user(ctx.guild.owner_id)
        await ctx.send(f"Hey! {ctx.author.name}, kamu bukan pemilik server ini!")


@client.command()
async def wet(ctx):
    url = "https://ibnux.github.io/BMKG-importer/cuaca/501191.json"
    today = datetime.date.today()
    time_param = "18:00:00"
    time_param = datetime.datetime.strptime(time_param, "%H:%M:%S")
    response = request.urlopen(url)
    data = json.loads(response.read())
    w_cuaca = ""
    for item in data:
        date_time_obj = datetime.datetime.strptime(
            item["jamCuaca"], "%Y-%m-%d %H:%M:%S"
        )
        date = date_time_obj.date()
        time = date_time_obj.time()
        w_cuaca += f"Time : {time}\n"
        w_cuaca += f'Weather : {item["cuaca"]}\n'
        w_cuaca += f'Humidity : {item["humidity"]}\n'
        w_cuaca += f'TempC : {item["tempC"]}\n'
        w_cuaca += f"\n"
        if time == time_param.time():
            break
    # print(w_cuaca)
    embed = discord.Embed(
        title=f"Weather Info {today}\n{ctx.guild.name} CITY",
        description=f"{w_cuaca}",
        color=discord.Color.blue(),
    )
    embed.set_footer(
        text=f"Data BMKG\nReal Time Data Location : DKI Jakarta | Created by Kacang Team"
    )
    await ctx.send(embed=embed)


@client.command()
async def dompet(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]
    wallet = "{:,.0f}".format(wallet_amt)
    bank = "{:,.0f}".format(bank_amt)

    embed = discord.Embed(
        color=discord.Color.green(),
        description=f"**{ctx.author.name}**, total aset kekayaan kamu adalah",
    )
    embed.set_author(name=f"Dompet dari {str(user.name)}", icon_url=user.avatar_url)
    embed.add_field(name="Uang di Dompet 💰", value=f"**{wallet}**")
    embed.add_field(name="Uang di Bank 🏦", value=f"**{bank}**")
    embed.set_footer(text="ID: " + str(user.id) + " | Created by Kacang Team")
    await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 600, commands.BucketType.user)
async def blt(ctx):
    await open_account(ctx.author)
    await open_profil(ctx.author)
    users = await get_bank_data()
    akun = await get_user_data()
    user = ctx.author
    if akun[str(user.id)]["role"] == "WALI KOTA KACANG":
        embed = discord.Embed(
            description=f"**Dasar {ctx.author.name}**, kamu punya jabatan tinggi masih minta BLT!",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
    else:
        earn = random.randrange(0, 101)
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, kamu dapat tunjangan pengangguran sebesar **{earn}** `🥜` dikirimkan ke `rekening bank`.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
        users[str(user.id)]["bank"] += earn
        with open("bank.json", "w") as bank:
            json.dump(users, bank)


@client.command()
@commands.cooldown(1, 1800, commands.BucketType.user)
async def kerja(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()
    profile = await get_user_data()
    user = ctx.author
    rand = ["pass", "pass", "pass", "broke"]
    if random.choice(rand) == "broke":
        minus = random.randrange(10, 100)
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, akibat kecelakaan kerja kamu dilarikan ke rumah sakit dengan total biaya **{minus}** `🥜` diambil dari `rekening bank`. `❌`",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        users[str(user.id)]["bank"] -= minus
        with open("bank.json", "w") as bank:
            json.dump(users, bank)

        profile[str(user.id)]["health"] -= 2
        with open("cogs/profil.json", "w") as profil:
            json.dump(profile, profil)
    else:
        earn = random.randrange(100, 500)
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, setelah kerja keras membantu pemerintah, kamu mendapatkan upah sebesar **{earn}** `🥜` dikirimkan ke `rekening bank`.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
        users[str(user.id)]["bank"] += earn
        with open("bank.json", "w") as bank:
            json.dump(users, bank)

        profile[str(user.id)]["health"] -= 2
        with open("cogs/profil.json", "w") as profil:
            json.dump(profile, profil)


@client.command()
async def tarik(ctx, amount=None):
    await open_account(ctx.author)

    if amount is None:
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, harap masukkan jumlah tarik tunai.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount > bal[1]:
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, kamu tidak punya cukup uang.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    if amount < 0:
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, jumlah tidak boleh minus.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1 * amount, "bank")
    embed = discord.Embed(
        description=f"**{ctx.author.name}**, kamu melakukan tarik tunai sebesar `💸 {amount}`",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


@client.command()
async def simpan(ctx, amount=None):
    await open_account(ctx.author)

    if amount is None:
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, harap masukkan jumlah deposit.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount > bal[0]:
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, kamu tidak punya cukup uang.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    if amount < 0:
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, jumlah tidak boleh minus.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    await update_bank(ctx.author, -1 * amount)
    await update_bank(ctx.author, amount, "bank")
    embed = discord.Embed(
        description=f"**{ctx.author.name}**, kamu menyimpan uang sebesar `💸 {amount}`",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


@client.command()
async def tf(ctx, member: discord.Member = None, amount=None):
    await open_account(ctx.author)
    await open_account(member)

    if member == None:
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, siapa yang di transfer?",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    if amount is None:
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, harap masukkan jumlah uang yang di transfer.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    bal = await update_bank(ctx.author)
    amount = int(amount)
    if amount > bal[1]:
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, kamu tidak punya cukup uang.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    if amount < 0:
        embed = discord.Embed(
            description=f"**{ctx.author.name}**, jumlah tidak boleh minus.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)
        return

    await update_bank(ctx.author, -1 * amount, "bank")
    await update_bank(member, amount, "bank")
    embed = discord.Embed(
        description=f"**{ctx.author.name}**, kamu transfer uang sebesar `💸 {amount}` kepada `{member.name}`",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("bank.json", "w") as bank:
        json.dump(users, bank)
    return True


async def get_bank_data():
    with open("bank.json", "r") as bank:
        users = json.load(bank)
    return users


@client.command()
async def bag(ctx):
    await open_bag(ctx.author)
    user = ctx.author
    users = await get_user_bag()

    em = discord.Embed(title="Your Bag")
    for item in bag:
        name = item["name"]
        amount = item["amount"]

        em.add_field(name=name, value=amount)

    await ctx.send(embed=em)


@client.command(name="pasar", help="Untuk melihat menu pasar")
async def pasar(ctx, kategori=None, affirm=None):
    store_data = await get_store_data()
    # check null value
    idbarang = []
    data = store_data["makanan"] + store_data["minuman"]
    for i in data:
        if i["name"] == affirm:
            idbarang = [(i["id"])]
    if kategori is None and affirm is None:
        text = f"**{ctx.author.name}**, mohon pilih salah satu dari kategori dibawah\ndan ketik `..pasar [kategori]` untuk melihat item\n*- makanan : Makanan general*\n*- minuman : minuman menyegarkan*\n\n*tahap dev, belum bisa membeli!"
        embed = discord.Embed(description=text, color=discord.Color.orange())
        embed.set_author(
            name="Selamat Datang di Pasar Kacang ✨", icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)
    if kategori == "makanan":
        data = store_data["makanan"]
        item = ""
        for i in data:
            item += f"- [{i['price']}] **{i['name']}** | Stock : **{i['stock']}** ({i['description']})\n"
        text = f"Membeli makanan untuk memulihkan energimu!\n**Usage**\nUntuk membeli ketik `pasar beli [nama item]`\n**Dagangan**\n{item}"
        embed = discord.Embed(description=text, color=discord.Color.orange())
        embed.set_author(
            name="Selamat Datang di Pasar Kacang ✨", icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)
    if kategori == "minuman":
        data = store_data["minuman"]
        item = ""
        for i in data:
            item += f"- [{i['price']}] **{i['name']}** ({i['description']})\n"
        text = f"Membeli minuman untuk memulihkan energimu!\n**Usage**\nUntuk membeli ketik `pasar beli [nama item]`\n**Dagangan**\n{item}"
        embed = discord.Embed(description=text, color=discord.Color.orange())
        embed.set_author(
            name="Selamat Datang di Pasar Kacang ✨", icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)

    if kategori == "beli" and len(idbarang) == 0:
        text = (
            f"tidak ada barang dengan kode atau nama **{affirm}**\nmohon cek kembali!"
        )
        embed = discord.Embed(description=text, color=discord.Color.red())
        await ctx.send(embed=embed)

    if kategori == "beli" and affirm == affirm:
        data = store_data["makanan"] + store_data["minuman"]
        for i in data:
            if i["name"] == affirm:
                price = i["price"]
        text = f"Apakah kamu ingin membeli **{affirm}** seharga **{price}**?"
        embed = discord.Embed(
            title="Confirmation Dialog", description=text, color=discord.Color.orange()
        )
        msg = await ctx.channel.send(embed=embed)
        react1 = await msg.add_reaction("\u2705")
        react2 = await msg.add_reaction("\U0001F6AB")

        try:
            reaction, user = await client.wait_for(
                "reaction_add",
                check=lambda reaction, user: user == ctx.author
                and reaction.emoji in ["\u2705", "\U0001F6AB"],
                timeout=30.0,
            )

        except asyncio.TimeoutError:
            embed = discord.Embed(
                description=f"Membatalkan pembelian karena waktu habis",
                color=discord.Color.red(),
            )
            await ctx.channel.send(embed=embed)
            await msg.clear_reactions()

        else:
            if reaction.emoji == "\u2705":
                await open_account(ctx.author)
                bal = await update_bank(ctx.author)
                amount = int(price)
                if amount > bal[0]:
                    embed = discord.Embed(
                        description=f"**{ctx.author.name}**, kamu tidak punya cukup uang.",
                        color=discord.Color.red(),
                    )
                    await msg.edit(embed=embed)
                    await msg.clear_reactions()
                    return
                await update_bank(ctx.author, -1 * price)
                await update_bank(ctx.author, price, "bank")
                embed = discord.Embed(
                    description=f"Kamu berhasil membeli **{affirm}**",
                    color=discord.Color.green(),
                )
                await msg.edit(embed=embed)
                await msg.clear_reactions()

            else:
                embed = discord.Embed(
                    description=f"Transaksi dibatalkan!", color=discord.Color.red()
                )
                await msg.edit(embed=embed)
                await msg.clear_reactions()


async def get_store_data():
    with open("shop.json", "r") as shop:
        store = json.load(shop)
    return store


@client.command()
async def role(ctx):
    await open_profil(ctx.author)
    users = await get_user_data()
    user = ctx.author

    role = users[str(user.id)]["role"]
    embed = discord.Embed(description=f"Test role {role}", color=discord.Color.green())
    await ctx.send(embed=embed)


async def open_profil(user):
    profil = await get_user_data()

    if str(user.id) in profil:
        return False
    else:
        profil[str(user.id)] = {}
        profil[str(user.id)]["role"] = "WARGA SIPIL"

    with open("cogs/profil.json", "w") as prof:
        json.dump(profil, prof)
    return True


async def get_user_data():
    with open("cogs/profil.json", "r") as prof:
        profil = json.load(prof)
    return profil


async def open_bag(user):
    bag = await get_user_bag()

    if str(user.id) in bag:
        return False
    else:
        bag[str(user.id)] = {}
        bag[str(user.id)]["name"] = None
        bag[str(user.id)]["amount"] = None

    with open("bag.json", "w") as tas:
        json.dump(bag, tas)
    return True


async def get_user_bag():
    with open("bag.json", "r") as tas:
        bag = json.load(tas)
    return bag


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("bank.json", "w") as bank:
        json.dump(users, bank)
    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            description="Cek kembali apa yang kamu ketik!", color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    if isinstance(error, commands.CommandOnCooldown):
        times = int(error.retry_after)
        minutes = times % 3600
        minutes = minutes // 60
        second = times % 60
        embed = discord.Embed(
            description="**{}**, kamu bisa `{}` lagi dalam **{}m {}s** ❌".format(
                ctx.author.name, ctx.command.name, minutes, second
            ),
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


##JOB


@client.command()
async def DM(ctx, user: discord.User, *, message=None):
    message = message or "Ignore this DM, it's just test dev for DM system!"
    await user.send(message)


# Suara


@client.command(name="suara", help="Test Untuk Voice Assistant")
@commands.has_permissions(send_messages=True, manage_messages=True)
async def suara(ctx, channel: discord.TextChannel, *, content: str):
    user = ctx.author.name
    tts = gTTS(f"{content}", lang="id")
    tts.save(f"audio/{user}.mp3")
    data = discord.File(f"audio/{user}.mp3")
    await channel.send(file=data)


client.run("ODI1MzY4ODkwOTc2NTAxODEw.YF86rg.flMGiRjn9aPnSpOgB6hQLRWQTZc")
