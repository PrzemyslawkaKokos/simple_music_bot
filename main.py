import discord
from discord.ext import commands
import youtube_dl as ytd
import os
import asyncio

client = commands.Bot(command_prefix="%")
client.remove_command("help")

# Funkcja sprawdzająca czy bot jest w vc
def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

# Funkcja od auto wychodzenia
async def auto_wyjscie(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    while True:
        await asyncio.sleep(5)

        if voice.is_playing() == False:
            await voice.disconnect()
            break

@client.command()
async def play(ctx, url : str):
    user = ctx.message.author
    vc = user.voice.channel

    # Sprawdzanie czy jest istniejący plik song.mp3, jeżeli tak go usuwa
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Proszę uprzejmie zaczekać aż obecnie grany utwór się zakończy :pray:")

    # Sprawdzanie czy bot jest już w vc za pomocą wcześniejszej funkcji
    # voiceChannel = discord.utils.get(ctx.guild.voice_channels, name="Nauru") tak na wszelki wypadek
    if not is_connected(ctx):
        await vc.connect()
    else:
        pass

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Tworzenie pliku song.mp3
    with ytd.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")

    await ctx.send("Kocham Jana Pawła II :pray:")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    await auto_wyjscie(ctx)

@client.command()
async def spierdalaj(ctx):
    await ctx.send("Jan Paweł II nie gwałcił małych dzieci :pray:")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await voice.disconnect()

@client.command()
async def pauza(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await ctx.send("Już pauzeju")
        voice.pause()
    else:
        await ctx.send("Nic nie gra debilu")

@client.command()
async def wznow(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await ctx.send("Ok")
        voice.resume()
    else:
        await ctx.send("Debilu nic nie jest zapauzowane :angry:")

@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await ctx.send("Skippuję mszę")
    voice.stop()

@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Pomoc", description = "Twój stary się zesrał", color = ctx.author.color)

    em.add_field(name = "Muzyczne", value = "`play`, `spierdalaj`, `pauza`, `wznow`, `skip`")

    await ctx.send(embed = em)

client.run("ODIwMzgzMzAyMTQ1NjcxMjI4.YE0XfQ.5J-1MqsaEWeZ_byneephFKGDFmI")
print("Powinien już być online")
