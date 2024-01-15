from bot.utils.embeds import GrimEmbeds
from guilded.ext import commands


class CustomHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.help_embeds = None

    def _get_embeds(self):
        if self.help_embeds is None:
            self.help_embeds = GrimEmbeds(self.context.bot)
        return self.help_embeds

    async def send_bot_help(self, mapping):
        embed = (
            self._get_embeds()
            .get_info_embed(
                self.context.message,
                title="Grimoire Index",
                dsc="Normal text is spells you can run straight.\n\n__Underline__ and *italicized* text is a group for sub spells you can access.",
            )
            .set_thumbnail(
                url="https://cdn-icons-png.flaticon.com/512/2407/2407510.png"
            )
        )
        for cog in mapping:
            if cog is None:
                continue
            else:
                embed.add_field(
                    name=cog.qualified_name,
                    value=f"{str.join('\n',[f'__*{command.name}*__' if isinstance(command, commands.Group) else command.name for command in mapping[cog]])}",
                    inline=True,
                )
        await self.context.message.reply(embed=embed, private=True)
        await self.context.message.delete()

    async def send_cog_help(self, cog):
        embed = (
            self._get_embeds()
            .get_info_embed(
                self.context.message,
                title="Grimoire Index",
                dsc=f"Unravelling {cog.qualified_name}'s sub spells...",
            )
            .set_thumbnail(
                url="https://cdn-icons-png.flaticon.com/512/2407/2407510.png"
            )
        )
        for command in cog.get_commands():
            embed.add_field(name=f"{', '.join([command.name, command.aliases])}", value=command.help, inline=False)
        await self.context.message.reply(embed=embed, private=True)
        await self.context.message.delete()

    async def send_group_help(self, group):
        embed = (
            self._get_embeds()
            .get_info_embed(
                self.context.message,
                title="Grimoire Index",
                dsc=f"If the {group.name} rune glows, it does not need a sub spell.",
            )
            .set_thumbnail(
                url="https://cdn-icons-png.flaticon.com/512/2407/2407510.png"
            )
        )
        if group.help:
            embed.add_field(name=', '.join([group.name, ', '.join(group.aliases)]), value=f'This rune radiates a light...\n{group.help}', inline=False)
        else:
            embed.add_field(name=', '.join([group.name, ', '.join(group.aliases)]), value="This rune does not emit any light.", inline=False)
        for command in group.commands:
            embed.add_field(name=command.name, value=command.help, inline=False)
        await self.context.message.reply(embed=embed, private=True)
        await self.context.message.delete()

    async def send_command_help(self, command):
        # await self.get_destination().send(f"{command.name}: {command.help}")
        embed = (
            self._get_embeds()
            .get_info_embed(
                self.context.message,
                title="Grimoire Index",
                dsc=f"Unravelling {command.name}...",
            )
            .set_thumbnail(
                url="https://cdn-icons-png.flaticon.com/512/2407/2407510.png"
            )
        )
        embed.add_field(name=command.name, value=command.help, inline=False)
        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)
        await self.context.message.reply(embed=embed, private=True)
        await self.context.message.delete()

helper = CustomHelp()