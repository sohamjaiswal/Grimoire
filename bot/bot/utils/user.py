from enum import Enum
from bot.utils.db import db as surreal

import guilded

from surrealdb.ws import Surreal

class UserReplyPolicy(Enum):
    public = "public"
    private = "private"


async def user_initializer(db: Surreal, user: guilded.User):
    return await db.create(
        f"user:{user.id}", {"name": user.name, "avatar": user.display_avatar.url}
    )

async def get_user(db: Surreal, user_id: str):
    return await db.select(f"user:{user_id}")

async def update_user(db: Surreal, user: guilded.User):
    return await db.merge(
        f"user:{user.id}", {"name": user.name, "avatar": user.display_avatar.url}
    )

async def update_user_policy(user_id: str, command_name: str, policy: UserReplyPolicy):
    curr_policy = await surreal.db.select(f"user_policy:{user_id}")
    try:
        if not bool(curr_policy):
            await surreal.db.create(
                f"user_policy:{user_id}",
                {command_name: policy.value, "user": f"user:{user_id}"},
            )
        else:
            await surreal.db.merge(
                f"user_policy:{user_id}", {command_name: policy.value}
            )
    except Exception as e:
        raise e

async def get_all_user_reply_policies(user_id: str):
    curr_policy_record = await surreal.db.select(f"user_policy:{user_id}")
    curr_policy: dict[str, str] = {}
    if not bool(curr_policy_record):
        return curr_policy
    curr_policy: dict[str, str] = curr_policy_record # type: ignore
    return curr_policy
