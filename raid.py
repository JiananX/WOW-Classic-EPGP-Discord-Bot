import cfg
import util

async def retrive_roster(message):
  await message.channel.send('名单\n%s\n总计: %s'%(cfg.raid_roster.values(), len(cfg.raid_roster.values())));

async def reward_raid_ep(message):
  ep = int(message.content.split(" ")[-1]);
  
  for author in cfg.raid_roster.keys():
    game_id = cfg.raid_roster[author];
    util.set_ep(game_id, ep + util.get_ep(game_id));
    await author.send('%s EP奖励生效, 当前EP: %s,当前GP: %s'%(ep, util.get_ep(game_id), util.get_gp(game_id)));