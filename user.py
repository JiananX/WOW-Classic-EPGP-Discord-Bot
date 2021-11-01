import cfg
import util
import view
'''
Command
'''


async def member_login(message):
    game_id = message.content.split(" ")[1]

    if (cfg.raid_user_msg.get(message.author) != None):
        await message.channel.send('您的游戏ID已经登陆')
        return

    if (cfg.raider_dict.get(game_id) == None):
        await message.channel.send('错误的游戏ID, 请重新登陆或者联系管理员%s' % (cfg.admin))
        return

    cfg.raider_dict[game_id].in_raid = True
    cfg.raider_dict[game_id].author = message.author
    cfg.raider_dict[game_id].author_id = message.author.id

    msg = await message.channel.send(
        '欢迎参加本次Raid %s' % (game_id),
        components=view.user_view_component(False),
        embed=view.my_pr_embed(message.author))
    cfg.raid_user_msg.update({message.author: msg})

    # Update roster section of admin view
    await cfg.admin_msg.edit(embed=view.loot_admin_embed())

    util.log_msg('登陆信息 ID: %s EP: %s, GP: %s' %
                 (game_id, util.get_ep(game_id), util.get_gp(game_id)))


'''
Message Interaction
'''


def raid_pr_list():
    pr_list = {}
    ep_list = {}
    gp_list = {}
    for game_id in cfg.raider_dict.keys():
        raider = cfg.raider_dict[game_id]
        if (raider.in_raid == True):
            ep_list.update({game_id: util.get_ep(game_id)})
            gp_list.update({game_id: util.get_gp(game_id)})
            pr_list.update({game_id: util.calculate_pr(game_id)})

    return util.generate_pr_list(pr_list, ep_list, gp_list)


def my_pr(author):
    game_id = util.find_game_id(author)
    return 'EP: %s  GP: %s  PR: %s' % (
        util.get_ep(game_id), util.get_gp(game_id), util.calculate_pr(game_id))
