from raider import Raider
from view.view import update_raider_view

import cfg
import constant
import re
import util

async def add_new_member(message):
    game_id_match = re.findall("-id ([^ ]+)", message.content, re.IGNORECASE)

    if (len(game_id_match) == 1):
        game_id = game_id_match[0]

        if (cfg.raider_dict.get(game_id) != None):
            await message.author.send('The game id is already existed')
            return

        cfg.raider_dict.update(
            {game_id: Raider(game_id, 0, constant.initial_gp, False, False, None, None)})

        await message.author.send(
            'New game id has been added, user need to login')
    else:
        await message.author.send('No game id in the command')

async def adjust(message):
    game_id_match = re.findall("-id ([^ ]+)", message.content, re.IGNORECASE)

    if (len(game_id_match) == 1):
        game_id = game_id_match[0]

        if (cfg.raider_dict.get(game_id) == None):
            await message.author.send('Cannot find game id')
            return

        ep_match = re.findall("-ep ([+-]?[0-9]+)", message.content,
                              re.IGNORECASE)
        gp_match = re.findall("-gp ([+-]?[0-9]+)", message.content,
                              re.IGNORECASE)
        ep = 0
        gp = 0
        if (len(ep_match) == 1):
            ep = int(ep_match[0])
        if (len(gp_match) == 1):
            gp = int(gp_match[0])

        ep_before = util.get_ep(game_id)
        gp_before = util.get_gp(game_id)
        util.set_ep(game_id, ep_before + ep)
        util.set_gp(game_id, gp_before + gp)

        adjust_message = '调整成功 ID: %s Before EP: %s, GP: %s, After EP: %s, GP: %s' % (
            game_id, ep_before, gp_before, util.get_ep(game_id),
            util.get_gp(game_id))

        reason_match = re.findall("-r ([^ ]+)", message.content, re.IGNORECASE)
        if (len(reason_match) == 1):
            adjust_message += ', 原因: %s' % (reason_match[0])

        await message.author.send(adjust_message)

        await update_raider_view()

        util.log_msg(adjust_message)
    else:
        await message.author.send('No game id in the command')
