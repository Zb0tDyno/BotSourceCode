# import stuff
from keep_alive import keep_alive
import discord
from discord.ext import commands
from asyncio import sleep
import os
import aiohttp
import random
import json
from config import config

cfg = config
primed = False

# Honestly idk what i'm doing here, the warn command needs a shit tone of stuff
with open('reports.json', encoding='utf-8') as f:
  try:
    report = json.load(f)
  except ValueError:
    report = {}
    report['users'] = []

# importing
Creators = os.environ.get('Creators')
nukepword = os.environ.get('NUKEPWORD')

# Version number
Version = cfg.Version

prefix = cfg.BOT_PREFIX

# prefix
client = commands.Bot(command_prefix= prefix, help_command = None)

# if pinged
@client.event
async def on_message(message):
  mention = f'<@!{client.user.id}> prefix'
  if mention in message.content:
    await message.channel.sent(f'<@{message.author.id}> the bots prefix is `mtf `')
  else:
    pass
  await client.process_commands(message)


# on_ready
@client.event
async def on_ready():
    print(client.user.name, ' version=',Version)
    await client.change_presence(activity=discord.Game(name = 'mtf help'))

@client.command()
async def info(ctx):
  embed=discord.Embed(title = 'What is this bot?', descripton = 'This bot was for this server, it is currently a W I P but that will change', color = discord.Colour.blurple())
  embed.add_field(name = 'Who can nuke the server?', value=('anyone with L-5 clearance and above'))
  embed.add_field(name = 'Who can prep the nuke?', value = ('anyone with L-4 clearence and above'))
  embed.add_field(name = 'Developers', value = (Creators))
  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/790716118947594250/842113685643198534/image0.png')
  await ctx.send(embed = embed)

# discharge command
@client.command()
@commands.has_any_role('L-4', 'L-5', 'SCP Omni', 'Phantom Task Force Commander', 'MTF Commander', 'Best Friend')
async def disarm(ctx):
    await sleep(5)
    await ctx.send('warhead disarmed')

# Ban command
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason = None):
        if reason == None:
            reason = "Being a dumbass for breaking the rules"
        author = ctx.author
        authorid= ctx.author.id
        await member.send(f"You have been banned from {ctx.guild.name} for {reason} by {author}, if you want to appeal the ban you can join the appeals server here: https://discord.gg/Wu7Ev3Xcjj")
        await ctx.guild.ban(member, reason=reason)
        await ctx.channel.send(f"{member} has been banned for {reason}.")


# Meme command
@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="Welcome to your daily dose of memes", description=f"<@{ctx.author.id}>", color = (0x4103fc))
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/SCPMemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

# pp size command
@client.command(pass_context = True)
async def pp_size(ctx):
    embed = discord.Embed(title = f"{ctx.author} your pp size is...", description = (random.randint(1, 500)), color = (0xFF0000))
    await ctx.send(embed = embed)

# Secret pp_size command :eyes:
@client.command(pass_context = True)
async def real_pp_size(ctx):
    embed = discord.Embed(title = f"{ctx.author} your pp size is...", description = (random.randint(69420, 6969420)), color = (0xFF0000))
    await ctx.send(embed = embed)
    await ctx.message.delete()

# help command
@client.command()
async def help(ctx):
  embed = discord.Embed(title = 'Help Menu', desc = ('Help menu for the bot'), color = (0x0e0f0f))
  embed.add_field(name = 'prefix', value = ('mtf '))
  embed.add_field(name = 'Commands', value = ('mtf pp_size, mtf meme'))
  embed.add_field(name = 'Mobile Task Forces', value = ('MTF E-11, MTF Nu-7, MTF Beta-7, MTF I-10, MTF Alpha-1'))
  embed.add_field(name = 'Card Levels', value = ('Lvl 1, Lvl 2, Lvl 3, Lvl 4, Lvl 5'))
  embed.set_footer(text = Version)
  embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/790716118947594250/845498944132874320/Mobile_Tast_Force.jpg')
  await ctx.send(embed = embed)

# version check command
@client.command()
async def version(ctx):
  await ctx.send(f'Bot version is {Version}')



# Warnings command
@client.command(pass_context = True)
async def warnings(ctx,user:discord.User):
  for current_user in report['users']:
    if user.name == current_user['name']:
      await client.send(f"{user.name} has been reported {len(current_user['reasons'])} times : {','.join(current_user['reasons'])}")
      break
  else:
    await client.send(f"{user.name} has never been reported")

TOKEN = os.environ.get('TOKEN')
client.run(TOKEN)

keep_alive()
# Created by Zbot
