from discord_components import ComponentsBot

from command.admin_command import add_new_member, adjust
from command.raider_command import update_user_id

from infra.source import load_loot_from_json_to_memory, load_epgp_from_json_to_memory

from menu_callback.menu_callback import all_paths_callback

from view.menu.menu import all_paths
from view.view import send_initial_message, update_admin_view, update_raider_view
from emojis import emojis

import asyncio
import cfg
import constant
import discord
import history
import json
import re
import util

bot = ComponentsBot('?')
history.start_logger()

discord_token = None
admin_user_id = None
with open('local_settings.json') as infile:
    data = json.load(infile)
    discord_token = data['discord_token']
    admin_user_id = int(data['admin_user_id'])

cfg.raider_dict = {}
cfg.loot_dict = {}
cfg.emojis_dict = {}

cfg.admin_path = []
cfg.admin_path_values = {}

cfg.event_msg = 'No event yet'


@bot.event
async def on_ready():
    load_loot_from_json_to_memory()
    load_epgp_from_json_to_memory()

    cfg.raider_channel = await bot.fetch_channel(constant.loot_channel)
    cfg.admin_channel = await bot.fetch_user(admin_user_id)

    raid_voice_channel = await bot.fetch_channel(constant.raid_channel)
    for member_id in raid_voice_channel.voice_states.keys():
        for name, raider in cfg.raider_dict.items():
            if raider.user_id == member_id:
                raider.in_raid = True

    async for message in cfg.raider_channel.history():
        await message.delete()

    async for message in cfg.admin_channel.history():
        if message.author.id != admin_user_id:
            await message.delete()

    for name, id in emojis.items():
        cfg.emojis_dict.update({name: bot.get_emoji(id)})

    await send_initial_message()

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
            if raider.user_id == member.id:
                raider.in_raid = True
                await update_admin_view()
                await update_raider_view()
                break
    elif ((new_channel is None or new_channel.id != constant.raid_channel)
          and (before_channel is not None)
          and (before_channel.id == constant.raid_channel)):
        print('%s left server' % (member.name))

        for raider in cfg.raider_dict.values():
            if raider.user_id == member.id:
                raider.in_raid = False
                await update_admin_view()
                await update_raider_view()
                break


@bot.event
async def on_message(message):
    if (type(message.channel) is not discord.DMChannel):
        return

    if (message.author == bot.user):
        return

    if (util.is_match(constant.add_new_member_reg, message.content)):
        await add_new_member(message)

    if (util.is_match(constant.adjust_reg, message.content)):
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
        loot_name = custom_id.split(' ')[1]

        if (user_id in cfg.main_spec[loot_name] or user_id in cfg.off_spec[loot_name]):
            return

        if (custom_id.startswith(constant.loot_main_spec_id)):  
            cfg.main_spec[loot_name].append(interaction.user.id)
        elif (custom_id.startswith(constant.loot_off_spec_id)):
            cfg.off_spec[loot_name].append(interaction.user.id)

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
                cfg.loot_msg = 'distributing %s' % (
                    cfg.admin_path_values[constant.loot_menu_id])
                asyncio.create_task(
                    callback(cfg.admin_path_values[constant.loot_menu_id]))
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

    if (interaction.custom_id.startswith('distribute')):
        info = interaction.custom_id.split(' ')
        raider_name = interaction.values[0]
        loot = cfg.loot_dict[info[2]]
        if (info[1] == 'main'):
            util.set_gp(raider_name, util.get_gp(raider_name) + loot.gp)
            history.log_adjustment([raider_name], loot=loot, gp=loot.gp)
        elif (info[1] == 'off'):
            util.set_gp(raider_name,
                        util.get_gp(raider_name) + int(loot.gp / 2))
            history.log_adjustment([raider_name],
                                   loot=loot,
                                   gp=int(loot.gp / 2))

        cfg.even_msg = 'Distribute %s successfully' % (loot.name)

        await update_raider_view()
    else:
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


bot.run(discord_token)