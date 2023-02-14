from discord.ext import commands
from database import Database
from main import reload_cogs
from colors import *
import discord
import asyncio
import time
import os

class Utility(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def helpsb(self, ctx, cog=None):
    if cog is None:
      cogs = [f'> **{cog.replace(".py", "")}:** `{Database("config.json").load()["prefix"]}helpsb {cog.replace(".py", "").lower()}`' for cog in os.listdir('./cogs')[1:]]
      await ctx.send('> 𝔻𝔼𝕍𝕀𝕆𝕌𝕊 *COMMANDS*\n'+'\n'.join(cogs))
    else:
      cog = cog[0].upper()+cog[1:].lower()
      if os.path.exists(f'cogs/{cog}.py'):
        with open(f'cogs/{cog}.py', 'r') as file:
          file = file.read()
          commands = []
          prefix = Database("config.json").load()["prefix"]
          for i, line in enumerate(file.split('\n')):
            if line.strip() == '@commands.command()':
              commands.append(file.split('\n')[i+1].replace('async def ', '').replace('):', '').replace('self, ctx, ', '').replace('self, ctx', '')+')')
        
        for i, cmd in enumerate(commands):
          commands[i] = f'> **`{prefix}{cmd.split("(")[0].strip()}`**: `{cmd.strip()}`'
  
        await ctx.send(f'> 𝔻𝔼𝕍𝕀𝕆𝕌𝕊 *{cog}*\n'+'\n'.join(commands))
      else:
        await ctx.send(f'> Could not load `cogs/{cog}.py`')

  @commands.command()
  async def debug(self, ctx):
    info = [
      f'> **Version:** `{Database().load()["version"]}`',
      f'> **Client:** `{self.client.user}`',
      f'> **Uptime:** `{round((time.time()/Database().load()["uptime"])/60/60, 3)}` hrs\n> ',
      f'> **Message Processing:** `{round(Database().load()["message_processing"], 3)}` s',
      f'> **Command Processing:** `{round(time.time()-Database().load()["command_processing"], 3)}` s',
      f'> **Latency:** `{round(self.client.latency, 3)}` ms\n> ',
      f'> **Cogs:** `{len(os.listdir("./cogs"))-1}`'
    ]
    await ctx.send('> 𝔻𝔼𝕍𝕀𝕆𝕌𝕊 Client\n'+'\n'.join(info))

  @commands.command()
  async def refresh(self, ctx, cog=None):
    if cog is None:
      try:
        reload_cogs()
        await ctx.send(f'> Refreshed `{len(os.listdir("./cogs"))-1}` cogs')
      except discord.ext.commands.errors.ExtensionAlreadyLoaded:
        await ctx.send('> Cogs were recently reloaded!') 
    else:
      try:
        reload_cogs(f'{cog[0].upper()}{cog[1:]}')
        await ctx.send(f'> Refreshed `cogs.{cog[0].upper()}{cog[1:]}`')
      except discord.ext.commands.errors.ExtensionAlreadyLoaded:
        await ctx.send(f'> `cogs.{cog[0].upper()}{cog[1:]}` was recently reloaded!')
      except discord.ext.commands.errors.ExtensionNotFound:
        await ctx.send(f'> `cogs.{cog[0].upper()}{cog[1:]}` does not exist')

  @commands.command()
  async def src(self, ctx, command, file='main.py'):
    if os.path.exists(file):
      with open(file, 'r') as file:
        data = file.read().split('\n')
        for x, line in enumerate(data):
          if f'async def {command}' in line:
            for y in range(x, len(data)):
              if data[y].strip() == '@commands.command()':
                await ctx.send(f'{codeblock}py\n'+'\n'.join(data[x:y])+codeblock)
                return
            await ctx.send(f'> Error while reading lines `{x}, {y}`')
        await ctx.send(f'> Error while indexing `{command}`')
    else:
      await ctx.send(f'> `{file}` does not exist')

  @commands.command()
  async def avatar(self, ctx, member: discord.User):
    await ctx.send(member.avatar_url)

  @commands.command()
  async def icon(self, ctx):
    try:
      await ctx.send(ctx.guild.icon_url)
    except AttributeError:
      await ctx.send('> Try `!icon` on a guild')

  @commands.command()
  async def delete(self, ctx, limit=10, check_limit=100, sleep=0.5):
    counter, i = 0, 0
    async for message in ctx.channel.history(limit=check_limit):
      i += 1
      if counter == limit: break
      if message.author.id == self.client.user.id:
        await message.delete()
        await asyncio.sleep(sleep)
        counter += 1

    await ctx.send(f'> Succesfully scanned `{i}` ({i/check_limit*100}%) messages and deleted `{limit}`')

  @commands.command()
  async def prefix(self, ctx, prefix):
    Database().set_key('prefix', prefix)
    self.client.command_prefix = prefix
    await ctx.send(f'> Successfully set prefix to `{prefix}`')

  @commands.command()
  async def blacklist(self, ctx, id):
    db = Database().load()
    db['blacklisted'].append(int(id))
    Database().set_key('blacklisted', db['blacklisted'])
    await ctx.send(f'> Succesfully blacklisted `{id}`')

  @commands.command()
  async def unblacklist(self, ctx, id: int):
    db = Database().load()
    if id in db['blacklisted']:
      db['blacklisted'].remove(id)
      Database().set_key('blacklisted', db['blacklisted'])
      await ctx.send(f'> Succesfully removed `{id}` from blacklisted servers')
    else:
      await ctx.send(f'> Server `{id}` is not blacklisted')

  @commands.command()
  async def blacklisted(self, ctx):
    await ctx.send('\n'.join([f'> `{i}`' for i in Database().load()['blacklisted']]))

  @commands.command()
  async def viewconfig(self, ctx, key=None):
    db = Database().load()
    if key is None:
      await ctx.send('\n'.join([f'> `{conf}`: `{str(db[conf])}`' for conf in db]))
    else:
      if key in db:
        await ctx.send(f'> `{key}`: `{str(db[key])}`')
      else:
        await ctx.send(f'> `{key}` is not a config')

def setup(client):
  client.add_cog(Utility(client))
