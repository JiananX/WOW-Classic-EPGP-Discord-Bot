import admin
import cfg
import constant
import discord
import distribute
import os
import raid
import re
import user

import logging



formatter = logging.Formatter('%(asctime)s %(message)s');
fh = logging.FileHandler('testing.log');
fh.setLevel(level=logging.INFO);
fh.setFormatter(formatter);

logger=logging.getLogger('EPGP');
logger.addHandler(fh)

client = discord.Client();

@client.event
async def on_ready():
  initialize_global_vars();

  print('CF Senior EPGP start');

@client.event
async def on_message(message):
  if(message.author == client.user):
    return;
  
  if(match_keywork(constant.admin_reg, message)):
    await on_admin_message(message);
  elif(match_keywork(constant.raid_op_reg, message)):
    await on_raid_op_message(message);
  elif(match_keywork(constant.dis_reg, message)):
    await on_distribution_message(message);
  else:
    await on_user_message(message);


async def on_user_message(message):
  if (cfg.admin == None):
    await message.channel.send('管理员还未开始本次Raid, 请稍后再试');
    return;

  if(match_keywork(constant.login_reg, message)):
    await user.member_login(message);
  elif(match_keywork(constant.raid_pr_list_reg, message)):
    await user.raid_pr_list(message);
  elif(match_keywork(constant.main_spec_reg, message)):
    await user.main_spec_response(message);
  else:
    await message.author.send('''
      指令              用途
    Login 游戏ID      进入Raid
    Raid PR          查看当前Raid中所有人的PR信息
    Main Spec/1      需求当前装备

    Admin指令（只有管理员可以使用）
    Admin|a 具体指令 (-h for help)
    Distribute|d 具体指令 (-h for help)
    Raid|r 具体指令 (-h for help)
    ''');

async def on_raid_op_message(message):
  if (str(message.author) not in os.environ['admin_token']):
    await message.channel.send('您不是管理员');
    return;

  if (cfg.admin == None):
    await admin.start_new_raid(message);

  if(match_keywork(constant.reward_ep, message)):
    await raid.reward_raid_ep(message);
  elif(match_keywork(constant.retrive_roster, message)):
    await raid.retrive_roster(message);
  else:
    await message.author.send('''
      指令              用途
    Raid|r Roster      Raid名册
    Raid|r reward XX [-r 原因] 奖励raid XX EP
    ''');

async def on_admin_message(message):
  if (str(message.author) not in os.environ['admin_token']):
    await message.channel.send('您不是管理员');
    return;

  if(match_keywork(constant.start_new_raid_reg, message)):
    await admin.start_new_raid(message);
  elif(match_keywork(constant.add_new_member_reg, message)):
    await admin.add_new_member(message);
  elif(match_keywork(constant.all_pr_list_reg, message)):
    await admin.all_pr_list(message);
  elif(match_keywork(constant.decay_reg, message)):
    await admin.decay(message);
  elif(match_keywork(constant.adjust_reg, message)):
    await admin.adjust(message);
  elif(match_keywork(constant.sync_epgp_from_gsheet, message)):
    await admin.sync_epgp_from_gsheet(message); 
  elif(match_keywork(constant.sync_loot_from_gsheet, message)):
    await admin.sync_loot_from_gsheet(message);   
  else:
    await message.author.send('''
      指令              用途
    Admin|a start      开始raid
    Admin|a pr         DB中所有人的PR信息
    Admin|a add -id    游戏ID [-ep XX] [-gp XX] 添加新的游戏ID到DB
    Admin|a decay      衰减DB中所有的EP/GP
    Admin|a adjust -id 游戏ID [-ep XX] [-gp XX] [-r 原因] 修改游戏ID的EP/GP
    Admin|a pull PR    从Gsheet中导入所有人的PR信息
    ''');

async def on_distribution_message(message):
  if (str(message.author) not in os.environ['admin_token']):
    await message.channel.send('您不是管理员');
    return;

  if (cfg.admin == None):
    await admin.start_new_raid(message);

  if(match_keywork(constant.announcement_reg, message)):
    await distribute.announcement(message);
  elif(match_keywork(constant.dis_cancel_reg, message)):
    await distribute.cancel(message);
  elif(match_keywork(constant.dis_confirm_reg, message)):
    await distribute.confirm(message);
  else:
    await message.author.send('''
      指令              用途
      Dis 物品 GP       准备分配物品
      Dis confirm [-percent 20|50] [-id 游戏ID] 确认分配物品
      Dis cancel       取消当前分配
    ''');

def match_keywork(keyword, message):
  return re.fullmatch(keyword, message.content, re.IGNORECASE);

def initialize_global_vars():
  cfg.admin = None;
  cfg.raid_roster = {};

  cfg.main_spec = None;
  cfg.current_item = None;
  cfg.current_winner = None;
  cfg.is_distributing = False;
  cfg.item_gp = None;

client.run(os.environ['discord_token']);

#print(re.findall("(Main Spec|1)", "Main Spec", re.IGNORECASE));
#print({}.get(1));
