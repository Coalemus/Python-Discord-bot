#! python3
# Discord Bot with Admin and music playing Features.
# Eduardo Jose Flores III: https://github.com/Coalemus
# Copyright (c) Eduardo Jose Flores III

from secret import TOKEN
import random 
from random import randint
import os 
from os import system
import shutil
import asyncio
import youtube_dl
import discord
from discord import opus
from discord.ext import commands
from discord.utils import get



sound_folder = r'D:\Music\Sound Effects'
log_channel_id = int('821008061480697896') 
tag_dict={'tag1': ['name1', 'name2'],
          'tag2': ['name1', 'name2', 'name3']}

client = commands.Bot(command_prefix = '.') 

@client.event
async def on_ready(): 
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Buff Correll videos')) 
    print("Bot is ready.")
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('.hello'):
        await message.reply('Hello!', mention_author=True)
    await client.process_commands(message)

@client.event 
async def on_member_join(member):
    print("f'{member} has joined a server.")

@client.event 
async def on_member_remove(member):
    print("f'{member} has left the server.")

@client.command(
    brief="Erases messages.", 
    description="Clears a specified amount of text depending on user input.")
async def clear(ctx, amount=0):
    if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        await ctx.channel.purge(limit=amount+1)

@client.command(
    brief="Permission error prompt.", 
    description="Prompts the user for unpermitted clear command.")
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to use this command.')

@client.command(
    brief="Direct message using bot.", 
    description="The bot sends a message specified by the User.")
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await client.fetch_user(user_id)
            await target.send(args)

            await ctx.channel.send("'" + args + "' sent to: " + target.name)

        except:
            await ctx.channel.send("Couldn't dm the given user.")

@client.command(
    brief="Bot messages all Users.", 
    description="The bot sends a message specified by the User to all members.")
async def dm_all(ctx, *, args=None):
    if args != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(args)
                print("'" + args + "' sent to: " + member.name)

            except:
                print("Couldn't send '" + args + "' to: " + member.name)

    else:
        await ctx.channel.send("A message was not provided.")

@client.command(
    brief="Kicks a User.", 
    description="Speaks for itself.")
async def kick(ctx, member : discord.Member, *, reason=None): 
    await member.kick(reason=reason)

@client.command(
    brief="Bans a User.", 
    description="Speaks for itself.")
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command(
    brief="Unbans a User.", 
    description="Speaks for itself.")
async def unban(ctx, *, member): 
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command(pass_context=True, aliases=['j','joi'], 
brief="Bot joins in your Voice channel.", 
description="Use when you have already joined a Voice channel.")
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connected to {channel}\n')

    await ctx.send(f'joined {channel}')    

@client.command(pass_context=True, aliases=['l','lea'], 
brief="Bot leaves your Voice channel.", 
description="Only works if Bot is in your Voice channel.")
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'The bot has left {channel}')
        await ctx.send(f'Left {channel}')   
    else:
        print('Bot was told to leave voice channel, but was not in one.')
        await ctx.send('Dont think I am in a voice channel.')

@client.command(pass_context=True, aliases=['p','pla'], 
brief="Plays a Youtube/Spotify song, predownloaded.", 
description="Use when stream command frequently crashes.")
async def play(ctx, url: str):
    
    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith("mp3"):
                        os.rename(file, "song.mp3")

                voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07
    
            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song.\n")    
    
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print('Removed old song file')
    except PermissionError:
        print('Trying to delete song file, but its being played.')
        await ctx.send('ERROR: music playing')
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send('Getting everything ready now.')

    voice = get(client.voice_clients, guild=ctx.guild) 

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }   
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading audio now.\n')
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'Renamed file: {file}\n')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit('-', 2)
    await ctx.send(f'Playing: {nname[0]}')
    print('Playing\n')

@client.command(pass_context=True, aliases=['pa','pau'], 
brief="Pauses a playing song.", 
description="Doesn't 'stop' a song, there's a seeparate command for that.")
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("music paused")
        voice.pause()
        await ctx.send("music paused")
    else:
        print("music not playing failed pause")
        await ctx.send("music not playing failed pause")

