from guilded.ext import commands
from bot.middleware.grimoire import grimoire
from bot.utils.embeds import GrimEmbeds
import os
import requests
import shlex

from typing import List, Dict, Union


class Weeb(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None
        self.embeds = GrimEmbeds(bot)
        self.consumet_url = os.getenv("CONSUMET_HOST")

    async def _search_query_parse(
        self, tokens: List[str]
    ) -> Dict[str, Union[str, int]]:
        args = {"-s": "", "-n": 1, "-p": 1}
        # Check if the basic query flag is present
        if "-s" not in tokens:
            args["-s"] = " ".join(tokens)
            return args
        # Iterate through the tokens and parse the arguments
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == "-s":
                i += 1
                args["-s"] = tokens[i]
            elif token == "-n":
                i += 1
                args["-n"] = int(tokens[i])
            elif token == "-p":
                i += 1
                args["-p"] = int(tokens[i])
            i += 1

        return args

    async def _zoro_search(self, query: str, page: int = 1):
        r = requests.get(f"{self.consumet_url}/anime/zoro/{query}?page={page}")
        return r

    async def _gogo_search(self, query: str, page: int = 1):
        r = requests.get(f"{self.consumet_url}/anime/gogoanime/{query}?page={page}")
        return r

    @commands.command()
    @grimoire
    async def zoro(self, ctx: commands.Context, *, query: str = ''):
        """
        Basic:
        Gives first result for searched anime from Zoro.
        Advanced:
        -s: str = Query for zoro `*` Required
        -n: int = Number of results to return `*` Optional
        -p: int = Page number `*` Optional
        """
        tokens = shlex.split(query, posix=True)
        try:
            args = await self._search_query_parse(tokens)
        except Exception as e:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error", dsc="Something went wrong."
            )
            return embed
        r = await self._zoro_search(args["-s"], args["-p"])  # type: ignore
        if r.status_code != 200:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error", dsc="Something went wrong."
            )
            return embed
        res = r.json()
        num_results = len(res["results"])
        if args["-n"] > num_results:  # type: ignore
            args["-n"] = num_results
        for i in range(args["-n"]):  # type: ignore
            if i == 0 and args["-n"] == 1:
                embed = self.embeds.get_success_embed(
                    ctx.message,
                    title=res["results"][i]["title"],
                    dsc=f"Query: {args['-s']}",
                )  # type: ignore
            elif i == 0:
                embed = self.embeds.get_success_embed(
                    ctx.message,
                    title=res["results"][i]["title"],
                    dsc=f"Query: {args['-s']}\nPage: {args['-p']}\nResult: {i+1}/{args['-n']}",
                )  # type: ignore
            else:
                embed = self.embeds.get_success_embed(
                    ctx.message,
                    title=res["results"][i]["title"],
                    dsc=f"Result: {i+1}/{args['-n']}",
                )
            embed.add_field(name="id", value=res["results"][i]["id"], inline=True)
            embed.add_field(
                name="url",
                value=f"[{res['results'][i]['url']}]({res['results'][i]['url']})",
                inline=True,
            )
            embed.add_field(name="type", value=res["results"][i]["type"], inline=True)
            embed.set_image(url=res["results"][i]["image"])
            return embed
    
    @commands.command()
    @grimoire
    async def gogo(self, ctx: commands.Context, *, query: str = ''):
        """
        Basic:
        Gives first result for searched anime from GoGoAnime.
        Advanced:
        -s: str = Query for zoro `*` Required
        -n: int = Number of results to return `*` Optional
        -p: int = Page number `*` Optional
        """
        tokens = shlex.split(query, posix=True)
        try:
            args = await self._search_query_parse(tokens)
        except Exception as e:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error", dsc="Something went wrong."
            )
            return embed
        r = await self._gogo_search(args["-s"], args["-p"])  # type: ignore
        if r.status_code != 200:
            embed = self.embeds.get_error_embed(
                ctx.message, title="Error", dsc="Something went wrong."
            )
            return embed
        res = r.json()
        num_results = len(res["results"])
        if args["-n"] > num_results:  # type: ignore
            args["-n"] = num_results
        for i in range(args["-n"]):  # type: ignore
            if i == 0 and args["-n"] == 1:
                embed = self.embeds.get_success_embed(
                    ctx.message,
                    title=res["results"][i]["title"],
                    dsc=f"Query: {args['-s']}",
                )  # type: ignore
            elif i == 0:
                embed = self.embeds.get_success_embed(
                    ctx.message,
                    title=res["results"][i]["title"],
                    dsc=f"Query: {args['-s']}\nPage: {args['-p']}\nResult: {i+1}/{args['-n']}",
                )  # type: ignore
            else:
                embed = self.embeds.get_success_embed(
                    ctx.message,
                    title=res["results"][i]["title"],
                    dsc=f"Result: {i+1}/{args['-n']}",
                )
            embed.add_field(name="id", value=res["results"][i]["id"], inline=True)
            embed.add_field(
                name="url",
                value=f"[{res['results'][i]['url']}]({res['results'][i]['url']})",
                inline=True,
            )
            embed.add_field(name="Release Date", value=res["results"][i]["releaseDate"], inline=True)
            embed.add_field(name="Sub/Dub", value=res["results"][i]["subOrDub"], inline=True)
            embed.set_image(url=res["results"][i]["image"])
            return embed


def setup(bot: commands.Bot):
    bot.add_cog(Weeb(bot))
    