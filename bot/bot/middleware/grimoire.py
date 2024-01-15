import inspect
from typing import Callable
from bot.middleware.analytics import apply_command_logging

from bot.middleware.policies import apply_reply_policies

def grimoire(func: Callable):
    @apply_reply_policies
    @apply_command_logging
    async def decorator(*args, **kwargs):
        return await func(*args, **kwargs)
    decorator.__name__ = func.__name__
    decorator.__doc__ = func.__doc__
    decorator.__signature__ = inspect.signature(func)
    return decorator
