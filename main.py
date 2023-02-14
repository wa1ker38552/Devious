from discord.ext import commands
from database import Database
from functions import filter
from colors import *
import discord
import copy
import time
import os

client = commands.Bot(command_prefix=Database('config.json').load()['prefix'], self_bot=True, help_command=None)

def reload_cogs(cog=None):
  if cog is None:
    for file in os.listdir('./cogs'):
      if file.endswith('.py'):
        client.load_extension(f'cogs.{file[:-3]}')
  else:
    client.load_extension(f'cogs.{cog}')


@client.event
async def on_ready():
  Database().set_key('uptime', time.time())
  print(f'{blue}𝔻𝔼𝕍𝕀𝕆𝕌𝕊{white} Client {lime}v{Database("config.json").load()["version"]}{white} loaded!')
  print(f'Hosting on user: {blue}{client.user}{white}')

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, discord.ext.commands.errors.CommandNotFound):
    return
  raise error

@client.event
async def on_message(message):
  Database().set_key('message_processing', time.time())
  if message.author == client.user:
    if message.content.startswith(Database('config.json').load()['prefix']):
      if Database().load()['hidden'] is True:
        reference = copy.copy(message)
        await message.delete()
      
      Database().set_key('message_processing', time.time()-Database().load()['message_processing'])
      Database().set_key('command_processing', time.time())
      await client.process_commands(reference)
  else:
    if not message.channel.id in Database().load()['blacklisted']:
      db = Database().load()
      if message.author.id in db['mocking']:
          async for message in message.channel.history(limit=1): message_content = message.content
            
          if 'https://' in message_content: 
            await message.channel.send(f'`{filter(message_content)}`')
          elif message.mentions: 
            await message.channel.send('Naughty mentions')
          else:
            await message.channel.send(filter(message_content))

      if str(message.author.id) in db['reacting']:
        for reaction in db['reacting'][str(message.author.id)]:
          await message.add_reaction(reaction)

      if str(message.author.id) in db['replying']:
        await message.reply(db['replying'][str(message.author.id)])
      

reload_cogs()
client.run(os.environ[Database("config.json").load()["token"]], bot=False)
