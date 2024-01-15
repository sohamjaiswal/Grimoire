from pyurbandict import UrbanDict
from guilded.ext import commands
from dateparser import parse
from PyDictionary import PyDictionary
from bot.middleware.grimoire import grimoire
from bot.utils.embeds import GrimEmbeds

class Dictionaries(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None
        self.embeds = GrimEmbeds(bot)
        self.dictionary = PyDictionary()

    @commands.command()
    @grimoire
    async def define(self, ctx: commands.Context, *, term: str):
        """Defines a term."""
        definition = self.dictionary.meaning(term)
        if not definition:
            await ctx.reply("No definition found.", private=True)
            return
        embed = self.embeds.get_success_embed(ctx.message, title=term, dsc="Definitions:")
        for key in definition.keys():
            embed.add_field(name=key, value=str.join("\n\n", definition[key]), inline=False)
        await ctx.reply(embed=embed, private=True)

    @commands.command()
    @grimoire
    async def urban(self, ctx: commands.Context, *, term: str):
        """Searches the Urban Dictionary for a term."""
        ud = UrbanDict(term)
        res = ud.search()[0]
        embed = self.embeds.get_success_embed(ctx.message, title=res.word, dsc=res.definition)
        embed.add_field(name="Author", value=res.author, inline=False)
        embed.add_field(name="Example", value=res.example, inline=False)
        embed.add_field(name="Thumbs Up", value=res.thumbs_up, inline=True)
        embed.add_field(name="Thumbs Down", value=res.thumbs_down, inline=True)
        embed.add_field(name="Link", value=f"[{res.permalink}]({res.permalink})", inline=False)
        embed.add_field(name="Written On", value=parse(res.written_on).strftime('%m/%d/%Y'), inline=False)
        await ctx.reply(embed=embed, private=True)


def setup(bot: commands.Bot):
    bot.add_cog(Dictionaries(bot))