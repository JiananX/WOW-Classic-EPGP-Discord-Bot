from raider import Raider
from view.view import update_raider_view, update_admin_view

import cfg
import constant
import history
import re
import util


async def add_new_member(message):
    raider_name_match = re.findall("-name ([^ ]+)", message.content,
                                   re.IGNORECASE)

    if (len(raider_name_match) == 1):
        raider_name = raider_name_match[0]

        if (cfg.raider_dict.get(raider_name) != None):
            cfg.event_msg = 'The raider name is already existed'
        else:
            cfg.raider_dict.update({
                raider_name:
                Raider(raider_name, 0, constant.initial_gp, None)
            })

            cfg.event_msg = 'New raider name has been added, user need to login'
    else:
        cfg.event_msg = 'No raider name in the command'

    await update_raider_view()
    await update_admin_view()


async def adjust(message):
    raider_name_match = re.findall("-name ([^ ]+)", message.content,
                                   re.IGNORECASE)

    if (len(raider_name_match) == 1):
        raider_name = raider_name_match[0]

        if (cfg.raider_dict.get(raider_name) == None):
            cfg.event_msg = 'Cannot find raider name'
        else:
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

            ep_before = util.get_ep(raider_name)
            gp_before = util.get_gp(raider_name)
            util.set_ep(raider_name, ep_before + ep)
            util.set_gp(raider_name, gp_before + gp)

            reason = ''
            reason_match = re.findall("-r ([^ ]+)", message.content,
                                      re.IGNORECASE)
            if (len(reason_match) == 1):
                reason = reason_match[0]

            history.log_adjustment([raider_name], ep=ep, gp=gp)

            cfg.event_msg = 'Adjust successfully'
    else:
        cfg.event_msg = 'No raider name in the command'

    await update_raider_view()
    await update_admin_view()
