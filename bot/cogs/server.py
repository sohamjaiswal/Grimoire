from typing import Union
from guilded.ext import commands

from bot.utils.embeds import GrimEmbeds
from bot.utils.server import ServerReplyPolicy, update_server_reply_policy, get_all_server_reply_policies


class Server(commands.Cog):
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
    async def server(self, ctx: commands.Context):
        """
        Used to set your own preferences.

        Args:
            See subcommands.
        """
        embed = self.embeds.get_error_embed(
            ctx.message, title="Server Settings", dsc="Use a subcommand."
        )
        await ctx.reply(embed=embed, private=True)
    
    @server.command()
    async def review(self, ctx: commands.Context):
      '''
      Overview:
      Review the server settings.
      '''
      policies = await get_all_server_reply_policies(ctx.message.server_id)
      embed = self.embeds.get_success_embed(
          ctx.message, title="Server Settings", dsc="Server Settings:"
      )
      for policy in policies:
        if policy == 'id':
          continue
        elif policy == 'server':
          continue
        else:
          embed.add_field(name=policy, value=policies[policy], inline=True)
      await ctx.reply(embed=embed, private=True)

    @server.group(invoke_without_command=True)
    async def policy(self, ctx: commands.Context):
      '''
      Overview:
      Set reply and command_sd policy for the server.
      '''
      embed = self.embeds.get_error_embed(
          ctx.message, title="ServerPolicy", dsc="Use a subcommand.\n\nSubcommands: reply, command_sd"
      )
      await ctx.reply(embed=embed, private=True)
      return
    
    @policy.group()
    async def comamnd_sd(self, ctx: commands.Context, delete_time: int = -1):
      # set self destruct to delete_time, no self destruct if delete_time is -1
      pass
    
    @policy.group(invoke_without_command=True)
    async def reply(self, ctx: commands.Context, *, command_name:str):
      """
      Overview:
      Sets your reply policy of a command issued on this server.
      Public: The bot will respond to you publicly when using the referenced command.
      Private: The bot will respond to you privately when using the referenced command.
      Note:
      Server policy is overridden by channel policy.
      Usage:
      policy: enum = "public" | "private" | "default" | "disallowed"
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
          title="Setting ServerReplyPolicy",
          dsc=f"Enter subcommand for private/public...\n\n Commands:\n{str.join(', ', self._command_name_list)}",
      )
      await ctx.reply(embed=embed, private=True)

  
    @reply.group()
    @commands.has_server_permissions(manage_bots=True)
    async def public(self, ctx: commands.Context, *, command_name: str):
        """
        Overview:
        Sets your policy of a command to public.
        Usage:
        command_name: str = The command name to set the policy for.
        """
        if not self._command_name_list:
            self._refresh_command_name_list()

        if not bool(self._command_name_list):
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting ServerReplyPolicy", dsc="Bot error."
            )
            await ctx.reply(embed=embed, private=True)
            return

        if command_name not in self._command_name_list:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting ServerReplyPolicy", dsc="Command not found."
            )
            await ctx.reply(embed=embed, private=True)
            return

        if not ctx.message.server_id:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting ServerReplyPolicy", dsc="Server not found."
            )
            await ctx.reply(embed=embed, private=True)
            return

        try:
            await update_server_reply_policy(
                ctx.message.server_id, command_name, ServerReplyPolicy("public")
            )
        except Exception as e:
            embed = self.embeds.get_error_embed(
                ctx.message,
                title="Error Setting ServerReplyPolicy",
                dsc=f"Something went wrong.\n\n'''{e}'''",
            )
            await ctx.reply(embed=embed, private=True)
            return

        embed = self.embeds.get_success_embed(
            ctx.message,
            title="ServerReplyPolicy",
            dsc="ServerReplyPolicy set to public.\n\nNote: Your policy will be overriden by channel policy.",
        )
        await ctx.reply(embed=embed, private=True)

    @reply.group()
    @commands.has_server_permissions(manage_bots=True)
    async def private(self, ctx: commands.Context, *, command_name: str):
        """
        Overview:
        Sets server policy of a command to enforce private reply, useful for active channels.
        Usage:
        command_name: str = The command name to set the policy for.
        """
        if not self._command_name_list:
            self._refresh_command_name_list()

        if not bool(self._command_name_list):
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting ServerReplyPolicy", dsc="Bot error."
            )
            await ctx.reply(embed=embed, private=True)
            return

        if command_name not in self._command_name_list:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting ServerReplyPolicy", dsc="Command not found."
            )
            await ctx.reply(embed=embed, private=True)
            return

        try:
            await update_server_reply_policy(
                ctx.message.server_id, command_name, ServerReplyPolicy("private")
            )
        except Exception as e:
            embed = self.embeds.get_error_embed(
                ctx.message,
                title="Error Setting ServerReplyPolicy",
                dsc=f"Something went wrong.\n\n'''{e}'''",
            )
            await ctx.reply(embed=embed, private=True)
            return

        embed = self.embeds.get_success_embed(
            ctx.message,
            title="ServerReplyPolicy",
            dsc="ServerReplyPolicy set to private.\n\nNote: Your policy will be overriden by message args and server policy.",
        )
        await ctx.reply(embed=embed, private=True)
    
    @reply.group()
    @commands.has_server_permissions(manage_bots=True)
    async def default(self, ctx: commands.Context, *, command_name: str):
        """
        Overview:
        Sets server policy of a command to default (i.e. be overriden by channel/message/user policy).
        Usage:
        command_name: str = The command name to set the policy for.
        """
        if not self._command_name_list:
            self._refresh_command_name_list()

        if not bool(self._command_name_list):
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting ServerReplyPolicy", dsc="Bot error."
            )
            await ctx.reply(embed=embed, private=True)
            return

        if command_name not in self._command_name_list:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting ServerReplyPolicy", dsc="Command not found."
            )
            await ctx.reply(embed=embed, private=True)
            return

        try:
            await update_server_reply_policy(
                ctx.message.server_id, command_name, ServerReplyPolicy("default")
            )
        except Exception as e:
            embed = self.embeds.get_error_embed(
                ctx.message,
                title="Error Setting ServerReplyPolicy",
                dsc=f"Something went wrong.\n\n'''{e}'''",
            )
            await ctx.reply(embed=embed, private=True)
            return

        embed = self.embeds.get_success_embed(
            ctx.message,
            title="ServerReplyPolicy",
            dsc="ServerReplyPolicy set to private.\n\nNote: Your policy will be overriden by message args and server policy.",
        )
        await ctx.reply(embed=embed, private=True)
        
    @reply.group()
    @commands.has_server_permissions(manage_bots=True)
    async def disallowed(self, ctx: commands.Context, *, command_name: str):
        """
        Overview:
        Sets server policy of a command to disallowed.
        Usage:
        command_name: str = The command name to set the policy for.
        """
        if not self._command_name_list:
            self._refresh_command_name_list()

        if not bool(self._command_name_list):
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting ServerReplyPolicy", dsc="Bot error."
            )
            await ctx.reply(embed=embed, private=True)
            return

        if command_name not in self._command_name_list:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error Setting ServerReplyPolicy", dsc="Command not found."
            )
            await ctx.reply(embed=embed, private=True)
            return

        try:
            await update_server_reply_policy(
                ctx.message.server_id, command_name, ServerReplyPolicy("disallowed")
            )
        except Exception as e:
            embed = self.embeds.get_error_embed(
                ctx.message,
                title="Error Setting ServerReplyPolicy",
                dsc=f"Something went wrong.\n\n'''{e}'''",
            )
            await ctx.reply(embed=embed, private=True)
            return

        embed = self.embeds.get_success_embed(
            ctx.message,
            title="ServerReplyPolicy",
            dsc="ServerReplyPolicy set to private.\n\nNote: Your policy will be overriden by message args and server policy.",
        )
        await ctx.reply(embed=embed, private=True)


def setup(bot: commands.Bot):
    bot.add_cog(Server(bot))
