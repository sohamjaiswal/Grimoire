import xkcd
import cartoonista
from guilded.ext import commands
from bot.middleware.grimoire import grimoire

from bot.utils.embeds import GrimEmbeds


class Comics(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.embeds = GrimEmbeds(bot)

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @grimoire
    async def xkcd(
        self, ctx: commands.Context
    ):
        """
        Fetches a random xkcd comic.
        """
        comic = xkcd.getRandomComic()
        embed = self.embeds.get_success_embed(
            ctx.message, title=comic.getTitle(), dsc=comic.getAltText()
        )
        embed.set_image(url=comic.getImageLink())
        embed.add_field(name="Number", value=comic.number, inline=True)
        embed.add_field(name="Link", value=f"[{comic.link}]({comic.link})", inline=True)
        return embed

    @xkcd.command(aliases=["ltx"])
    @grimoire
    async def latest(
        self, ctx: commands.Context
    ):
        """
        Fetches the latest xkcd comic.
        """
        comic = xkcd.getLatestComic()
        embed = self.embeds.get_success_embed(
            ctx.message, title=comic.getTitle(), dsc=comic.getAltText()
        )
        embed.set_image(url=comic.getImageLink())
        embed.add_field(name="Number", value=comic.number, inline=True)
        embed.add_field(name="Link", value=f"[{comic.link}]({comic.link})", inline=True)
        return embed

    @xkcd.command(aliases=["num"])
    @grimoire
    async def number(self, ctx: commands.Context, *, query: str = ""):
        """
        Fetches a xkcd comic by its number.
        """
        try:
            number = int(query)  # type: ignore
        except Exception as e:
            embed = self.embeds.get_error_embed(
                ctx.message, title="XKCD Comic", dsc="No comic found."
            )
            await ctx.reply(embed=embed)
            return
        comic = xkcd.getComic(number)
        embed = self.embeds.get_success_embed(
            ctx.message, title=comic.getTitle(), dsc=comic.getAltText()
        )
        embed.set_image(url=comic.getImageLink())
        embed.add_field(name="Number", value=comic.number, inline=True)
        embed.add_field(name="Link", value=f"[{comic.link}]({comic.link})", inline=True)
        return embed

    @commands.command(aliases=["xplsm"])
    @grimoire
    async def explosm(self, ctx: commands.Context):
        """
        Fetches a random explosm comic.
        """
        try:
            comic = cartoonista.get_random_cartoon(include=["explosm_net"])
        except Exception as e:
            print(e)
            embed = self.embeds.get_error_embed(
                ctx.message, title="SBMC Comic", dsc="No comic found."
            )
            await ctx.reply(embed=embed)
            return
        if comic is None:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Explosm Comic", dsc="No comic found."
            )
            await ctx.reply(embed=embed)
            return
        embed = self.embeds.get_success_embed(
            ctx.message, title="Explosm Comic", dsc=comic["txt"]
        )
        embed.set_image(url=comic["img"])
        embed.add_field(name="Credits", value=comic["credits"], inline=True)
        embed.add_field(
            name="Link", value=f'[{comic['img']}]({comic['img']})', inline=True
        )
        await ctx.reply(embed=embed)

    @commands.command(aliases=["cms"])
    @grimoire
    async def commitstrip(self, ctx: commands.Context):
        """
        Fetches a random commitstrip comic.
        """
        try:
            comic = cartoonista.get_random_cartoon(include=["commitstrip_com"])
        except Exception as e:
            print(e)
            embed = self.embeds.get_error_embed(
                ctx.message, title="SBMC Comic", dsc="No comic found."
            )
            await ctx.reply(embed=embed)
            return
        if comic is None:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Commitstrip Comic", dsc="No comic found."
            )
            await ctx.reply(embed=embed)
            return
        embed = self.embeds.get_success_embed(
            ctx.message, title="Commitstrip Comic", dsc=comic["txt"]
        )
        embed.set_image(url=comic["img"])
        embed.add_field(name="Credits", value=comic["credits"], inline=True)
        embed.add_field(
            name="Link", value=f'[{comic['img']}]({comic['img']})', inline=True
        )
        await ctx.reply(embed=embed)

    @commands.command()
    @grimoire
    async def smbc(self, ctx: commands.Context):
        """
        Fetches a random commitstrip comic.
        """
        try:
            comic = cartoonista.get_random_cartoon(include=["smbc_comics_com"])
        except Exception as e:
            print(e)
            embed = self.embeds.get_error_embed(
                ctx.message, title="SBMC Comic", dsc="No comic found."
            )
            await ctx.reply(embed=embed)
            return
        if comic is None:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Commitstrip Comic", dsc="No comic found."
            )
            await ctx.reply(embed=embed)
            return
        embed = self.embeds.get_success_embed(
            ctx.message, title="Commitstrip Comic", dsc=comic["txt"]
        )
        embed.set_image(url=comic["img"])
        embed.add_field(name="Credits", value=comic["credits"], inline=True)
        embed.add_field(
            name="Link", value=f'[{comic['img']}]({comic['img']})', inline=True
        )
        await ctx.reply(embed=embed)

    @commands.command()
    @grimoire
    async def james(self, ctx: commands.Context):
        """
        Fetches a random commitstrip comic.
        """
        try:
            comic = cartoonista.get_random_cartoon(include=["jamesofnotrades_com"])
        except Exception as e:
            print(e)
            embed = self.embeds.get_error_embed(
                ctx.message, title="SBMC Comic", dsc="No comic found."
            )
            await ctx.reply(embed=embed)
            return
        if comic is None:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Commitstrip Comic", dsc="No comic found."
            )
            await ctx.reply(embed=embed)
            return
        embed = self.embeds.get_success_embed(
            ctx.message, title="Commitstrip Comic", dsc=comic["txt"]
        )
        embed.set_image(url=comic["img"])
        embed.add_field(name="Credits", value=comic["credits"], inline=True)
        embed.add_field(
            name="Link", value=f'[{comic['img']}]({comic['img']})', inline=True
        )
        await ctx.reply(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Comics(bot))
