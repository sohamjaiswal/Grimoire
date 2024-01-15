import inspect
import shlex
from typing import Callable
from guilded.ext import commands
from bot.utils.db import db as surreal
import guilded
from bot.utils.embeds import inv_res_color_map

async def add_command_log(ctx: commands.Context, res_emb: guilded.Embed):
  command = ctx.command.root_parent if ctx.command and ctx.command.parent else ctx.command
  message_id = ctx.message.id
  user_id = ctx.message.author_id
  server_id = ctx.message.server_id
  channel_id = ctx.message.channel_id
  exact = shlex.split(ctx.message.content, posix=True)
  emb_color: guilded.Color = res_emb.color # type: ignore
  res_type = inv_res_color_map[emb_color]
  if command and command.name:
    try:
      await surreal.db.query(
        f'''
          create command_log:`{message_id}` 
          set time = time::now(), 
          author = user:{user_id}, 
          server = server:{server_id}, 
          channel = channel:`{channel_id}`, 
          command = "{command.name}", 
          exact = {exact}, 
          result = "{res_type}"
        '''
      )
    except Exception as e:
      print('error', e)
  return

def apply_command_logging(func: Callable):
  async def decorator(*args, **kwargs):
    context: commands.Context = args[1]
    res  = await func(*args, **kwargs)
    await add_command_log(context, res)
    print('res', res)
    return res
  decorator.__name__ = func.__name__
  decorator.__doc__ = func.__doc__
  decorator.__signature__ = inspect.signature(func)
  return decorator
