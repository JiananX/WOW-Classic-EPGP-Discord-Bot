from view.view import update_raider_view

import cfg
import history
import re
import util


async def adjust(message):
    raider_name_match = re.findall("-name ([^ ]+)", message.content,
                                   re.IGNORECASE)

    if (len(raider_name_match) == 1):
        raider_name = raider_name_match[0]

        if (cfg.raider_dict.get(raider_name) == None):
            await message.channel.send('无法找到游戏名称')
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
            await message.channel.send('调整成功')
    else:
        await message.channel.send('无法找到游戏名称')

    await update_raider_view()


async def decay(message):
    factor = float(message.content.split(" ")[1])
    for raider in cfg.raider_dict.values():
        raider_name = raider.name
        ep_before = util.get_ep(raider_name)
        gp_before = util.get_gp(raider_name)
        util.set_ep(raider_name, int(ep_before * factor))
        util.set_gp(raider_name, int(gp_before * factor))
    await message.channel.send('Decay成功')
