from view.view import send_loot_message, send_loot_result_message, update_admin_view

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
    winner_user_id = None

    if (len(cfg.main_spec) == 0):
        for user_id in cfg.off_spec:
            pr = util.calculate_pr(util.find_raider_name(user_id))
            if (pr > highest_pr):
                highest_pr = pr
                winner_user_id = user_id
    else:
        for user_id in cfg.main_spec:
            pr = util.calculate_pr(util.find_raider_name(user_id))
            if (pr > highest_pr):
                highest_pr = pr
                winner_user_id = user_id

    await send_loot_result_message(loot, winner_user_id)

    cfg.event_msg = '[%s] to %s' % (loot.name,
                                    util.find_raider_name(winner_user_id))

    await update_admin_view()
