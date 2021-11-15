from view.view import send_loot_message, update_admin_view

import asyncio
import cfg
import constant
import util


# TODO: Consider the cocurrent loot announcement situation, or consider support multi-loot announcement
async def loot_announcement(loot_name):
    cfg.main_spec = []
    cfg.off_spec = []

    loot = cfg.loot_dict[loot_name]

    await send_loot_message(loot)

    await asyncio.sleep(constant.loot_announcement_duration)

    await _calculate_result(loot)


async def _calculate_result(loot):
    highest_pr = 0
    min_ep = 0
    winner = None

    factor = 0
    all_bis_class = []
    if len(loot.BIS) != 0:
        for bis in loot.BIS.strip().split(' '):
            if (len(bis) != 0):
                all_bis_class.append(bis[len(bis) - 2])

    all_bis_class = set(all_bis_class)

    if (len(all_bis_class) == 1):
        factor = 0.5
    elif (len(all_bis_class) > 1):
        factor = 0.8

    if (len(cfg.main_spec) == 0):
        for user_id in cfg.off_spec:
            pr = util.calculate_pr(util.find_game_id(user_id))
            if (pr > highest_pr):
                highest_pr = pr
                winner = user_id
    else:
        for user_id in cfg.main_spec:
            ep = util.get_ep(util.find_game_id(user_id))

            if (ep * factor > min_ep):
                min_ep = ep * factor

        for user_id in cfg.main_spec:
            pr = util.calculate_pr(util.find_game_id(user_id))
            if (pr > highest_pr
                    and util.get_ep(util.find_game_id(user_id)) >= min_ep):
                highest_pr = pr
                winner = user_id

    if (winner != None):
        loot_result_message = 'Winner: __***%s***__\n\n' % (
            util.find_game_id(winner))

        for user_id in cfg.main_spec:
            loot_result_message += '**Main Spec**\n'
            game_id = util.find_game_id(user_id)
            loot_result_message += '%s (EP: %s, PR: %s)\n' % (
                game_id, util.get_ep(game_id), util.calculate_pr(game_id))

        for user_id in cfg.off_spec:
            loot_result_message += '**Off Spec**\n'
            game_id = util.find_game_id(user_id)
            loot_result_message += '%s (EP: %s, PR: %s)\n' % (
                game_id, util.get_ep(game_id), util.calculate_pr(game_id))
        cfg.loot_msg = loot_result_message

        await cfg.loot_channel.send(
            loot_result_message,
            delete_after=constant.loot_announcement_duration)
        await update_admin_view()
    else:
        cfg.loot_msg = 'Nobody want this loot :('
        await cfg.loot_channel.send(
            'Nobody want this loot :(',
            delete_after=constant.loot_announcement_duration)
        await update_admin_view()
