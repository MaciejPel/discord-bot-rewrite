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
queue = []

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
@client.command(aliases=["l"])
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(aliases=["p"])
async def play(ctx, *, arg):
    if not ctx.message.author.voice:
        pass
    else:
        channel = ctx.message.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)
    async with ctx.typing():
        title=await YTDLSource.search(arg)
    queue.append(title)
    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        player, duration, videoIdExt = await YTDLSource.from_search(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))
    await asyncio.sleep(duration)
    del(queue[0])
    os.remove("files/"+videoIdExt)

@client.command(aliases=["ch"])
async def check(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    if voice_channel.is_playing():
        return True
    else:
        return False

@client.command(aliases=["n"])
async def skip(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()
    # if len(queue)>0:
    #     play(ctx)

@client.command(aliases=["v"])
async def view(ctx):
    await ctx.send(f'`{queue}`')
    

@client.command(aliases=["r"])
async def remove(ctx, number):
    try:
        del(queue[int(number)])
        await ctx.send(f'`{queue}`')
    except:
        await ctx.send('empty')

@client.command(aliases=["s"])
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()

@client.command()
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.pause()

@client.command()
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.resume()

@client.command(aliases=['vol'])
async def volume(ctx, number:int):
    ctx.voice_client.source.volume=number/100

#clean up debug
@client.command()
async def delete(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)

# @client.command(aliases=['thinking'])
# async def seek(ctx, number:int):
#     ffmpeg_options.update({'options': '-vn -ss '+str(number)})

client.run(os.getenv('TOKEN'))

# @tasks.loop(seconds=20)
# async def change_status():
#     await client.change_presence(activity=discord.Game(choice(status)))
