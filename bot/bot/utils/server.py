from enum import Enum
from bot.utils.db import db as surreal
from bot.utils.user import user_initializer

from surrealdb.ws import Surreal

import guilded


class ServerReplyPolicy(Enum):
    public = "public"
    private = "private"
    default = "default"
    disallowed = "disallowed"


async def server_initializer(db: Surreal, server: guilded.Server):
    # check if server owner in user table, initialize if not
    if not bool(await db.select(f"user:{server.owner_id}")):
        owner = await server.fetch_member(server.owner_id)
        await user_initializer(db, owner)
    return await db.create(
        f"server:{server.id}",
        {
            "prefix": "/grim",
            "name": server.name,
            "slug": server.slug,
            "owner": f"user:{server.owner_id}",
        },
    )

async def get_server(db: Surreal, server_id: str):
    return await db.select(f"server:{server_id}")

async def update_server(db: Surreal, server: guilded.Server):
    if not bool(await db.select(f"user:{server.owner_id}")):
        owner = await server.fetch_member(server.owner_id)
        await user_initializer(db, owner)
    return await db.merge(
        f"server:{server.id}",
        {"name": server.name, "slug": server.slug, "owner": f"user:{server.owner_id}"},
    )


async def update_server_reply_policy(
    server_id: str, command_name: str, policy: ServerReplyPolicy
):
    curr_policy = await surreal.db.select(f"server_policy:{server_id}")
    try:
        if not bool(curr_policy):
            await surreal.db.create(
                f"server_policy:{server_id}",
                {command_name: policy.value, "server": f"server:{server_id}"},
            )
        else:
            await surreal.db.merge(
                f"server_policy:{server_id}", {command_name: policy.value}
            )
    except Exception as e:
        raise e


async def get_all_server_reply_policies(server_id: str):
    curr_policy_record = await surreal.db.select(f"server_policy:{server_id}")
    curr_policy: dict[str, str] = {}
    if not bool(curr_policy_record):
        return curr_policy
    curr_policy: dict[str, str] = curr_policy_record  # type: ignore
    return curr_policy
