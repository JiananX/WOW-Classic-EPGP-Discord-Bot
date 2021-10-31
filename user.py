import cfg;
import util;
import view;

'''
Command
'''
async def member_login(message):
    game_id = message.content.split(" ")[1]

    if (cfg.raid_roster.get(message.author) != None):
        await message.channel.send('您的游戏ID已经登陆')
        return

    if (util.is_valid_game_id(game_id) == False):
        await message.channel.send('您的epgp存在问题, 请联系本次管理员%s' % (cfg.admin))
        return

    cfg.raid_roster.update({message.author: game_id})

    msg = await message.channel.send('欢迎参加本次Raid %s'%(game_id),
                               components = view.user_view_component(False),
                               embed = view.my_pr_embed(message.author));
                                   
    cfg.raid_user_msg.update({message.author: msg});

    util.log_msg('登陆信息 ID: %s EP: %s, GP: %s' %(game_id, util.get_ep(game_id), util.get_gp(game_id)));


'''
Message Interaction
'''
def raid_pr_list():
    pr_list = {}
    ep_list = {}
    gp_list = {}
    for author in cfg.raid_roster.keys():
        game_id = cfg.raid_roster[author]

        ep_list.update({game_id: util.get_ep(game_id)})
        gp_list.update({game_id: util.get_gp(game_id)})
        pr_list.update({game_id: util.calculate_pr(game_id)})

    return util.generate_pr_list(pr_list, ep_list, gp_list);

def my_pr(author):
  game_id = cfg.raid_roster[author];
  return 'EP: %s  GP: %s  PR: %s'%(util.get_ep(game_id), util.get_gp(game_id), util.calculate_pr(game_id));


def main_spec_response(author):
    cfg.main_spec.update(
        {author: util.calculate_pr(cfg.raid_roster[author])})
