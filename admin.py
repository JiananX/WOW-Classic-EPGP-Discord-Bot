from replit import db

import cfg;
import constant
import re
import util
import gsheet
import pandas as pd
import json
import raider
import loot

import logging

raider_dict = {}
loot_dict = {}

async def start_new_raid(message):
  logger=logging.getLogger('EPGP');
  if (cfg.admin != None):
    await message.channel.send('%s已经开始本次Raid，请稍后再试'%(cfg.admin));
  else:
    cfg.admin = message.author;
    await message.channel.send('%s开始本次Raid'%(cfg.admin));
    logger.warning("start");

async def add_new_member(message):  
  game_id_match = re.findall("-id ([^ ]+)", message.content, re.IGNORECASE);
  
  if (len(game_id_match) == 1):
    game_id = game_id_match[0];

    if (util.is_valid_game_id(game_id) == True):
      await message.author.send('当前游戏ID已经存在于DB');
      return;

    ep_match = re.findall("-ep ([0-9]+)", message.content, re.IGNORECASE);
    gp_match = re.findall("-gp ([0-9]+)", message.content, re.IGNORECASE);
    ep = 0;
    gp = constant.initial_gp;
    if (len(ep_match) == 1):
      ep = int(ep_match[0]);
    if (len(gp_match) == 1):
      gp = int(gp_match[0]);

    util.set_ep(game_id, ep);
    util.set_gp(game_id, gp);
    await message.author.send('加入成功 ID: %s EP: %s, GP: %s'%(game_id, util.get_ep(game_id), util.get_gp(game_id)));
  else:
    await message.author.send('请指定新的游戏ID');

async def all_pr_list(message):
  raiders = '';
  for value in raider_dict.values():
    raiders += str(value) + '\n';
  if raiders == '':
    await message.author.send('请先运行(Admin|a) pull PR')
  else:
    await message.author.send(raiders)

async def all_pr_list_from_db(message):
  db_keys = db.keys();
  game_id_list = [];

  for db_key in db_keys:
    match = re.fullmatch("([^ ]+)\_ep", db_key);
    if (match):
      game_id = match[1];
      if (util.is_valid_game_id(game_id)):
        game_id_list.append(game_id);
      
  pr_list = {};
  ep_list = {};
  gp_list = {};
  for game_id in game_id_list:
    ep_list.update({game_id: util.get_ep(game_id)});
    gp_list.update({game_id: util.get_gp(game_id)});
    pr_list.update({game_id: util.calculate_pr(game_id)});

  await message.channel.send(util.generate_pr_list(pr_list, ep_list, gp_list));

async def decay(message):
  db_keys = db.keys();
  game_id_list = [];

  for db_key in db_keys:
    match = re.fullmatch("([^ ]+)\_ep", db_key);
    if (match):
      game_id = match[1];
      if (util.is_valid_game_id(game_id)):
        game_id_list.append(game_id);

  for game_id in game_id_list:
    util.set_ep(game_id, int(util.get_ep(game_id) * constant.decay_factor));
    util.set_gp(game_id, int(util.get_gp(game_id) * constant.decay_factor));

  await message.channel.send("Deacy 成功，系数为%s"%(constant.decay_factor));

async def adjust(message):  
  game_id_match = re.findall("-id ([^ ]+)", message.content, re.IGNORECASE);
  
  if (len(game_id_match) == 1):
    game_id = game_id_match[0];

    if (util.is_valid_game_id(game_id) == False):
      await message.author.send('当前游戏ID不存在');
      return;

    ep_match = re.findall("-ep ([+-]?[0-9]+)", message.content, re.IGNORECASE);
    gp_match = re.findall("-gp ([+-]?[0-9]+)", message.content, re.IGNORECASE);
    ep = 0;
    gp = 0;
    if (len(ep_match) == 1):
      ep = int(ep_match[0]);
    if (len(gp_match) == 1):
      gp = int(gp_match[0]);

    util.set_ep(game_id, util.get_ep(game_id) + ep);
    util.set_gp(game_id, util.get_gp(game_id) + gp);
    await message.author.send('调整成功 ID: %s EP: %s, GP: %s'%(game_id, util.get_ep(game_id), util.get_gp(game_id)));
  else:
    await message.author.send('请指定游戏ID');

async def sync_epgp_from_gsheet_to_json(message):
  epgp_from_gsheet = gsheet.get_epgp_from_gsheet()
  df = pd.DataFrame.from_dict(epgp_from_gsheet);
  raiders = [];
  for index, row in df.iterrows():
    r = raider.Raider(row['ID'], row['EP'], row['GP'], False)
    raider_dict[row['ID']] = r
    print(r)
    raiders.append(r)
  jstr = json.dumps([ob.__dict__ for ob in raiders])
  with open ('epgp.txt', 'w') as outfile:
    outfile.write(jstr)
  await message.author.send('从google sheet中导入epgp.txt成功');

async def sync_loot_from_gsheet_to_json(message):
  loot_from_gsheet = gsheet.get_loot_from_gsheet()
  df = pd.DataFrame.from_dict(loot_from_gsheet);
  loots = [];
  for index, row in df.iterrows():
    l = loot.Loot(row['ID'], row['NAME'], row['GP'], False)
    loot_dict[row['ID']] = l
    print(l)
    loots.append(l)
  jstr = json.dumps([ob.__dict__ for ob in loots])
  with open ('loot.txt', 'w') as outfile:
    outfile.write(jstr)
  await message.author.send('从google sheet中导入loot.txt成功');
  
async def load_epgp_from_json_to_memory(message):
  with open('epgp.txt', 'r') as infile:
    json_data = infile.read()   
  raiders = json.loads(json_data);
  for index, value in enumerate(raiders):
    r = raider.Raider(raiders[index]['ID'], raiders[index]['EP'], raiders[index]['GP'], False)
    raider_dict[raiders[index]['ID']] = r
    print(raider_dict[raiders[index]['ID']])
  await message.author.send('从epgp.txt导入成功');

async def load_loot_from_json_to_memory(message):
  with open('loot.txt', 'r') as infile:
    json_data = infile.read()   
  loots = json.loads(json_data);
  for index, value in enumerate(loots):
    l = loot.Loot(loots[index]['ID'], loots[index]['NAME'], loots[index]['GP'], False)
    loot_dict[loots[index]['ID']] = l
    print(loot_dict[loots[index]['ID']])
  await message.author.send('从loot.txt导入成功');

async def dump_epgp_from_memory_to_json(message):
  raiders = [];
  for value in raider_dict.values():
    raiders.append(value)
  jstr = json.dumps([ob.__dict__ for ob in raiders])
  with open ('epgp.txt', 'w') as outfile:
    outfile.write(jstr)
  await message.author.send('写入epgp.txt成功');

async def dump_loot_from_memory_to_json(message):
  loots = [];
  for value in loot_dict.values():
    loots.append(value)
  jstr = json.dumps([ob.__dict__ for ob in loots])
  with open ('loot.txt', 'w') as outfile:
    outfile.write(jstr)
  await message.author.send('写入loot.txt成功');