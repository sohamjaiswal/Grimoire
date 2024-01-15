import asyncio
import shlex
from typing import Dict, List
from guilded.ext import commands
from horde_sdk import ANON_API_KEY, RequestErrorResponse

from horde_sdk.ai_horde_api.ai_horde_clients import AIHordeAPIAsyncSimpleClient
from horde_sdk.ai_horde_api.apimodels import ImageGenerateAsyncRequest, ImageGenerateStatusResponse, ImageGenerateCheckResponse
from horde_sdk.ai_horde_api.fields import JobID

import aiohttp
from bot.middleware.grimoire import grimoire

from bot.utils.embeds import GrimEmbeds

class Ai(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.embeds = GrimEmbeds(bot)
  
  @commands.group(invoke_without_command=True)
  @grimoire
  async def horde(self, ctx: commands.Context):
    '''
    Used to interact with stable horde
    
    Args:
      stable | kobold
    '''
    embed = self.embeds.get_error_embed(
      ctx.message, title="Horde", dsc="Use a subcommand."
    )
    return embed
  
  async def _prompt_parse(
    self, tokens: List[str]
  ) -> Dict[str, str]:
    args = {"-p": "", "-n": "", "-m": [], "nsfw": False}
    if "--nsfw" in tokens:
      args["nsfw"] = True
      tokens.remove("--nsfw")
    if "-p" not in tokens:
      args["-p"] = " ".join(tokens)
      return args
    i = 0
    while i < len(tokens):
      token = tokens[i]
      if token == "-p":
        i += 1
        args["-p"] = tokens[i]
      elif token == "-n":
        i += 1
        args["-n"] = tokens[i]
      elif token == "-m":
        i += 1
        args["-m"] = tokens[i].split(",")
      i += 1
    return args
  
  async def _async_one_image_generate(self, client: AIHordeAPIAsyncSimpleClient, api_key: str, ctx: commands.Context, status_update_callback, **kwargs):
    single_generation_response: ImageGenerateStatusResponse
    job_id: JobID
    single_generation_response, job_id = await client.image_generate_request(
      ImageGenerateAsyncRequest(
        apikey=api_key,
        prompt=kwargs["-p"] + (f" ### {kwargs['-n']}" if len(kwargs["-n"]) != 0 else ""),
        models= kwargs["-m"] if len(kwargs["-m"]) != 0 else ["Deliberate", "stable_diffusion"],
        r2=True,
        nsfw=kwargs["nsfw"],
        censor_nsfw=False,
      ),
      check_callback=status_update_callback
    )
    
    if isinstance(single_generation_response, RequestErrorResponse):
      return self.embeds.get_error_embed(
        ctx.message, title="Error", dsc=single_generation_response.message
      )
    
    else:
      return self.embeds.get_success_embed(
        ctx.message, title="Success", dsc=f"Job ID: {job_id}"
      ).set_image(url=single_generation_response.generations[0].img)
    
  @horde.command()
  @commands.cooldown(1, 50, commands.BucketType.user)
  @grimoire
  async def image(self, ctx: commands.Context, *, prompt: str):
    '''
    Overview:
    Starts a request on the AI Horde.
    Advanced:
    Note: All arguments are optional, enter string values in quotes.
    -p: str = Positive Prompt (default)
    -n: str = Negative Prompt
    -m: str = comma separated models to use (defaults to deliberate and stable_diffusion model) e.g. "stable_diffusion,'OpenJourney Diffusion',deliberate"
    -s: int = number of steps to interrogate (default = 25)
    '''
    tokens = shlex.split(prompt, posix=True)
    try:
      args = await self._prompt_parse(tokens)
      print(args)
    except Exception as e:
      embed = self.embeds.get_error_embed(
        ctx.message, title="Error", dsc="Something went wrong."
      )
      return embed
    try:
      async with aiohttp.ClientSession() as session:
        client = AIHordeAPIAsyncSimpleClient(session)
        status_message = await ctx.reply(
          embed=self.embeds.get_success_embed(
            ctx.message, title="Success", dsc="Starting request..."
          )
        )
        
        async def update_message(generation: ImageGenerateCheckResponse):
          update_embed = self.embeds.get_success_embed(
              ctx.message, title="Success", dsc=f"Status: **{"Done" if generation.done else "Faulted" if generation.faulted else "Possible" if generation.is_possible else "Fetching Status..."}**"
            )
          update_embed.add_field(name="Kudos", value=f"**{generation.kudos}**", inline=True)
          update_embed.add_field(name="Position", value=f"**{generation.queue_position}**", inline=True)
          update_embed.add_field(name="Wait Time", value=f"**{generation.wait_time}**", inline=True)
          update_embed.add_field(name="Wait Time", value=f"**{generation.wait_time}**", inline=True)
          await status_message.edit(
            embed=update_embed
          )
          
        def status_callback(generation: ImageGenerateCheckResponse):
          asyncio.create_task(update_message(generation))

        return await self._async_one_image_generate(client, ANON_API_KEY, ctx, status_callback, **args)
    except Exception as e:
      embed = self.embeds.get_error_embed(
        ctx.message, title="Error", dsc="Something went wrong."
      )
      return embed

def setup(bot: commands.Bot):
  bot.add_cog(Ai(bot))
