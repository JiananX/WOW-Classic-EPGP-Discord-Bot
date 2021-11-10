import asyncio
import cfg
import view
import util
'''
Command
'''


async def announcement(message):
    if (cfg.main_spec != None or cfg.off_spec != None):
        await cfg.admin.send('请取消或者分配当前物品')
        return

    loot_id = message.content.split(" ")[1]

    if (cfg.loot_dict.get(loot_id) == None):
        await cfg.admin.send('无法找到该物品')
        return

    cfg.current_loot = cfg.loot_dict[loot_id]
    cfg.main_spec = []
    cfg.off_spec = []

    cfg.loot_channel.send(embed=view.loot_view_embed(),
                          components=view.loot_view_component())

    util.log_msg('开始分配[%s]' % (cfg.current_loot.NAME))
    await asyncio.sleep(20)
    await _calculate_result()


'''
Message Interaction
'''


async def cancel():
    util.log_msg('[%s]分配取消' % (cfg.current_loot.NAME))
    await _reset()
    await cfg.admin_msg.edit(embed=view.admin_embed(),
                             components=view.admin_view_component())


async def confirm(factor):
    before_gp = util.get_gp(cfg.current_winner)
    loot_gp = int(cfg.current_loot.GP * factor)
    gp = loot_gp + before_gp
    util.set_gp(cfg.current_winner, gp)
    util.log_msg('[%s]按照%s%%GP(%s)分配给%s, 分配前GP: %s, 分配后GP: %s' %
                 (cfg.current_loot.NAME, factor * 100, loot_gp,
                  util.find_game_id(cfg.current_winner), before_gp, gp))
    await _reset()
    await cfg.admin_msg.edit(embed=view.admin_embed(),
                             components=view.admin_view_component())


'''
Util
'''


async def _calculate_result():
    highest_pr = 0
    winner = None

    if (len(cfg.main_spec) == 0):
        for user_id in cfg.off_spec:
            pr = util.calculate_pr(util.find_game_id(user_id))
            if (pr > highest_pr):
                highest_pr = pr
                winner = user_id
    else:
        for user_id in cfg.main_spec:
            pr = util.calculate_pr(util.find_game_id(user_id))
            if (pr > highest_pr):
                highest_pr = pr
                winner = user_id

    last_message = cfg.loot_channel.last_message
    last_message_embed = last_message.embed

    if (winner != None):
        cfg.current_winner = winner

        last_message_embed.add_field(name="获胜者",
                                     value='%s' % (cfg.game_id),
                                     inline=False)

        prs = ''
        game_ids = ''
        sources = ''

        for user_id in cfg.main_spec:
            game_id = util.find_game_id(user_id)
            game_ids += game_id + '\n'
            sources += 'Main Spec\n'
            prs += '%s\n' % (util.calculate_pr(game_id))

        for user_id in cfg.off_spec:
            game_id = util.find_game_id(user_id)
            game_ids += game_id + '\n'
            sources += 'Off Spec\n'
            prs += '%s\n' % (util.calculate_pr(game_id))

        await last_message.edit(
            embed=last_message_embed,
            components=view.loot_view_component(enable_button=False))
        await cfg.admin_msg.edit(embed=view.admin_embed(),
                                 components=view.admin_view_component(
                                     enable_confirm_button=True,
                                     enable_cancel_button=True))
    else:
        last_message_embed.add_field(name="获胜者",
                                     value='本次无人需求该装备',
                                     inline=False)
        await last_message.edit(
            embed=last_message_embed,
            components=view.loot_view_component(enable_button=False))

        await cfg.admin_msg.edit(
            embed=view.admin_embed(),
            components=view.admin_view_component(enable_cancel_button=True))


async def _reset():
    cfg.main_spec = None
    cfg.off_spec = None
    cfg.current_loot = None
    cfg.current_winner = None
