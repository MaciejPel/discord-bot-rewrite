import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import json
import aiohttp
import random
import youtube_dl
import os
import random
import threading
bot = commands.Bot(command_prefix='.')
link="https://imgur.com/a/sjCdDr5"
players={}
queues={}
def check_queue(id):
    if queues[id] !=[]:
        player=queues[id].pop(0)
        players[id]=player
        player.start()

"""def printit():
  threading.Timer(2.0, printit).start()
  print (players)
printit()"""

"""(y)"""
@bot.event
async def on_ready():
    await bot.change_presence(game=discord.Game(name="muzykę na serwerze",url='https://www.twitch.tv/qet_makej', 
        type=1))
    print('Zaczynam, wersja: '+discord.__version__)

"""#1 dziala"""
@bot.command(pass_context=True)
async def ready(ctx):
    await bot.say ("Jestem bardziej ready od ciebie")
    await bot.say ("Jestem " + bot.user.name)
    await bot.say ("Id: " + bot.user.id)
    print('Pytano czy bot jest gotowy')
"""#2 dziala swietnie"""
@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    await bot.say("Nazwa typa: {}".format(user.name))
    await bot.say("Id typa: {}".format(user.id))
    await bot.say("Status typa: {}".format(user.status))
    await bot.say("Najwyższa rola to: {}".format(user.top_role))
    await bot.say("Przyłączył się: {}".format(user.joined_at))
    print('Ktoś pytał o {}'.format(user.name))
"""#3 raczej dziala"""
@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    await bot.say(":boot: Eldo, {}".format(user.name))
    await bot.kick(user)
    print('Wyrzucono {}'.format(user.name))

"""#4 dziala poedytowac"""
@bot.command(pass_context=True)
async def showhelp(ctx):
    await bot.say("Prefiks bota to '.'")
    await bot.say("#showhelp -  pomoc ogólna")
    await bot.say("#info @user- informacje o użytkownikach")
    await bot.say("#kick @user - wywalanie ludzi")
    await bot.say("music - opcje dotyczące kanału muzycznego")
    print ("Ktoś poprosił o pomoc")

@bot.command(pass_context=True)
async def music(ctx):
    await bot.say("#j- wezwanie bota na kanał")
    await bot.say("#l- usunięcie bota z kanału")
    await bot.say("#p- graj_muzyko {link z yt}")
    await bot.say("#q- dodanie kolejnej piosenki do kolejki, 2nd play nie zadziała")
    await bot.say("#skip- pominięcie aktulanie granej piosenki")
    await bot.say("#pause- spauzowanie bota w danym momencie piosenki")
    await bot.say("#resume- odpauzowanie bota z zatrzymanego miejsca")
    await bot.say("#stop- zatrzymanie całego bota muzycznego łącznie z playlistą")
    print ("Ktoś poprosił o pomoc z muzyką")

"""bot.command(pass_context=True)#poprawic
async def dosc(ctx):
    msg=await bot.say(link)
    print ("Ktoś poprosił o pomoc")"""

@bot.command(pass_context=True)
async def l(ctx):
    server = ctx.message.server
    for vclient in bot.voice_clients:
        if(vclient.server == ctx.message.server):
            await vclient.disconnect()
    else:
        await bot.say("Bot is not in a voice channel in this server!")
        return
    await bot.say(":white_check_mark:")

@bot.command(pass_context=True)
async def pause(ctx):
    id=ctx.message.server.id
    players[id].pause()  
    print ("Muzyka spauzowana")
    
@bot.command(pass_context=True)
async def resume(ctx):
    id=ctx.message.server.id
    players[id].resume()
    print ("Muzyka wznowiona")

@bot.command(pass_context=True)
async def skip(ctx):
    id=ctx.message.server.id
    players[id].stop()
    print ("Pominięto piosenkę")

@bot.command(pass_context=True)
async def stop(ctx):
    server = ctx.message.server
    id=ctx.message.server.id
    players[id].stop()
    queues[server.id]=[]
    print ("Kolejka wyzerowana")

@bot.command(pass_context=True, aliases=['vol'])
async def v(ctx, amount):
    server = ctx.message.server
    id=ctx.message.server.id
    player=players[id]
    i=int(amount)
    player.volume = i / 100
    p=await bot.say('Zmieniono :speaker: do: ' + amount + '%')
    channel = ctx.message.channel
    await asyncio.sleep(15)
    await bot.delete_message(p)
    mgs = [] 
    number = int(1) 
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await bot.delete_messages(mgs)
    print('Zmiana głośności')

@bot.command(pass_context=True, aliases=['np','now'])
async def n(ctx):
    server = ctx.message.server
    id=ctx.message.server.id
    player=players[id]
    embed2 = discord.Embed(colour=discord.Colour(0x7777EC))
    embed2.add_field(name="Teraz gramy: ", value=player.title)
    span=await bot.say(embed=embed2)
    await asyncio.sleep(15)
    await bot.delete_message(span)
    number = int(2) 
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await bot.delete_messages(mgs)
    print('Zmiana głośności')
    print ('Była pytana piosenka')

