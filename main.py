from discord_components import ComponentsBot

import admin
import cfg
import constant
import discord
import distribute
import json
import re
import source
import util
import view

bot = ComponentsBot('?')
util.start_logger()

admin_tokens = None
discord_token = None
with open('local_settings.json') as infile:
    data = json.load(infile)
    admin_tokens = data['admin_token']
    discord_token = data['discord_token']


@bot.event
async def on_ready():
    initialize_global_vars()

    cfg.loot_channel = await bot.fetch_channel(constant.loot_channel)

    print('CF Senior EPGP start')


@bot.event
async def on_voice_state_update(member, before, after):
    if (len(cfg.raider_dict) == 0):
        return

    newChannel = after.channel

    if (newChannel is not None and newChannel.id == constant.raid_channel):
        print('%s joined server' % (member.name))

        for raider in cfg.raider_dict.values():
            if raider.author_id == member.id & raider.in_raid == False:
                raider.in_raid = True
                await view.update_admin_view()
                await view.update_raider_view()
                break
    elif ((newChannel is None or newChannel.id != constant.raid_channel)
          and (before.channel is not None) and
          (before.channel.id == constant.raid_channel)):
        print('%s left server' % (member.name))

        for raider in cfg.raider_dict.values():
            if raider.author_id == member.id & raider.in_raid == True:
                raider.in_raid = False
                await view.update_admin_view()
                await view.update_raider_view()
                break


@bot.event
async def on_message(message):
    if (type(message.channel) is not discord.DMChannel):
        return

    if (message.author == bot.user):
        return

    if (match_keywork(constant.admin_reg, message)):
        if (str(message.author) not in admin_tokens):
            await message.channel.send('You are not admin')
            return

        await on_admin_message(message)
    else:
        if (len(cfg.raider_dict) == 0):
            await message.channel.send('The raid has not started yet')
            return

        if (match_keywork(constant.announcement_reg, message)):
            if (str(message.author) not in admin_tokens):
                await message.channel.send('You are not admin')
                return

            await distribute.announcement(message)

        if (match_keywork(constant.update_reg, message)):
            game_id = message.content.split(" ")[1]

            if (cfg.raider_dict.get(game_id) == None):
                await message.channel.send('Invalid game id')
                return

            cfg.raider_dict[game_id].in_raid = True
            cfg.raider_dict[game_id].author_id = message.author.id

            await view.update_admin_view()
            await view.update_raider_view()

            await message.send('User id gets updated successfully')


async def on_admin_message(message):
    if (match_keywork(constant.start_new_raid_reg, message)):
        await admin.start_new_raid(message, bot)
    elif (match_keywork(constant.add_new_member_reg, message)):
        await admin.add_new_member(message)
    elif (match_keywork(constant.decay_reg, message)):
        await admin.decay(message)
    elif (match_keywork(constant.adjust_reg, message)):
        await admin.adjust(message)
    elif (match_keywork(constant.gbid_reg, message)):
        await admin.gbid(message)
    elif (match_keywork(constant.standby_reg, message)):
        await admin.standby(message)
    elif (match_keywork(constant.sync_epgp_from_gsheet_to_json, message)):
        await source.sync_epgp_from_gsheet_to_json(message)
    elif (match_keywork(constant.sync_loot_from_gsheet_to_json, message)):
        await source.sync_loot_from_gsheet_to_json(message)
    elif (match_keywork(constant.load_epgp_from_json_to_memory, message)):
        source.load_epgp_from_json_to_memory()
    elif (match_keywork(constant.load_loot_from_json_to_memory, message)):
        source.load_loot_from_json_to_memory()
    elif (match_keywork(constant.dump_epgp_from_memory_to_json, message)):
        await source.dump_epgp_from_memory_to_json(message)
    elif (match_keywork(constant.dump_loot_from_memory_to_json, message)):
        source.dump_loot_from_memory_to_json()
    else:
        await message.author.send('''
        指令              用途
      Admin|a start      开始raid
      Admin|a add -id    游戏ID [-ep XX] [-gp XX] 添加新的游戏ID到DB
      Admin|a decay      衰减DB中所有的EP/GP
      Admin|a adjust -id 游戏ID [-ep XX] [-gp XX] [-r 原因] 修改游戏ID的EP/GP
      Admin|a gbid -id 游戏ID [-l XX] 记录gbid交易
      Admin|a standby -id 游戏ID 替补游戏ID
      Admin|a g2js pr    Gsheet中导入所有人的pr信息到epgp.json文件
      Admin|a g2js loot  Gsheet中导入所有loot信息到loot.json文件
      Admin|a js2m pr    epgp.json导入epgp对象
      Admin|a js2m loot  loot.json导入loot对象
      Admin|a (write|w)  epgp对象导入epgp.json
      Admin|a m2js loot  loot对象导入loot.json
      ''')


@bot.event
async def on_button_click(interaction):
    custom_id = interaction.custom_id

    if (custom_id == None):
        return
    elif (custom_id.startswith('loot')):
        await on_loot_view_click(interaction)
    elif (custom_id.startswith('reward')):
        await on_reward_click(interaction)


async def on_loot_view_click(interaction):
    custom_id = interaction.custom_id

    if (custom_id == (constant.loot_off_spec_confirm_id + cfg.stamp)):
        await distribute.confirm(constant.gp_off_spec_factor)
    elif (custom_id == (constant.loot_main_spec_confirm_id + cfg.stamp)):
        await distribute.confirm(constant.gp_main_spec_factor)
    elif (custom_id == (constant.loot_cancel_id + cfg.stamp)):
        await distribute.cancel()
    elif (custom_id == (constant.loot_main_spec_id + cfg.stamp)):
        user_id = interaction.user.id
        if ((user_id not in cfg.main_spec) & (user_id not in cfg.off_spec)):
            cfg.main_spec.append(user_id)
    elif (custom_id == (constant.loot_off_spec_id + cfg.stamp)):
        user_id = interaction.user.id
        if ((user_id not in cfg.main_spec) & (user_id not in cfg.off_spec)):
            cfg.off_spec.append(interaction.user.id)

    if (custom_id.endswith(cfg.stamp)):
        await interaction.respond(
            type=constant.update_message_button_response_type)


async def on_reward_click(interaction):
    custom_id = interaction.custom_id

    match = re.fullmatch("reward_(20|150|200)%s" % (cfg.stamp), custom_id)
    if (match):
        ep = int(match[1])

        eligible_raiders = []
        for raider in cfg.raider_dict.values():
            if ((raider.in_raid == True) & (raider.stand_by == False)):
                util.set_ep(raider.ID, ep + util.get_ep(raider.ID))
                eligible_raiders.append(raider.ID)

        await view.update_raider_view()

        await interaction.respond(
            type=constant.update_message_button_response_type)
        util.log_msg('%sEP奖励给%s' % (ep, eligible_raiders))


def match_keywork(keyword, message):
    return re.fullmatch(keyword, message.content, re.IGNORECASE)


def initialize_global_vars():
    cfg.stamp = ''
    cfg.raider_dict = {}
    cfg.loot_dict = {}

    cfg.main_spec = None
    cfg.off_spec = None
    cfg.current_winner = None
    cfg.current_loot = None

    cfg.admin_msg = None
    cfg.raider_msg = None


bot.run(discord_token)