@client.command(pass_context=True, aliases=['r','res'], 
brief="Resumes a paused song.", 
description="Onnly resumes a 'paused' song and not a 'stopped' song.")
async def resume(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("music is not paused")
        await ctx.send("music is not paused")

@client.command(pass_context=True, aliases=['s','sto'], 
brief="Stops current song.",
 description="It is not a pause command.")
async def stop(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    if voice and voice.is_playing():
        print("music stopped")
        voice.stop()
        await ctx.send("music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")

queues = {}

@client.command(pass_context=True, aliases=['q','que'], 
brief="Queues songs , predownloaded.", 
description="Tested for Play command only, add Issue if it doesn't work for Stream command.")
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }   
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading audio now.\n')
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff sng{q_num} -f " + '"' + q_path + '"' + " -s " + url)

    await ctx.send("Adding song " + str(q_num) + " to the queue.")    

    print("Song added to queue\n")

@client.command(
    brief="Loads a cog.", 
    description="Cogs are 'Example', 'Test', 'soundboard', and 'stream'.")
async def load(ctx, extension): 
    client.load_extension(f'cogs.{extension}')

@client.command(
    brief="Unloads a cog.", 
    description="Cogs are 'Example', 'Test', 'soundboard', and 'stream'.")
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command(
    brief="Reloads a cog, refreshing it.", 
    description="Cogs are 'Example', 'Test', 'soundboard', and 'stream'.")
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

@client.command(aliases=['unsaynet', 'kahinay'],
 brief="Shows your own Ping.", 
 description="Shows a different ping for different people.")
async def ping(ctx): 
    await ctx.send(f'Pong! {client.latency * 100 // .2}ms') 

@client.command(aliases=['8ball'], brief="Basic 8ball.", 
description="Don't depend on this.")
async def magic8ball(ctx, *, question):

    responses = ['It is certain.',
                'It is decidedly so.',
                'Without a doubt.',
                'Yes - definetly.',
                'You may rely on it',
                'As I see it, yes.',
                'most likely.',
                'Outlook good.',
                'Yes.',
                'Signs point to yes.',
                'Reply hazy, try again.',
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now',
                'Concentrate and ask again.',
                'Don\'t count on it.',
                'my reply is no.',
                'my sources say no.',
                'Outlook not very good',
                'Very doubtful.']

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command(aliases=['Babye', 'bye', 'babye', 'byye', 'Byye', 'babyye', 'byyye'],
 brief='Bye greet.', 
 description="Says bye back.")
async def Bye(ctx):

    await ctx.send("Bye! See you next time.")

@client.command(aliases=['thankyou', 'Thanks', 'ty', 'thanks', 'TY'],
 brief='Thanks greet.', 
 description="Says you're welcome.")
async def Thankyou(ctx):

    responses = ["You're welcome.",
                    'No problem.',
                    'Anytime.']

    await ctx.send(f"{random.choice(responses)}")

@client.command(aliases=['Goodmorning', 'Gm', 'gm', 'gudmorneng'],
 brief="Greets you Good morning.", 
 description="It doesn't greet you good night. :(")
async def goodmorning(ctx):

    await ctx.send("Good morning!")

@client.command(aliases=['Goodnight', 'Gn', 'gn', 'gudnayt'],
 brief="Greets you Good night.", 
 description="It doesn't greet you good morning. :(")
async def goodnight(ctx):

    await ctx.send("Good night!")

@client.command(aliases=['hi', 'Hello', 'hello', 'Hey', 'hey', 'Yo', 'yo', 'Sup', 'sup'],
 brief='Says hi.', 
 description="Command to say hi to the bot.")
async def Whatsup(ctx):

    responses = ['hi~',
                'Hello~',
                'hello~',
                'Hey~',
                'hey~',
                'Yo~',
                'yo~',
                'Sup~',
                'sup~']

    await ctx.send(f"{random.choice(responses)}")

client.run(TOKEN)