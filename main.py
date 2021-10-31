from discord_components import ComponentsBot

import admin
import cfg
import constant
import distribute
import os
import raid
import re
import user
import util
import view

bot = ComponentsBot('?')
util.start_logger()


@bot.event
async def on_ready():
    initialize_global_vars()

    print('CF Senior EPGP start')


@bot.event
async def on_button_click(interaction):
    custom_id = interaction.custom_id

    if (custom_id == None):
      return
    elif (custom_id.startswith('user')):
      await on_user_view_click(interaction)
    elif (custom_id.startswith('loot')):
      await on_loot_view_click(interaction)


@bot.event
async def on_message(message):
    if (message.author == bot.user):
        return

    if (match_keywork(constant.admin_reg, message)):
        await on_admin_message(message)
    elif (match_keywork(constant.raid_op_reg, message)):
        await on_raid_op_message(message)
    elif (match_keywork(constant.dis_reg, message)):
        await on_distribution_message(message)
    else:
        await on_user_message(message)


async def on_user_message(message):
    if (cfg.admin == None):
        await message.channel.send('管理员还未开始本次Raid, 请稍后再试')
        return

    if (match_keywork(constant.login_reg, message)):
        await user.member_login(message)
    else:
        await message.author.send('''
      指令              用途
    Login 游戏ID      进入Raid

    Admin指令（只有管理员可以使用）
    Admin|a 具体指令 (-h for help)
    Distribute|d 具体指令 (-h for help)
    Raid|r 具体指令 (-h for help)
    ''')


async def on_user_view_click(interaction):
    if (cfg.admin == None):
        await interaction.user.send('管理员还未开始本次Raid, 请稍后再试')
        return

    if (cfg.raid_roster.get(interaction.user) == None):
        await interaction.user.send('您还未加入本次Raid')
        return

    if (cfg.raid_user_msg.get(interaction.user) == None):
        return

    author = interaction.user
    custom_id = interaction.custom_id
    if (custom_id == (constant.user_raid_pr_list_id + cfg.stamp)):
        original_msg = cfg.raid_user_msg[author]
        await original_msg.edit(embed=view.raid_pr_embed())
        await interaction.respond(
            type=constant.update_message_button_response_type)
    elif (custom_id == (constant.user_my_pr_id + cfg.stamp)):
        original_msg = cfg.raid_user_msg[author]
        await original_msg.edit(embed=view.my_pr_embed(author))
        await interaction.respond(
            type=constant.update_message_button_response_type)
    elif (custom_id == (constant.user_main_spec_id + cfg.stamp)):
        user.main_spec_response(author)
        original_msg = cfg.raid_user_msg[author]
        await original_msg.edit(components=view.user_view_component(False))
        await interaction.respond(
            type=constant.update_message_button_response_type)


async def on_raid_op_message(message):
    if (str(message.author) not in os.environ['admin_token']):
        await message.channel.send('您不是管理员')
        return

    if (cfg.admin == None):
        await admin.start_new_raid(message)
        return

    if (match_keywork(constant.reward_ep, message)):
        await raid.reward_raid_ep(message)
    elif (match_keywork(constant.retrive_roster, message)):
        await raid.retrive_roster(message)
    else:
        await message.author.send('''
      指令              用途
    Raid|r Roster      Raid名册
    Raid|r reward XX [-r 原因] 奖励raid XX EP
    ''')


async def on_admin_message(message):
    if (str(message.author) not in os.environ['admin_token']):
        await message.channel.send('您不是管理员')
        return

    if (match_keywork(constant.start_new_raid_reg, message)):
        await admin.start_new_raid(message)
    elif (match_keywork(constant.add_new_member_reg, message)):
        await admin.add_new_member(message)
    elif (match_keywork(constant.decay_reg, message)):
        await admin.decay(message)
    elif (match_keywork(constant.adjust_reg, message)):
        await admin.adjust(message)
    elif (match_keywork(constant.sync_epgp_from_gsheet, message)):
        await admin.sync_epgp_from_gsheet(message)
    elif (match_keywork(constant.sync_loot_from_gsheet, message)):
        await admin.sync_loot_from_gsheet(message)
    else:
        await message.author.send('''
      指令              用途
    Admin|a start      开始raid
    Admin|a add -id    游戏ID [-ep XX] [-gp XX] 添加新的游戏ID到DB
    Admin|a decay      衰减DB中所有的EP/GP
    Admin|a adjust -id 游戏ID [-ep XX] [-gp XX] [-r 原因] 修改游戏ID的EP/GP
    Admin|a pull PR    从Gsheet中导入所有人的PR信息
    ''')


async def on_distribution_message(message):
    if (str(message.author) not in os.environ['admin_token']):
        await message.channel.send('您不是管理员')
        return

    if (cfg.admin == None):
        await admin.start_new_raid(message)
        return

    if (match_keywork(constant.announcement_reg, message)):
        await distribute.announcement(message)
    else:
        await message.author.send('''
      指令              用途
      Dis 物品       准备分配物品
    ''')

async def on_loot_view_click(interaction):
    custom_id = interaction.custom_id
    if (custom_id == (constant.loot_gbid_confirm_id + cfg.stamp)):
        await distribute.confirm(0.2);
        await interaction.respond(
            type=constant.update_message_button_response_type)
    elif (custom_id == (constant.loot_main_spec_confirm_id + cfg.stamp)):
        await distribute.confirm(1);
        await interaction.respond(
            type=constant.update_message_button_response_type)
    elif (custom_id == (constant.loot_cancel_id + cfg.stamp)):
        await distribute.cancel();
        await interaction.respond(
            type=constant.update_message_button_response_type)


def match_keywork(keyword, message):
    return re.fullmatch(keyword, message.content, re.IGNORECASE)


def initialize_global_vars():
    cfg.admin = None
    cfg.raid_roster = {}
    cfg.stamp = ''

    cfg.main_spec = None
    cfg.current_item = None
    cfg.current_winner = None
    cfg.is_distributing = False
    cfg.item_gp = None
    cfg.current_loot = None
    cfg.loot_message = None

    cfg.raid_user_msg = {}
    cfg.raid_user_main_spec_button = {}


bot.run(os.environ['discord_token'])
