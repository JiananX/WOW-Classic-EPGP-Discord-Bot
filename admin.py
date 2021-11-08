from raider import Raider

import cfg
import constant
import re
import util
import view
import time
import source


async def start_new_raid(message):
    if (cfg.admin != None):
        await message.channel.send('%s已经开始本次Raid，请稍后再试' % (cfg.admin))
        return

    cfg.admin = message.author
    cfg.stamp = str(time.time())

    source.load_loot_from_json_to_memory()
    source.load_epgp_from_json_to_memory()

    # Reset some of the fields read from source
    for raider in cfg.raider_dict.values():
        raider.in_raid = False
        raider.stand_by = False

    cfg.admin_msg = await message.channel.send(
        '%s开始本次Raid' % (cfg.admin),
        embed=view.loot_admin_embed(),
        components=view.loot_admin_view_component(False, False))

    util.log_msg('%s开始Raid' % (cfg.admin))

async def sync_from_discord_channel(message, client):
    channel = client.get_channel(constant.channel)
    members = channel.members

    memids = []
    for member in members:
        memids.append(member.name)
        for name, raider in cfg.raider_dict.items():
            if raider.author_id == member.id:
                raider.in_raid = True
                msg = await member.send(
                     '欢迎参加本次Raid %s' % (name),
                     components=view.user_view_component(False),
                     embed=view.my_pr_embed(member.id))
                cfg.raid_user_msg.update({member.id: msg})

                #Update roster section of admin view
                await cfg.admin_msg.edit(embed=view.loot_admin_embed())
                util.log_msg('%s 加入Raid' % name)
    await message.channel.send('以下加入Raid：' + str(memids))

async def recover_raid(message, client):
    if (cfg.admin != None):
        await message.channel.send('%s已经开始本次Raid，请稍后再试' % (cfg.admin))
        return

    cfg.admin = message.author
    cfg.stamp = str(time.time())

    source.load_loot_from_json_to_memory()
    source.load_epgp_from_json_to_memory()

    for raider in cfg.raider_dict.values():
        if ((raider.in_raid == True) & (raider.stand_by == False) &
            (raider.author_id != None)):
            user = await client.fetch_user(raider.author_id)
            msg = await user.send('重新参加本次Raid %s' % (raider.ID),
                                  components=view.user_view_component(False),
                                  embed=view.my_pr_embed(raider.author.id))
            cfg.raid_user_msg.update({user.id: msg})
            # Need to re-assign the user obj to author, as during json transformation,
            # author will be translate to string
            raider.author = user
        else:
            raider.in_raid = False
            raider.stand_by = False

    cfg.admin_msg = await message.channel.send(
        '%s重新开始本次Raid' % (cfg.admin),
        embed=view.loot_admin_embed(),
        components=view.loot_admin_view_component(False, False))


async def add_new_member(message):
    game_id_match = re.findall("-id ([^ ]+)", message.content, re.IGNORECASE)

    if (len(game_id_match) == 1):
        # raider_dict can be empty only the raid is not started.
        if (len(cfg.raider_dict) == 0):
            await message.author.send(
                'Please start a raid session to add new raid member')
            return

        game_id = game_id_match[0]

        ep_match = re.findall("-ep ([0-9]+)", message.content, re.IGNORECASE)
        gp_match = re.findall("-gp ([0-9]+)", message.content, re.IGNORECASE)
        ep = 0
        gp = constant.initial_gp
        if (len(ep_match) == 1):
            ep = int(ep_match[0])
        if (len(gp_match) == 1):
            gp = int(gp_match[0])

        if (cfg.raider_dict.get(game_id) != None):
            await message.author.send('当前游戏ID已经存在于DB')
            cfg.raider_dict = {}
            return

        cfg.raider_dict.update(
            {game_id: Raider(game_id, ep, gp, False, False, None, None)})
        await message.author.send('新ID添加成功')
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
    game_id = message.content.split(" ")[2]

    # raider_dict can be empty only the raid is not started.
    if (len(cfg.raider_dict) == 0):
        await message.author.send(
            'Please start a raid session to add new raid member')
        return

    if (cfg.raider_dict.get(game_id) == None):
        await message.author.send('无法找到该ID')
        return

    if (cfg.raider_dict[game_id].in_raid != True):
        await message.author.send('该ID并未在Raid中')
        return

    cfg.raider_dict[game_id].stand_by = True

    await cfg.admin_msg.edit(embed=view.loot_admin_embed())
    util.log_msg("%s stand by" % (game_id))


async def adjust(message):
    game_id_match = re.findall("-id ([^ ]+)", message.content, re.IGNORECASE)

    if (len(game_id_match) == 1):
        game_id = game_id_match[0]

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

        # raider_dict can be empty only the raid is not started.
        if (len(cfg.raider_dict) == 0):
            await message.author.send(
                'Please start a raid session to adjust ep/gp')
            return

        if (cfg.raider_dict.get(game_id) == None):
            await message.author.send('无法找到该ID')
            return

        ep_before = util.get_ep(game_id)
        gp_before = util.get_gp(game_id)
        util.set_ep(game_id, ep_before + ep)
        util.set_gp(game_id, gp_before + gp)

        adjust_message = '调整成功 ID: %s Before EP: %s, GP: %s, After EP: %s, GP: %s' % (
            game_id, ep_before, gp_before, util.get_ep(game_id), util.get_gp(game_id))

        reason_match = re.findall("-r ([^ ]+)", message.content, re.IGNORECASE)
        if (len(reason_match) == 1):
          adjust_message += ', 原因: %s'%(reason_match[0]);
          
        await message.author.send(adjust_message)
        util.log_msg(adjust_message)
    else:
        await message.author.send('请指定游戏ID')

async def gbid(message):
    game_id_match = re.findall("-id ([^ ]+)", message.content, re.IGNORECASE)

    if (len(game_id_match) == 1):
        game_id = game_id_match[0]

        loot_match = re.findall("-l ([^ ]+)", message.content,
                              re.IGNORECASE)
        gbid_match = re.findall("-g ([0-9]+)", message.content,
                              re.IGNORECASE)
        gp = 0;
        loot = None;
        if (len(loot_match) == 1):
            if (cfg.loot_dict.get(loot_match[0]) == None):
                await message.author.send('无法找到该装备， 请检查loot输入')
                return
            else:
                loot = cfg.loot_dict.get(loot_match[0])
                gp = int(int(loot.GP) * constant.gp_gbid_factor)
        if (len(gbid_match) == 1):
            gbid = int(gbid_match[0])

        # raider_dict can be empty only the raid is not started.
        if (len(cfg.raider_dict) == 0):
            await message.author.send(
                'Please start a raid session to adjust ep/gp')
            return

        if (cfg.raider_dict.get(game_id) == None):
            await message.author.send('无法找到该ID')
            return

        gp_before = util.get_gp(game_id)
        util.set_gp(game_id, gp_before + gp)

        adjust_message = '%s, gbid: %s, 20%% GP:%s, 购买者: %s, Before GP: %s, After GP: %s' % (
           loot.NAME, gbid, gp, game_id, gp_before, util.get_gp(game_id))
        await message.author.send(adjust_message)
        util.log_msg(adjust_message)
    else:
        await message.author.send('请指定游戏ID')
