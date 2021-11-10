from raider import Raider

import cfg
import constant
import re
import util
import time
import source
import view


async def start_new_raid(message, client):
    if (len(cfg.raider_disct) != 0):
        await message.channel.send('Raid已经开始')
        return

    cfg.stamp = str(time.time())

    source.load_loot_from_json_to_memory()
    source.load_epgp_from_json_to_memory()

    # Reset some of the fields read from source
    for raider in cfg.raider_dict.values():
        raider.in_raid = False
        raider.stand_by = False

    channel = client.get_channel(constant.raid_channel)

    for member_id in channel.voice_states.keys():
        for name, raider in cfg.raider_dict.items():
            if raider.author_id == member_id:
                raider.in_raid = True

    cfg.admin_msg = await message.send(embed=view.admin_embed(),
                                 components=view.admin_view_component())
    util.log_msg('%s开始Raid' % (cfg.admin))


async def add_new_member(message):
    # raider_dict can be empty only the raid is not started.
    if (len(cfg.raider_dict) == 0):
        await message.author.send(
            'Please start a raid session to add new raid member')
        return

    game_id_match = re.findall("-id ([^ ]+)", message.content, re.IGNORECASE)

    if (len(game_id_match) == 1):
        game_id = game_id_match[0]

        if (cfg.raider_dict.get(game_id) != None):
            await message.author.send('当前游戏ID已经存在于DB')
            return

        ep_match = re.findall("-ep ([0-9]+)", message.content, re.IGNORECASE)
        gp_match = re.findall("-gp ([0-9]+)", message.content, re.IGNORECASE)
        ep = 0
        gp = constant.initial_gp
        if (len(ep_match) == 1):
            ep = int(ep_match[0])
        if (len(gp_match) == 1):
            gp = int(gp_match[0])

        cfg.raider_dict.update(
            {game_id: Raider(game_id, ep, gp, False, False, None, None)})
        await message.author.send('新ID添加成功, 需要用户自己更新User ID')
    else:
        await message.author.send('请指定新的游戏ID')


async def decay(message):
    if (len(cfg.raider_dict) != 0):
        await message.author.send('You cannot decay while in the session')
        return

    source.load_epgp_from_json_to_memory()

    for raider in cfg.raider_dict.values():
        util.set_ep(raider.ID,
                    int(constant.decay_factor * util.get_ep(raider.ID)))
        util.set_gp(raider.ID,
                    int(constant.decay_factor * util.get_gp(raider.ID)))

    await source.dump_epgp_from_memory_to_json(message)

    cfg.raider_dict = {}

    await message.channel.send("Deacy 成功，系数为%s" % (constant.decay_factor))
    util.log_msg("Deacy 成功，系数为%s" % (constant.decay_factor))


async def standby(message):
    if (len(cfg.raider_dict) == 0):
        await message.author.send(
            'Please start a raid session to add new raid member')
        return

    game_id_match = re.findall("-id ([^ ]+)", message.content, re.IGNORECASE)

    if (len(game_id_match) == 1):
        game_id = game_id_match[0]

        if (cfg.raider_dict.get(game_id) == None):
            await message.author.send('无法找到该ID')
            return

        if (cfg.raider_dict[game_id].in_raid != True):
            await message.author.send('该ID并未在Raid中')
            return

        cfg.raider_dict[game_id].stand_by = True
        await cfg.admin_msg.edit(embed=view.admin_embed())

        util.log_msg("%s stand by" % (game_id))


async def adjust(message):
    # raider_dict can be empty only the raid is not started.
    if (len(cfg.raider_dict) == 0):
        await message.author.send('Please start a raid session to adjust ep/gp'
                                  )
        return

    game_id_match = re.findall("-id ([^ ]+)", message.content, re.IGNORECASE)

    if (len(game_id_match) == 1):
        game_id = game_id_match[0]

        if (cfg.raider_dict.get(game_id) == None):
            await message.author.send('无法找到该ID')
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
        util.log_msg(adjust_message)
    else:
        await message.author.send('请指定游戏ID')


async def gbid(message):
    # raider_dict can be empty only the raid is not started.
    if (len(cfg.raider_dict) == 0):
        await message.author.send('Please start a raid session to adjust ep/gp'
                                  )
        return

    if (cfg.curret_loot == None):
        await message.author.send('Not distributing')
        return

    game_id_match = re.findall("-id ([^ ]+)", message.content, re.IGNORECASE)

    if (len(game_id_match) == 1):
        game_id = game_id_match[0]

        if (cfg.raider_dict.get(game_id) == None):
            await message.author.send('无法找到该ID')
            return

        loot_match = re.findall("-l ([^ ]+)", message.content, re.IGNORECASE)

        if (len(loot_match) == 1):
            if (cfg.loot_dict.get(loot_match[0]) == None):
                await message.author.send('无法找到该装备， 请检查loot输入')
                return

            loot = cfg.loot_dict.get(loot_match[0])
            gp = int(int(loot.GP) * constant.gp_gbid_factor)
            gp_before = util.get_gp(game_id)
            util.set_gp(game_id, gp_before + gp)
            adjust_message = '%s, gbid: %s, 20%% GP:%s, 购买者: %s, Before GP: %s, After GP: %s' % (
                loot.NAME, gbid, gp, game_id, gp_before, util.get_gp(game_id))
            await message.author.send(adjust_message)
            util.log_msg(adjust_message)
        else:
            await message.author.send('请确认物品')
    else:
        await message.author.send('请指定游戏ID')
