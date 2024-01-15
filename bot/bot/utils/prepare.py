import os

from guilded.ext import commands
import guilded

from bot.utils.db import db as surreal

from dotenv import load_dotenv
from bot.utils.server import get_server, server_initializer, update_server
from bot.utils.server_channel import get_server_channel, server_channel_initializer, update_server_channel
from bot.utils.user import get_user, update_user, user_initializer


load_dotenv()


async def prepare(bot: commands.bot.Bot, message: guilded.Message):
    curr_pre = os.environ["DEFAULT_PREFIX"]
    try:
        # user init
        curr_user_record = await get_user(surreal.db, message.author_id)
        if (message.author) and not message.author.bot_id:
            if not bool(curr_user_record):
                curr_user_record = await user_initializer(surreal.db, message.author)
            else:
                curr_user_record = await update_user(surreal.db, message.author)
        # server init
        curr_server_record = await get_server(surreal.db, message.server_id)
        curr_server: dict[str, str] = curr_server_record  # type: ignore
        if not bool(curr_server_record):
            curr_server_record = await server_initializer(surreal.db, message.server)
        else:
            curr_server_record = await update_server(surreal.db, message.server)
        # channel init
        curr_channel_record = await get_server_channel(surreal.db, message.channel_id)
        if not bool(curr_channel_record):
            server_channels = message.server.channels
            this_channel = None
            for channel in server_channels:
                if channel.id == message.channel_id:
                    this_channel = channel
                    break
            if this_channel:
                curr_channel_record = await server_channel_initializer(
                    surreal.db, this_channel
                )
        else:
            server_channels = message.server.channels
            this_channel = None
            for channel in server_channels:
                if channel.id == message.channel_id:
                    this_channel = channel
                    break
            if this_channel:
                curr_channel_record = await update_server_channel(
                    surreal.db, this_channel
                )
        # curr_channel: dict[str, str] = curr_channel_record  # type: ignore
        curr_pre = curr_server["prefix"]
        return [
            f"{curr_pre} ",
            f"@{os.environ['BOT_NAME']} ",
            f"@{bot.user.display_name}" if bot.user else None,
        ]
    except Exception as e:
        print(e)
        embed = guilded.Embed()
        embed.title = "Error"
        embed.description = f"```{e}```"
        embed.color = guilded.Color.red()
        if message.content.split(" ")[0] in [
            f"{curr_pre}",
            f"{curr_pre} ",
            f"@{os.environ['BOT_NAME']} ",
            f"@{bot.user.display_name}" if bot.user else None,
        ]:
            await message.reply(embed=embed, private=True)
        await message.reply(embed=embed, private=True)
        return [
            f"{curr_pre} ",
            f"@{os.environ['BOT_NAME']} ",
            f"@{bot.user.display_name}" if bot.user else None,
        ]
