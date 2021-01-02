import discord 
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl
import os
import asyncio
from settings import YTDLSource, ytdl
from dotenv import load_dotenv
from random import choice
import validators

#bot config
client = commands.Bot(command_prefix='.')

#ytdl config
youtube_dl.utils.bug_reports_message = lambda: ''

#get token
load_dotenv()

#lists
status = ['Workin']
player_args = []
queue=[]

#management commands
@client.event
async def on_ready():
    print("{0.user}".format(client))
    print('discord.py version: '+discord.__version__)
    # change_status.start()

@client.command(aliases=["e"])
@commands.has_permissions(administrator=True)
async def exit(ctx):
    await client.close()

#music commands
@client.command(aliases=["j"])
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("Not connected to channel")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command(aliases=["l"])
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(aliases=["p"])
async def play(ctx):
    global player_args
    server = ctx.message.guild
    voice_channel = server.voice_client
    if validators.url(player_args[0]):
        async with ctx.typing():
            player, duration, videoIdExt = await YTDLSource.from_url(player_args[0], loop=client.loop)
            voice_channel.play(player, after=lambda e: print('error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))
        del(player_args[0])
        await asyncio.sleep(duration)
        os.remove("files/"+videoIdExt)
        if len(player_args)>0:
            play(ctx)
    else:
        async with ctx.typing():
            player, duration, videoIdExt = await YTDLSource.from_search(player_args[0], loop=client.loop)
            voice_channel.play(player, after=lambda e: print('error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))
        del(player_args[0])
        await asyncio.sleep(duration)
        os.remove("files/"+videoIdExt)
        if len(player_args)>0:
            play(ctx)


@client.command(aliases=["n"])
async def skip(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()
    if queue>0:
        play(ctx)

@client.command(aliases=["v"])
async def view(ctx):
    await ctx.send(f'`{player_args}`')
    
@client.command(aliases=["q"])
async def queue_(ctx, *, arg):
    player_args.append(str(arg))
    await ctx.send('Dodano')

@client.command(aliases=["r"])
async def remove(ctx, number):
    try:
        del(player_args[int(number)])
        await ctx.send(f'`{player_args}`')
    except:
        await ctx.send('empty')

@client.command(aliases=["s"])
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()

#clean up debug
@client.command()
async def delete(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)

@client.command(aliases=['vol'])
async def volume(ctx, number:int):
    ctx.voice_client.source.volume=number/100

@client.command(aliases=['thinking'])
async def seek(ctx, number:int):
    ffmpeg_options.update({'options': '-vn -ss '+str(number)})

client.run(os.getenv('TOKEN'))

# @tasks.loop(seconds=20)
# async def change_status():
#     await client.change_presence(activity=discord.Game(choice(status)))
