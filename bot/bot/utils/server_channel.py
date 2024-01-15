from bot.utils.server import server_initializer
from surrealdb.ws import Surreal
import guilded

async def server_channel_initializer(db: Surreal, channel: guilded.abc.ServerChannel):
    curr_server_record = await db.select(f"server:{channel.server_id}")
    if not bool(curr_server_record):
        curr_server_record = await server_initializer(db, channel.server)
    return await db.create(
        f"channel:`{channel.id}`",
        {
            "name": channel.name,
            "server": f"server:{channel.server_id}",
            "type": channel.type.value,
        },
    )

async def get_server_channel(db: Surreal, channel_id: str):
    return await db.select(f"channel:`{channel_id}`")

async def update_server_channel(db: Surreal, channel: guilded.abc.ServerChannel):
    curr_server_record = await db.select(f"server:{channel.server_id}")
    if not bool(curr_server_record):
        curr_server_record = await server_initializer(db, channel.server)
    return await db.merge(
        f"channel:`{channel.id}`",
        {"name": f'{channel.name}', "server": f"server:{channel.server_id}", "type": channel.type.value},
    )
