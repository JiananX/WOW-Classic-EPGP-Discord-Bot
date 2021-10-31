from replit import db

import admin
import asyncio
import cfg
import re
import view
import util

'''
Command
'''


async def announcement(message):
    if (cfg.is_distributing == True):
        await cfg.admin.send(
            'Last item still in progress, please cancel or confirm')
        return

    loot_id = message.content.split(" ")[1]

    if (admin.loot_dict.get(loot_id) == None):
        await cfg.admin.send('Invalid loot')
        return

    cfg.is_distributing = True
    cfg.current_loot = admin.loot_dict[loot_id]
    cfg.main_spec = {}

    for msg in cfg.raid_user_msg.values():
        await msg.edit(embed=view.my_pr_embed(message.author),
                       components=view.user_view_component(True))
    await cfg.admin_loot_message.edit(embed=view.loot_admin_embed())
    await asyncio.sleep(30)
    await _calculate_result()


'''
Message Interaction
'''
async def cancel():
    await _reset()


async def confirm(factor):
    winner_id = cfg.raid_roster[cfg.current_winner]
    util.set_gp(winner_id, int(cfg.current_loot.gp * factor)+util.get_gp(winner_id));

    await _reset()


'''
Util
'''


async def _calculate_result():
    for msg in cfg.raid_user_msg.values():
        await msg.edit(components=view.user_view_component(False))

    highest_pr = 0
    winner = None

    for author in cfg.main_spec.keys():
        pr = cfg.main_spec[author]
        if (pr > highest_pr):
            highest_pr = pr
            winner = author

    if (winner != None):
        all_string = '参与者\n'
        winner_string = '\n获胜者\n'
        for author in cfg.raid_roster.keys():
            if (author in cfg.main_spec.keys()):
                all_string += 'id: %s, pr: %s\n' % (cfg.raid_roster[author],
                                                    cfg.main_spec[author])
            if (author == winner):
                winner_string += 'id: %s, pr: %s' % (cfg.raid_roster[author],
                                                     cfg.main_spec[author])

        cfg.loot_message = all_string + winner_string
        cfg.current_winner = winner

        for user in cfg.raid_user_msg.keys():
            msg = cfg.raid_user_msg[user]
            await msg.edit(embed=view.my_pr_embed(user))

        await cfg.admin_loot_message.edit(
            embed=view.loot_admin_embed(),
            components=view.loot_admin_view_component(True, True))
    else:
        cfg.loot_message = '本次Loot无人GP需求'

        for user in cfg.raid_user_msg.keys():
            msg = cfg.raid_user_msg[user]
            await msg.edit(embed=view.my_pr_embed(user))

        await cfg.admin_loot_message.edit(
            embed=view.loot_admin_embed(),
            components=view.loot_admin_view_component(False, True))


async def _reset():
    cfg.main_spec = None
    cfg.current_loot = None
    cfg.current_winner = None
    cfg.loot_message = None
    cfg.is_distributing = False

    for user in cfg.raid_user_msg.keys():
        msg = cfg.raid_user_msg[user]
        await msg.edit(embed=view.my_pr_embed(user))

    await cfg.admin_loot_message.edit(
        embed=view.loot_admin_embed(),
        components=view.loot_admin_view_component(False, False))
