from discord_components import ComponentsBot

from command.admin_command import add_new_member,adjust
from command.raider_command import update_user_id

from infra.source import load_loot_from_json_to_memory, load_epgp_from_json_to_memory

from menu_callback.menu_callback import all_paths_callback

from view.menu.menu import all_paths
from view.view import send_initial_message, update_admin_view, update_raider_view

from  emojis import emojis

import wcl.wcl

import asyncio
import cfg
import constant
import discord
import json
import re
import util

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

    load_loot_from_json_to_memory()
    load_epgp_from_json_to_memory()

    # Reset some of the fields read from source
    for raider in cfg.raider_dict.values():
        raider.in_raid = False
        raider.stand_by = False

    cfg.loot_channel = await bot.fetch_channel(constant.loot_channel)

    raid_voice_channel = bot.get_channel(constant.raid_channel)

    admin_channel = await bot.fetch_user(723015651932897312)

    for member_id in raid_voice_channel.voice_states.keys():
        for name, raider in cfg.raider_dict.items():
            if raider.author_id == member_id:
                raider.in_raid = True

    async for message in cfg.loot_channel.history():
        await message.delete()

    async for message in admin_channel.history():
        if message.author.id != 723015651932897312:
            await message.delete()

    
    for name, id in emojis.items():
      cfg.emojis_dict.update({name: bot.get_emoji(id)})

    await send_initial_message(admin_channel)

    print('CF Senior EPGP start')


@bot.event
async def on_voice_state_update(member, before, after):
    if (len(cfg.raider_dict) == 0):
        return

    new_channel = after.channel
    before_channel = before.channel

    if (new_channel is not None and new_channel.id == constant.raid_channel):
        print('%s joined server' % (member.name))

        for raider in cfg.raider_dict.values():
            if raider.author_id == member.id:
                raider.in_raid = True
                break
    elif ((new_channel is None or new_channel.id != constant.raid_channel)
          and (before_channel is not None)
          and (before_channel.id == constant.raid_channel)):
        print('%s left server' % (member.name))

        for raider in cfg.raider_dict.values():
            if raider.author_id == member.id:
                raider.in_raid = False
                break


@bot.event
async def on_message(message):
    if (type(message.channel) is not discord.DMChannel):
        return

    if (message.author == bot.user):
        return

    if (util.is_match(constant.add_new_member_reg, message.content)):
        if (str(message.author) not in admin_tokens):
            await message.channel.send('You are not admin')
            return

        await add_new_member(message)
    
    if (util.is_match(constant.adjust_reg, message.content)):
        if (str(message.author) not in admin_tokens):
            await message.channel.send('You are not admin')
            return

        await adjust(message)
    
    if (util.is_match(constant.update_reg, message.content)):
        await update_user_id(message)


@bot.event
async def on_button_click(interaction):
    custom_id = interaction.custom_id

    if (custom_id == None):
        return
    elif (custom_id.startswith('loot')):
        user_id = interaction.user.id

        if (user_id in cfg.main_spec or user_id in cfg.off_spec):
            return

        if (custom_id == constant.loot_main_spec_id):
            cfg.main_spec.append(user_id)
        elif (custom_id == constant.loot_off_spec_id):
            cfg.off_spec.append(interaction.user.id)
        
        # TODO: Consider response with another response type other than edit message
        await interaction.respond(type=constant.edit_message_response_type)
    elif (custom_id.startswith('admin')):
        if ('confirm' in custom_id):
            callback = all_paths_callback[all_paths.index(cfg.admin_path)]
            # Invoke the proper callback for the given menu path
            # 1) Loot distribution is an async operation
            # 2) Other are sync operation
            if (cfg.admin_path_values[constant.main_menu_id][0] ==
                    'announce_loot_to_raider'):
                # Due to the task could start after the admin_path is cleared, so we wil need to pass the proper loot it
                cfg.loot_msg = 'distributing %s' %(cfg.admin_path_values[constant.loot_menu_id][0])
                asyncio.create_task(
                    callback(cfg.admin_path_values[constant.loot_menu_id][0]))
            else:
                callback()

        cfg.admin_path = []
        cfg.admin_path_values = {}

        await update_admin_view()
        await update_raider_view()

        await interaction.respond(type=constant.edit_message_response_type)


@bot.event
async def on_select_option(interaction):
    if (len(interaction.values) == 0):
        return

    path = None
    valid_value = []
    for value in interaction.values:
        match = re.findall('-path ([^ ]+) -value ([^ ]+)', value)
        valid_value.append(match[0][1])
        path = match[0][0]

    cfg.admin_path.append(path)
    cfg.admin_path_values.update({interaction.custom_id: valid_value})

    await update_admin_view()

    await interaction.respond(type=constant.edit_message_response_type)


def initialize_global_vars():
    cfg.raider_dict = {}
    cfg.loot_dict = {}
    cfg.emojis_dict = {}

    cfg.main_spec = []
    cfg.off_spec = []

    cfg.admin_msg = None
    cfg.raider_msg = None

    cfg.admin_path = []
    cfg.admin_path_values = {}

    cfg.loot_msg = 'No loot event yet'


#bot.run(discord_token)
wcl.wcl.query_basic_report("CfLZBJWwqxbmac36")
#wcl.wcl.query_basic_report("bVGMz4ArFp3txHN1")
wcl.wcl.send_out_res()
