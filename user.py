import cfg;
import util

import logging

async def member_login(message):
  logger=logging.getLogger('EPGP');
  game_id = message.content.split(" ")[1];
  
  if (cfg.raid_roster.get(message.author) !=  None):
    await message.channel.send('您的游戏ID已经登陆');
    return 

  if (util.is_valid_game_id(game_id) == False):
    await message.channel.send('您的epgp存在问题, 请联系本次管理员%s'%(cfg.admin));
    return 

  cfg.raid_roster.update({message.author: game_id});
  login_message = '登陆信息 ID: %s EP: %s, GP: %s'%(game_id, util.get_ep(game_id), util.get_gp(game_id));
  await message.channel.send(login_message);
  logger.warning("haha");

async def raid_pr_list(message):
  if (cfg.raid_roster.get(message.author) ==  None):
    await message.channel.send('您还未加入本次Raid');
    return;

  pr_list = {};
  ep_list = {};
  gp_list = {};
  for author in cfg.raid_roster.keys():
    game_id = cfg.raid_roster[author];
    
    ep_list.update({game_id: util.get_ep(game_id)});
    gp_list.update({game_id: util.get_gp(game_id)});
    pr_list.update({game_id: util.calculate_pr(game_id)});

  await message.channel.send(util.generate_pr_list(pr_list, ep_list, gp_list));

async def main_spec_response(message):
  if (cfg.raid_roster.get(message.author) ==  None):
    await message.channel.send('您还未加入本次Raid');
    return;

  if (cfg.is_distributing == False):
    await message.channel.send('现在没有正在分配物品');
    return;
  
  if (cfg.main_spec == None):
    await message.channel.send('当前物品已经结算完毕');
    return;

  if (message.author in cfg.main_spec.keys()):
    await message.channel.send('您已经参与本次Loot分配');
    return;

  cfg.main_spec.update({message.author: util.calculate_pr(cfg.raid_roster[message.author])});
  await message.channel.send('您已经需求%s'%(cfg.current_item));
    

  
