from glob import glob
from bot.utils.embeds import GrimEmbeds
from bot.utils.prepare import prepare
from bot.utils.db import db as surreal
from bot.utils.help import helper

import asyncio
import os

from guilded.ext import commands

# from dotenv import load_dotenv
# load_dotenv()


def check_environment_keys(keys: list[str]):
    """
    Check if all keys in the given array exist in the environment variables.

    :param keys: List of strings representing keys to check.
    :raises: ValueError if any key is missing.
    """
    missing_keys: list[str] = [key for key in keys if key not in os.environ]

    if missing_keys:
        error: str = f"Missing environment variable keys: {', '.join(missing_keys)}"
        raise ValueError(error)


check_environment_keys(
    ["BOT_TOKEN", "BOT_NAME", "DEFAULT_PREFIX", "DB_HOST", "DB_USER", "DB_PASSWORD", "CONSUMET_HOST"]
)

cogspath = "cogs/"
cogspathpy = [os.path.basename(f) for f in glob(f"{cogspath}*.py")]
cogs = [f"{cogspath[:-1]}." + os.path.splitext(f)[0] for f in cogspathpy]

bot = commands.Bot(command_prefix=prepare, help_command=helper)  # type: ignore
embeds = GrimEmbeds(bot)

@bot.event
async def on_ready():
    await surreal.test_connect()
    embeds = GrimEmbeds(bot)
    print("Ready")


@bot.event
async def on_disconnect():
    print("Disconnected")
    await surreal.db.close()

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.errors.CommandNotFound):
        embed = embeds.get_error_embed(
            ctx.message, title="Command not found", dsc="No command found."
        )
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        embed = embeds.get_error_embed(
            ctx.message,
            title="Missing required argument",
            dsc="You are missing a required argument.",
        )
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.errors.CommandOnCooldown):
        embed = embeds.get_error_embed(
            ctx.message,
            title="Command on cooldown",
            dsc=f"Command is on cooldown. Try again in {error.retry_after:.2f} seconds.",
        )
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.errors.BadArgument):
        embed = embeds.get_error_embed(
            ctx.message,
            title="Bad argument",
            dsc="You have provided a bad argument.",
        )
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.errors.MissingPermissions):
        embed = embeds.get_error_embed(
            ctx.message,
            title="Missing permissions",
            dsc="You are missing permissions to run this command.",
        )
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.errors.NotOwner):
        embed = embeds.get_error_embed(
            ctx.message,
            title="Not owner",
            dsc="You are not the owner of this bot.",
        )
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.errors.ExtensionAlreadyLoaded):
        embed = embeds.get_error_embed(
            ctx.message,
            title="Extension already loaded",
            dsc="This extension is already loaded.",
        )
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.errors.ExtensionNotFound):
        embed = embeds.get_error_embed(
            ctx.message,
            title="Extension not found",
            dsc="This extension was not found.",
        )
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.errors.ExtensionNotLoaded):
        embed = embeds.get_error_embed(
            ctx.message,
            title="Extension not loaded",
            dsc="This extension is not loaded.",
        )
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.errors.ExtensionFailed):
        embed = embeds.get_error_embed(
            ctx.message,
            title="Extension failed",
            dsc="This extension failed to load.",
        )
        await ctx.reply(embed=embed)
        

async def rotate_statuses():
    statuses = [
        "online",
        "Reading the Grimoire...",
        "Bringing magic to Guilded...",
    ]
    i = 0
    while True:
        await bot.wait_until_ready()
        if bot.is_ready():
            await bot.set_status(emote=2200591, content=statuses[i])
            i += 1
            print("Status changed")
            if i == len(statuses):
                i = 0
            await asyncio.sleep(30)
        else:
            continue

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except commands.errors.ExtensionAlreadyLoaded:
            pass
    tasks = asyncio.gather(bot.start(os.environ["BOT_TOKEN"]), rotate_statuses())
    try:
        loop.run_until_complete(tasks)
    except KeyboardInterrupt:
        loop.run_until_complete(bot.set_status(emote=2200576, content="offline"))
        loop.run_until_complete(bot.close())


if __name__ == "__main__":
    main()
