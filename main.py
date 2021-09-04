#Импорт библиотек
print("Импорт библиотек...")
import discord
print("Импорт 1/9")
from discord.ext import commands
print("Импорт 2/9")
from config import settings
print("Импорт 3/9")
import asyncio
print("Импорт 4/9")
from asyncio import sleep
print("Импорт 5/9")
from discord.utils import get
print("Импорт 6/9")
import youtube_dl
print("Импорт 7/9")
import os
print("Импорт 8/9")
import json
print("Импорт 9/10")
import sqlite3
print("Импорт 10/10")
import random

#переменные
waitingForSong = False
musicVolume = 100
usersData = {}
bot = commands.Bot(command_prefix = settings['prefix'], intents = discord.Intents.all())
bot.remove_command("help")

connection = sqlite3.connect("server.db")
cursor = connection.cursor()

@bot.event
async def on_ready():
    print('[LOG] Бот был активирован под ником {0.user}'.format(bot))
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        name TEXT,
        id INT,
        cash BIGINT,
        rep INT,
        lvl INT
    )""")
    connection.commit()

    for guild in bot.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 1)")
                connection.commit()
            else:
                pass

    connection.commit()

@bot.event
async def on_member_join(member):
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 1)")
        connection.commit()
    else:
        pass
    channel = bot.get_channel(673495471288746014)
    await channel.send(f'Добро пожаловать, {member}, на сервер!')

@bot.command(aliases = ["balance", "cash", "bal", "баланс", "деньги"])
async def __balance(ctx, member: discord.Member = None):
    if member is None:
        await ctx.send(embed = discord.Embed(
            description = f"""Баланс пользователя **{ctx.author}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :gem:**"""
        ))
    else:
        await ctx.send(embed = discord.Embed(
            description = f"""Баланс пользователя **{member}** составляет **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :gem:**"""
        ))

@bot.command(aliases = ["award"])
async def __award(ctx):
    randomAward = random.randint(250, 1050)
    cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(randomAward), ctx.author.id)
    connection.commit()

    await ctx.message.add_reaction("✅")
    dmId = bot.get_user(ctx.author.id)
    await dmId.send("Поздравляю вас с полученной зарплатой. На сегодня вы теперь не можете получить её ещё раз.\nС любовью,\nКоманда FireFall.")

@bot.command(aliases = ["pay"])
async def __pay(ctx, member: discord.Member = None, amount: int = None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, попробуйте ещё раз, только укажите имя пользователя, которому хочете перевести деньги.")
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author}**, попробуйте ещё раз, только не забудьте указать сумму, которую хотите перевести")
        elif amount < 1:
            await ctx.send(f"**{ctx.author}**, вы не можете перевести сумму меньше 1 :gem:")
        else:
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, ctx.member.id))
            connection.commit()

            await ctx.message.add_reaction("✅")
            await ctx.send(embed = discord.Embed(
                description = f"""Баланс пользователя {member} был пополнен игроком {ctx.author.id} на сумму **{cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :gem:**"""
            ))

@bot.command()
async def tempmute(ctx, user: discord.Member, time: int, reason):
    permissionRole = discord.utils.find(lambda r: r.name == 'Админ', ctx.message.server.roles)
    if permissionRole in user.roles:
        role = user.guild.get_role(872750957467947058) # айди роли которую будет получать юзер
        await ctx.send(f'{user} получил мут на {time} минут по причине: {reason}')
        await user.add_roles(role)
        await user.move_to(None)
        await asyncio.sleep(time * 60)
        await user.remove_roles(role)
    else:
        await ctx.send(embed = discord.Embed(
            description = f"""❌Вы не имеете прав на выполнение данной команды.❌"""
        ))
        await ctx.message.add_reaction("❌")

@bot.command()
async def tempban(ctx, user: discord.Member, time: int, reason):
    permissionRole = discord.utils.find(lambda r: r.name == 'Модератор', ctx.message.server.roles)
    if permissionRole in user.roles:
        role = user.guild.get_role(872751269809369118) # айди роли которую будет получать юзер
        await ctx.send(f'{user} был временно забанен на {time} минут по причине: {reason}')
        await user.add_roles(role)
        await user.move_to(None)
        await asyncio.sleep(time * 60)
        await user.remove_roles(role)
    else:
        await ctx.send(embed = discord.Embed(
            description = f"""❌Вы не имеете прав на выполнение данной команды.❌"""
        ))
        await ctx.message.add_reaction("❌")

@bot.command()
async def join(ctx):
    author = ctx.message.author
    global voice_channel
    channel = ctx.message.author.voice.channel
    voice_channel = get(bot.voice_clients, guild=ctx.guild)

    if voice_channel and voice_channel.is_connected():
        await voice_channel.move_to(channel)
        await ctx.send(f'Бот был перемещён к каналу {channel} пользователем {author}')
    else:
        voice_channel = await channel.connect()
        await ctx.send(f'Бот был подключён к каналу {channel} пользователем {author}')

@bot.command()
async def leave(ctx):
    author = ctx.message.author
    channel = ctx.message.author.voice.channel
    voice_channel = get(bot.voice_clients, guild=ctx.guild)

    if voice_channel and voice_channel.is_connected():
        await voice_channel.disconnect()
        await ctx.send(f'Бот покинул канал {channel}')
    else:
        voice_channel = await channel.connect()
        await ctx.send(f'Бот покинул канал {channel}')

@bot.command()
async def custom_play(ctx):
    await ctx.send("Отправь сюда аудио, которое хочешь воспроизвести(желательно в формате mp3)")
    wait_for_song = True

@bot.command()
async def play(ctx, url: str):
    song_is_here = os.path.isfile('song.mp3')

    try:
        if song_is_here:
            os.remove('song.mp3')
            print("[LOG] Старый файл удалён")
    except PermissionError:
        print("[LOG] Не удалось удалить файл")

    await ctx.send("Пожалуйста, подождите...")
    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("[LOG] Загрузка музыки...")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"[LOG] Переименовывание файла {file}...")
            os.rename(file, "song.mp3")
        else:
            pass

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"[LOG] {name}, музыка закончилась."))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.7

    song_name = name.rsplit("-", 2)
    await ctx.send(f"Вопроизведение музыки {song_name[0]}")

@bot.command()
async def musicstop(ctx):
    voice.stop()
    await ctx.send("Остановлено ⏹")

@bot.command(aliases = ["help", "помощь"])
async def __help(member, ctx):
    member.send('Привет! Я тут видел, тебе понадобилась помощь? Сейчас расскажу, как мной пользоваться!\n$tempban (айди участника) (причина) (длительность в минутах) - запрещает доступ участнику ко всему на сервере(только для ролей "Модератор")')
bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена
