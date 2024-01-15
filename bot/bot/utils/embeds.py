from guilded import Embed, Color, Message
from guilded.ext.commands import Bot

res_color_map={
  'success': Color.teal(),
  'warn': Color.gold(),
  'error': Color.red(),
  'info': Color.blue()
}

inv_res_color_map = {v: k for k, v in res_color_map.items()}


class GrimEmbeds:
  def __init__(self, client: Bot):
    self.client = client

  def _set_footer(self, embed: Embed, msg: Message) -> Embed:
    if self.client.user and msg.author:
      embed.set_footer(icon_url=self.client.user.avatar, text=f'© {self.client.user.name}->{msg.server.name}|{msg.author.name}')
      embed.timestamp = msg.created_at
      embed.set_author(name=msg.author.name, icon_url=msg.author.avatar)
    return embed

  def get_success_embed(self, msg: Message,  title:str="Success", dsc:str= "Success description") -> Embed:
    embed = Embed()
    embed.title = title
    embed.description = dsc
    embed.color = Color.teal()
    return self._set_footer(embed, msg)
  
  def get_warn_embed(self, msg: Message,  title:str="Warning", dsc:str= "Warning description") -> Embed:
    embed = Embed()
    embed.title = title
    embed.description = dsc
    embed.color = Color.gold()
    return self._set_footer(embed, msg)
  
  def get_error_embed(self,  msg: Message, title:str="Error", dsc:str= "Error description") -> Embed:
    embed = Embed()
    embed.title = title
    embed.description = dsc
    embed.color = Color.red()
    return self._set_footer(embed, msg)
  
  def get_info_embed(self, msg: Message,  title:str="Info", dsc:str= "Info description") -> Embed:
    embed = Embed()
    embed.title = title
    embed.description = dsc
    embed.color = Color.blue()
    return self._set_footer(embed, msg)