from discord.ext import commands
from database import Database
import discord
import asyncio


class Trolling(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.letters = 'abcdefghijklmnopqrstuvwxyz1234567890'
    
  @commands.command()
  async def ghostping(self, ctx, id='@everyone'):
    if id == '@everyone':
      message = await ctx.channel.send(id)
    else:
      message = await ctx.channel.send(f'<@{id}>')
    await message.delete()

  @commands.command()
  async def typing(self, ctx, seconds: int):
    await ctx.send(f'> Typing on channel `{ctx.channel.id}` for `{round(seconds/60/60)}` hours')
    async with ctx.channel.typing():
      await asyncio.sleep(seconds)

  @commands.command()
  async def massreact(self, ctx, emoji, limit: int=20, check_limit: int=100, include_self='true'):
    c = 0
    async for message in ctx.channel.history(limit=check_limit):
      if message.author == self.client.user.id:
        if include_self == 'true':
          await message.add_reaction(emoji)
          c += 1
      else:
        await message.add_reaction(emoji)
        c += 1

  @commands.command()
  async def charreact(self, ctx, text, check_limit=100):
    emojis = open('assets/emoji_chars.txt', 'r').read().split('\n')
    if ctx.message.reference is not None:
      async for message in ctx.message.channel.history(limit=check_limit):
        if message.id == ctx.message.reference.message_id:
          for char in text.lower():
            await message.add_reaction(emojis[self.letters.index(char)])
          break
    else:
      await ctx.send(f'> You must reply to a message with `{Database().load()["prefix"]}charreact {text}` to use this command')

def setup(client):
  client.add_cog(Trolling(client))
