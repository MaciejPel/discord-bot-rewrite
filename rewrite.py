import discord 
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl
import os
import asyncio
from settings import YTDLSource, ytdl
from dotenv import load_dotenv
from random import choice


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
@client.command(name='join')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("Not connected to channel")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command(name='leave')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(name='play')
async def play(ctx):
    global queue
    server = ctx.message.guild
    voice_channel = server.voice_client
    async with ctx.typing():
        player, duration, videoIdExt = await YTDLSource.from_url(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    await ctx.send('**Now playing:** {}'.format(player.title))
    del(queue[0])
    await asyncio.sleep(duration)
    os.remove("files/"+videoIdExt)
    if len(queue)>0:
        play(ctx)

@client.command(name='queue')
async def queue_(ctx, url):
    global queue
    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')

@client.command(name='remove')
async def remove(ctx, number):
    global queue
    try:
        del(queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')
    except:
        await ctx.send('Your queue is either **empty** or the index is **out of range**')

#clean up debug
@client.command(name='delete')
async def delete(ctx, amount=5):
    await ctx.channel.purge(limit=amount+1)

client.run(os.getenv('TOKEN'))

# @tasks.loop(seconds=20)
# async def change_status():
#     await client.change_presence(activity=discord.Game(choice(status)))
