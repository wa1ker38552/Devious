from discord.ext import commands
from database import Database
import discord


class Automation(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def mock(self, ctx, member: discord.User=None):
    db = Database().load()
    if member is None:
      Database().set_key('mocking', [])
      await ctx.send(f'> Stopped mocking `{len(db["mocking"])}` users')
    else:
      if member.id in db['mocking']:
        await ctx.send(f'> `{await self.client.fetch_user(member.id)}` is already being mocked')
      else:
        if member.id != self.client.user.id:
          db['mocking'].append(member.id)
          Database().set_key('mocking', db['mocking'])
          await ctx.send(f'> Mocking `{await self.client.fetch_user(member.id)}`')
        else:
          await ctx.send(f'> Avoiding recursive loop...')

  @commands.command()
  async def endmock(self, ctx, member: discord.User=None):
    db = Database().load()
    if member is None:
      Database().set_key('reacting', {})
      if len(db["reacting"]) != 1:
        await ctx.send(f'> Stopped mocking `{len(db["reacting"])}` users')
      else:
        await ctx.send('> Stopped mocking `1` user')
    else:
      if member.id in db['mocking']:
        db['mocking'].remove(member.id)
        Database().set_key('mocking', db['mocking'])
        await ctx.send(f'> Stopped mocking `{await self.client.fetch_user(member.id)}`')
      else:
        await ctx.send(f'> {await self.client.fetch_user(member.id)}` is not currently being mocked')

  @commands.command()
  async def mocking(self, ctx):
    if Database().load()['mocking']:
      await ctx.send('\n'.join([f'> `{await self.client.fetch_user(id)}`' for id in Database().load()['mocking']]))
    else:
      await ctx.send('> Nobody is currently being mocked')

  @commands.command()
  async def react(self, ctx, member: discord.User, emoji):
    db = Database().load()
    if str(member.id) in db['reacting']:
      await ctx.send(f'> `{await self.client.fetch_user(member.id)}` is already being reacted to')
    else:
      db['reacting'][member.id] = list(emoji)
      Database().set_key('reacting', db['reacting'])
      await ctx.send(f'> Reacting to `{await self.client.fetch_user(member.id)}` with {", ".join(list(emoji))}')

  @commands.command()
  async def endreact(self, ctx, member: discord.User=None):
    db = Database().load()
    if member is None:
      Database().set_key('reacting', {})
      if len(db["reacting"]) != 1:
        await ctx.send(f'> Stopped reacting to `{len(db["reacting"])}` users')
      else:
        await ctx.send('> Stopped reacting to `1` user')
    else:
      if str(member.id) in db['reacting']:
        del db['reacting'][str(member.id)]
        Database().set_key('reacting', db['reacting'])
        await ctx.send(f'> Stopped reacting to `{await self.client.fetch_user(member.id)}`')
      else:
        await ctx.send(f'> {await self.client.fetch_user(member.id)}` is not currently being reacted to')

  @commands.command()
  async def reacting(self, ctx):
    db = Database().load()['reacting']
    if db:
      await ctx.send('\n'.join([f'> `{await self.client.fetch_user(int(id))}`: {", ".join(db[id])}' for id in db]))
    else:
      await ctx.send('> Nobody is being reacted to')

  @commands.command()
  async def reply(self, ctx, member: discord.User, *message):
    message = ' '.join(message)
    db = Database().load()
    if str(member.id) in db['replying']:
      await ctx.send(f'> `{await self.client.fetch_user(member.id)}` is already being replied to')
    else:
      if member.id != self.client.user.id:
        db['replying'][member.id] = message
        Database().set_key('replying', db['replying'])
        await ctx.send(f'> Replying to `{await self.client.fetch_user(member.id)}` with `{message}`')
      else:
        await ctx.send(f'> Avoiding recursive loop...')

  @commands.command()
  async def endreply(self, ctx, member: discord.User=None):
    db = Database().load()
    if member is None:
      Database().set_key('replying', {})
      if len(db["replying"]) != 1
        await ctx.send(f'> Stopped replying to `{len(db["replying"])}` users')
    else:
      await ctx.send('> Stopped replying to `1` user')
    else:
      if str(member.id) in db['replying']:
        del db['replying'][str(member.id)]
        Database().set_key('replying', db['replying'])
        await ctx.send(f'> Stopped replying to `{await self.client.fetch_user(member.id)}`')
      else:
        await ctx.send(f'> {await self.client.fetch_user(member.id)}` is not currently being replied to')

  @commands.command()
  async def replying(self, ctx):
    db = Database().load()['replying']
    if db:
      await ctx.send('\n'.join([f'> `{await self.client.fetch_user(int(id))}`: `{db[id]}`' for id in db]))
    else:
      await ctx.send('> Nobody is being replied to')

def setup(client):
  client.add_cog(Automation(client))
