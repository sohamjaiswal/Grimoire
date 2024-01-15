from typing import Union
from guilded.ext import commands

from bot.utils.embeds import GrimEmbeds
from bot.utils.user import UserReplyPolicy as Policy, update_user_policy, get_all_user_reply_policies


class Own(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embeds = GrimEmbeds(bot)
        self._command_name_list: Union[list[str], None] = None

    def _refresh_command_name_list(self):
        cogs = self.bot.cogs
        command_name_list: list[str] = []
        for cog in cogs:
            cog = cogs[cog]
            for command in cog.get_commands():
                command_name_list.append(command.name)
        self._command_name_list = command_name_list

    @commands.group(invoke_without_command=True)
    async def own(self, ctx: commands.Context):
        """
        Used to set your own preferences.

        Args:
            See subcommands.
        """
        embed = self.embeds.get_error_embed(
            ctx.message, title="Own", dsc="Use a subcommand."
        )
        await ctx.reply(embed=embed, private=True)

    @own.command()
    async def review(self, ctx: commands.Context):
        """
        Overview:
        Shows your current preferences.
        """
        if not ctx.message.author:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Getting Preferences", dsc="User not found."
            )
            await ctx.reply(embed=embed, private=True)
            return
        policies = await get_all_user_reply_policies(ctx.message.author.id)
        
        embed = self.embeds.get_success_embed(
            ctx.message, title="Server Settings", dsc="Server Settings:"
        )
        for policy in policies:
            if policy == 'id':
                continue
            elif policy == 'user':
                continue
            else:
                embed.add_field(name=policy, value=policies[policy], inline=True)
        await ctx.reply(embed=embed, private=True)

    @own.group(invoke_without_command=True)
    async def policy(self, ctx: commands.Context):
        """
        Overview:
        Sets your policy of a command.
        Public: The bot will respond to you publicly when using the referenced command.
        Private: The bot will respond to you privately when using the referenced command.
        Note:
        Your policy will be overriden by message args and server policy.
        Usage:
        policy: enum = "public" | "private"
        command_name: str = The command name to set the policy for.
        """
        # get command name the policy is being set for
        if not self._command_name_list:
            self._refresh_command_name_list()

        if not bool(self._command_name_list):
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Getting Commands", dsc="Bot error."
            )
            await ctx.reply(embed=embed, private=True)
            return

        embed = self.embeds.get_error_embed(
            ctx.message,
            title="Setting Policy",
            dsc=f"Enter subcommand for private/public...\n\n Commands:\n{str.join(', ', self._command_name_list)}",
        )
        await ctx.reply(embed=embed, private=True)

    @policy.group()
    async def public(self, ctx: commands.Context, *, command_name: str):
        """
        Overview:
        Sets your policy of a command to public.
        Note:
        Your policy will be overriden by message args and server policy.
        Usage:
        command_name: str = The command name to set the policy for.
        """
        if not self._command_name_list:
            self._refresh_command_name_list()

        if not bool(self._command_name_list):
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting Policy", dsc="Bot error."
            )
            await ctx.reply(embed=embed, private=True)
            return

        if command_name not in self._command_name_list:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting Policy", dsc="Command not found."
            )
            await ctx.reply(embed=embed, private=True)
            return

        if not ctx.message.author:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting Policy", dsc="User not found."
            )
            await ctx.reply(embed=embed, private=True)
            return

        try:
            await update_user_policy(
                ctx.message.author.id, command_name, Policy("public")
            )
        except Exception as e:
            embed = self.embeds.get_error_embed(
                ctx.message,
                title="Error Setting Policy",
                dsc=f"Something went wrong.\n\n'''{e}'''",
            )
            await ctx.reply(embed=embed, private=True)
            return

        embed = self.embeds.get_success_embed(
            ctx.message,
            title="Policy",
            dsc="Policy set to public.\n\nNote: Your policy will be overriden by message args and server policy.",
        )
        await ctx.reply(embed=embed, private=True)

    @policy.group()
    async def private(self, ctx: commands.Context, *, command_name: str):
        """
        Overview:
        Sets your policy of a command to public.
        Note:
        Your policy will be overriden by message args and server policy.
        Usage:
        command_name: str = The command name to set the policy for.
        """
        if not self._command_name_list:
            self._refresh_command_name_list()

        if not bool(self._command_name_list):
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting Policy", dsc="Bot error."
            )
            await ctx.reply(embed=embed, private=True)
            return

        if command_name not in self._command_name_list:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting Policy", dsc="Command not found."
            )
            await ctx.reply(embed=embed, private=True)
            return

        if not ctx.message.author:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting Policy", dsc="User not found."
            )
            await ctx.reply(embed=embed, private=True)
            return

        try:
            await update_user_policy(
                ctx.message.author.id, command_name, Policy("private")
            )
        except Exception as e:
            embed = self.embeds.get_error_embed(
                ctx.message,
                title="Error Setting Policy",
                dsc=f"Something went wrong.\n\n'''{e}'''",
            )
            await ctx.reply(embed=embed, private=True)
            return

        embed = self.embeds.get_success_embed(
            ctx.message,
            title="Policy",
            dsc="Policy set to private.\n\nNote: Your policy will be overriden by message args and server policy.",
        )
        await ctx.reply(embed=embed, private=True)


def setup(bot: commands.Bot):
    bot.add_cog(Own(bot))
