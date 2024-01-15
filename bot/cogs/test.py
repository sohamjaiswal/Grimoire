import guilded
from guilded.ext import commands

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command()
    async def nogroup(self, ctx: commands.Context):
        await ctx.send("This command is not in a group.")
    
    @commands.group(invoke_without_command=True)
    async def group(self, ctx: commands.Context):
        """Contains commands for testing. 

        Args:
            ctx (commands.Context): _description_
        """
        await ctx.send("This is a group.")
    
    @group.command()
    async def subcommand(self, ctx: commands.Context):
        """This is a subcommand."""
        await ctx.send("This is a subcommand within a group.")
    
    @commands.command()
    async def hello(self, ctx, *, member: guilded.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member

def setup(bot: commands.Bot):
    bot.add_cog(Test(bot))