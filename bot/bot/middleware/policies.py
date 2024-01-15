import inspect
from typing import Union, Callable
from bot.utils.db import db as surreal
from guilded.ext import commands
from guilded import Embed, Color

from bot.utils.server import ServerReplyPolicy
from bot.utils.user import UserReplyPolicy


async def get_user_private_reply_policy(user_id: str, command_name: str):
    curr_policy_record = await surreal.db.select(f"user_policy:{user_id}")
    if not bool(curr_policy_record):
        return UserReplyPolicy('private')
    curr_policy: dict[str, str] = curr_policy_record  # type: ignore
    try:
        return UserReplyPolicy(curr_policy[command_name])
    except Exception as e:
        print(e)
        return UserReplyPolicy('private')

async def get_server_private_reply_policy(server_id: str, command_name: str):
    curr_policy_record = await surreal.db.select(f"server_policy:{server_id}")
    if not bool(curr_policy_record):
        return ServerReplyPolicy('default')
    curr_policy: dict[str, str] = curr_policy_record  # type: ignore
    try:
        return ServerReplyPolicy(curr_policy[command_name])
    except Exception as e:
        print(e)
        return ServerReplyPolicy('default')


def apply_reply_policies(func: Callable):
    async def decorator(*args, **kwargs):
        # get command name from ctx
        context: commands.Context = args[1]
        print('reached', context)
        root_parent = (
            context.command.root_parent
            if context.command and context.command.parent
            else context.command
        )
        private:bool = kwargs.pop("private", True)
        user_reply_policy: Union[UserReplyPolicy, None] = None
        server_reply_policy: Union[ServerReplyPolicy, None] = None
        # apply user reply policy
        user_reply_policy = await get_user_private_reply_policy(
            args[1].message.author.id,
            root_parent.name
            if root_parent
            else context.command.name
            if context.command
            else "",
        )
        # apply server reply policy
        server_reply_policy = await get_server_private_reply_policy(
            args[1].message.server_id,
            root_parent.name
            if root_parent
            else context.command.name
            if context.command
            else "",
        )
        if server_reply_policy == ServerReplyPolicy.disallowed:
          embed = Embed()
          embed.title = "Error"
          embed.description = "This command is disabled in this server."
          embed.color = Color.red()
          await context.reply(embed=embed, private=True)
          context.message.delete()
          return
        if user_reply_policy == UserReplyPolicy.private:
            private = True
        elif user_reply_policy == UserReplyPolicy.public:
            private = False
        if server_reply_policy == ServerReplyPolicy.private:
            private = True
        elif server_reply_policy == ServerReplyPolicy.public:
            private = False
          
        result: Embed = await func(*args, **kwargs)
        await context.reply(embed=result, private=private)
        return result

    decorator.__name__ = func.__name__
    decorator.__doc__ = func.__doc__
    decorator.__signature__ = inspect.signature(func)
    return decorator