@bot.command(pass_context = True, aliases=['clear'])
@commands.has_role('GTM')
async def c(ctx, number):
    mgs = [] 
    number = int(number) 
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await bot.delete_messages(mgs)

@bot.command(pass_context=True)
async def plemie(ctx):
    channel = ctx.message.channel
    zzz=str((random.choice(os.listdir("./nword"))))
    await bot.send_file(channel,'nword/'+zzz)
    await bot.say(zzz)
    await asyncio.sleep(7)
    mgs = [] 
    number = int(2) 
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        mgs.append(x)
    await bot.delete_messages(mgs)

@bot.command(pass_context=True, aliases=['join'])
async def j(ctx):
    channel= ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)
    print ("Bot rusza do akcji muzycznej")
@bot.command(pass_context=True, aliases=['xlay'])
async def x(ctx, *, args):
    server = ctx.message.server
    voice_bot = bot.voice_client_in(server)
    player = await voice_bot.create_ytdl_player("ytsearch:" +args, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", after=lambda:check_queue(server.id))
    players[server.id] = player
    player.start()
    z=player.duration/60
    h=round(z,2)
    embed1 = discord.Embed(colour=discord.Colour(0xFFC7EC))
    embed1.add_field(name="Status:", value="Zaczynam zabawę :fire:")
    embed1.add_field(name="Teraz gramy:", value=player.title, inline=True)
    embed1.add_field(name="Załączył:", value=ctx.message.author, inline=True)
    embed1.add_field(name="Czas trwania (min):", value=h, inline=True)
    embed1.add_field(name="Wyświetlenia:", value=player.views, inline=True)
    print ("Gram "+player.title)
    embed2 = discord.Embed(colour=discord.Colour(0x7777EC))
    embed2.add_field(name="Zakończona piosenka to: ", value=player.title)
    sent=await bot.say(embed=embed1)
    await asyncio.sleep(player.duration)
    await bot.delete_message(sent)
    span=await bot.say(embed=embed2)
    await asyncio.sleep(30)
    await bot.delete_message(span)
    print ("Wyczyszczono "+player.title)
@bot.command(pass_context=True, aliases=['queue'])
async def q(ctx,*,args):
    server=ctx.message.server
    voice_bot= bot.voice_client_in(server)
    player=await voice_bot.create_ytdl_player("ytsearch:" +args, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", after=lambda:check_queue(server.id))
    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id]=[player]
    z=player.duration/60
    h=round(z,2)
    embed = discord.Embed(colour=discord.Colour(0xFF5CE0))
    embed.add_field(name="Status:", value="Wideo zakolejkowane :heart:")
    embed.add_field(name="Teraz gram:", value=player.title, inline=True)
    embed.add_field(name="Załączył:", value=ctx.message.author, inline=True)
    embed.add_field(name="Czas trwania (min):", value=h, inline=True)
    embed.add_field(name="Wyświetlenia:", value=player.views, inline=True)
    await bot.say(embed=embed)
    print ("Dodano piosenke do kolejki")

@bot.command(pass_context=True, aliases=['play'])
async def p(ctx,*,args):
    channel1= ctx.message.author.voice.voice_channel
    channel1name=ctx.message.author.voice.voice_channel.name
    server1=ctx.message.server
    voice_bot1=bot.voice_client_in(server1)
    if not voice_bot1:
        await bot.join_voice_channel(channel1)
        if not players:
            server = ctx.message.server
            voice_bot = bot.voice_client_in(server)
            player = await voice_bot.create_ytdl_player("ytsearch:" +args, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", after=lambda:check_queue(server.id))
            players[server.id] = player
            player.start()
            z=player.duration/60
            h=round(z,2)
            embed1 = discord.Embed(colour=discord.Colour(0xFFC7EC))
            embed1.add_field(name="Status:", value="Zaczynam zabawę :fire:")
            embed1.add_field(name="Teraz gramy:", value=player.title, inline=True)
            embed1.add_field(name="Załączył:", value=ctx.message.author, inline=True)
            embed1.add_field(name="Czas trwania (min):", value=h, inline=True)
            embed1.add_field(name="Wyświetlenia:", value=player.views, inline=True)
            print ("Gram "+player.title)
            embed2 = discord.Embed(colour=discord.Colour(0x7777EC))
            embed2.add_field(name="Zakończona piosenka to: ", value=player.title)
            sent=await bot.say(embed=embed1)
            await asyncio.sleep(player.duration)
            await bot.delete_message(sent)
            span=await bot.say(embed=embed2)
            await asyncio.sleep(20)
            await bot.delete_message(span)
            print ("Wyczyszczono "+player.title)
            print (players)
            print (queues)
        elif players:
            server=ctx.message.server
            voice_bot= bot.voice_client_in(server)
            player=await voice_bot.create_ytdl_player("ytsearch:" +args, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", after=lambda:check_queue(server.id))
            if server.id in queues:
                queues[server.id].append(player)
            else:
                queues[server.id]=[player]
            z=player.duration/60
            h=round(z,2)
            embed = discord.Embed(colour=discord.Colour(0xFF5CE0))
            embed.add_field(name="Status:", value="Wideo zakolejkowane :heart:")
            embed.add_field(name="Teraz gram:", value=player.title, inline=True)
            embed.add_field(name="Załączył:", value=ctx.message.author, inline=True)
            embed.add_field(name="Czas trwania (min):", value=h, inline=True)
            embed.add_field(name="Wyświetlenia:", value=player.views, inline=True)
            await bot.say(embed=embed)
            print ("Dodano piosenke do kolejki")
            print (players)
            print (queues)
    elif voice_bot1:
        res = ",".join(("{}={}".format(*i) for i in players.items())) 
        print (res)
        if not players:
            server = ctx.message.server
            voice_bot = bot.voice_client_in(server)
            player = await voice_bot.create_ytdl_player("ytsearch:" +args, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", after=lambda:check_queue(server.id))
            players[server.id] = player
            player.start()
            z=player.duration/60
            h=round(z,2)
            embed1 = discord.Embed(colour=discord.Colour(0xFFC7EC))
            embed1.add_field(name="Status:", value="Zaczynam zabawę :fire:")
            embed1.add_field(name="Teraz gramy:", value=player.title, inline=True)
            embed1.add_field(name="Załączył:", value=ctx.message.author, inline=True)
            embed1.add_field(name="Czas trwania (min):", value=h, inline=True)
            embed1.add_field(name="Wyświetlenia:", value=player.views, inline=True)
            print ("Gram "+player.title)
            embed2 = discord.Embed(colour=discord.Colour(0x7777EC))
            embed2.add_field(name="Zakończona piosenka to: ", value=player.title)
            sent=await bot.say(embed=embed1)
            await asyncio.sleep(player.duration)
            await bot.delete_message(sent)
            span=await bot.say(embed=embed2)
            await asyncio.sleep(20)
            await bot.delete_message(span)
            print ("Wyczyszczono "+player.title)
            print (players)
            print (queues)
        elif "stopped" in res:
            server = ctx.message.server
            voice_bot = bot.voice_client_in(server)
            player = await voice_bot.create_ytdl_player("ytsearch:" +args, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", after=lambda:check_queue(server.id))
            players[server.id] = player
            player.start()
            z=player.duration/60
            h=round(z,2)
            embed1 = discord.Embed(colour=discord.Colour(0xFFC7EC))
            embed1.add_field(name="Status:", value="Zaczynam zabawę :fire:")
            embed1.add_field(name="Teraz gramy:", value=player.title, inline=True)
            embed1.add_field(name="Załączył:", value=ctx.message.author, inline=True)
            embed1.add_field(name="Czas trwania (min):", value=h, inline=True)
            embed1.add_field(name="Wyświetlenia:", value=player.views, inline=True)
            print ("Gram "+player.title)
            embed2 = discord.Embed(colour=discord.Colour(0x7777EC))
            embed2.add_field(name="Zakończona piosenka to: ", value=player.title)
            sent=await bot.say(embed=embed1)
            await asyncio.sleep(player.duration)
            await bot.delete_message(sent)
            span=await bot.say(embed=embed2)
            await asyncio.sleep(20)
            await bot.delete_message(span)
            print ("Wyczyszczono "+player.title)
            print (players)
            print (queues)  
        else:
            server=ctx.message.server
            voice_bot= bot.voice_client_in(server)
            player=await voice_bot.create_ytdl_player("ytsearch:" +args, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", after=lambda:check_queue(server.id))
            if server.id in queues:
                queues[server.id].append(player)
            else:
                queues[server.id]=[player]
            z=player.duration/60
            h=round(z,2)
            embed = discord.Embed(colour=discord.Colour(0xFF5CE0))
            embed.add_field(name="Status:", value="Wideo zakolejkowane :heart:")
            embed.add_field(name="Teraz gram:", value=player.title, inline=True)
            embed.add_field(name="Załączył:", value=ctx.message.author, inline=True)
            embed.add_field(name="Czas trwania (min):", value=h, inline=True)
            embed.add_field(name="Wyświetlenia:", value=player.views, inline=True)
            await bot.say(embed=embed)
            print ("Dodano piosenke do kolejki")
            print (players)
            print (queues)

bot.run("NDk1Mjc1MzQyMjIzOTAwNjgz.Do_sxg.RjJc3UfmA9-7aKRH7DLbvlEXN58")

"""do zrobienia
***done***kontrola glosnosci
***done***teraz grane
dodane purge przy okazji
#3polaczyc play join i queue
#4 wyswietlanir dtanu kolejki kolejki
"""