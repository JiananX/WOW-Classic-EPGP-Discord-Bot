import asyncio
import cfg
import view
import util
'''
Command
'''


async def announcement(message):
    if (cfg.main_spec != None or cfg.off_spec != None):
        await cfg.admin.send(
            'Last item still in progress, please cancel or confirm')
        return

    loot_id = message.content.split(" ")[1]

    if (cfg.loot_dict.get(loot_id) == None):
        await cfg.admin.send('Invalid loot')
        return

    cfg.current_loot = cfg.loot_dict[loot_id]
    cfg.main_spec = []
    cfg.off_spec = []

    # Update user/admin message for loot section
    for msg in cfg.raid_user_msg.values():
        await msg.edit(
            embed=view.my_pr_embed(message.author),
            components=view.user_view_component(enable_loot_button=True))
    await cfg.admin_msg.edit(embed=view.loot_admin_embed())

    util.log_msg('开始分配%s' % (cfg.current_loot.NAME))
    await asyncio.sleep(20)
    await _calculate_result()


'''
Message Interaction
'''


async def cancel():
    util.log_msg('%s分配取消' % (cfg.current_loot.NAME))
    await _reset()


async def confirm(factor):
    winner_id = util.find_game_id(cfg.current_winner)
    before_gp = util.get_gp(winner_id)
    loot_gp = int(cfg.current_loot.GP * factor)
    gp = loot_gp + before_gp
    util.set_gp(winner_id, gp)
    util.log_msg('%s 按照%s%%GP %s 分配给%s, Before GP %s, After GP %s' % (cfg.current_loot.NAME, factor*100, loot_gp, winner_id, before_gp, gp))
    await _reset()


'''
Util
'''


async def _calculate_result():
    # Disable all the main spec button before calculation.
    for msg in cfg.raid_user_msg.values():
        await msg.edit(components=view.user_view_component(False))

    highest_pr = 0
    winner = None

    for author in cfg.off_spec:
        pr = util.calculate_pr(util.find_game_id(author))
        if (pr > highest_pr):
            highest_pr = pr
            winner = author

    # Reset hightest_pr to 0, even 1 main_spec will outbid n off_spec
    highest_pr = 0

    for author in cfg.main_spec:
        pr = util.calculate_pr(util.find_game_id(author))
        if (pr > highest_pr):
            highest_pr = pr
            winner = author

    if (winner != None):
        all_string = '参与者\n'
        winner_string = '\n获胜者\n'
        for author in cfg.off_spec:
            game_id = util.find_game_id(author)
            all_string += 'Off Spec id: %s, pr: %s\n' % (game_id,
                                                util.calculate_pr(game_id))
            if (author == winner):
                winner_string += 'Off Spec id: %s, pr: %s' % (
                    game_id, util.calculate_pr(game_id))

        for author in cfg.main_spec:
            game_id = util.find_game_id(author)
            all_string += 'Main Spec id: %s, pr: %s\n' % (game_id,
                                                util.calculate_pr(game_id))
            if (author == winner):
                winner_string += 'Main Spec id: %s, pr: %s' % (
                    game_id, util.calculate_pr(game_id))

        cfg.loot_message = all_string + winner_string
        cfg.current_winner = winner

        for user in cfg.raid_user_msg.keys():
            msg = cfg.raid_user_msg[user]
            await msg.edit(embed=view.my_pr_embed(user))

        await cfg.admin_msg.edit(embed=view.loot_admin_embed(),
                                 components=view.loot_admin_view_component(
                                     True, True))
    else:
        cfg.loot_message = '本次Loot无人GP需求'

        for user in cfg.raid_user_msg.keys():
            msg = cfg.raid_user_msg[user]
            await msg.edit(embed=view.my_pr_embed(user))

        await cfg.admin_msg.edit(embed=view.loot_admin_embed(),
                                 components=view.loot_admin_view_component(
                                     False, True))


async def _reset():
    cfg.main_spec = None
    cfg.off_spec = None
    cfg.current_loot = None
    cfg.current_winner = None
    cfg.loot_message = None

    for user in cfg.raid_user_msg.keys():
        msg = cfg.raid_user_msg[user]
        await msg.edit(embed=view.my_pr_embed(user))

    await cfg.admin_msg.edit(embed=view.loot_admin_embed(),
                             components=view.loot_admin_view_component(
                                 False, False))
