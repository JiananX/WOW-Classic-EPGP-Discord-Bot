from view.embed.admin_embed import admin_embed_view
from view.embed.loot_embed import loot_embed_view, loot_result_embed_view
from view.embed.raider_embed import raider_embed_view

from view.button.admin_button import admin_cancel_button, admin_reward_buttons
from view.button.loot_button import loot_button

from view.menu.loot_menu import boss_menu
from view.menu.raider_menu import loot_raider_menu

import cfg
import constant


async def send_initial_message():
    cfg.admin_msg = await cfg.admin_channel.send(
        embed=admin_embed_view(),
        components=boss_menu() + admin_cancel_button + admin_reward_buttons)

    cfg.raider_msg = await cfg.raider_channel.send(embed=raider_embed_view())


async def update_admin_view():
    if (cfg.is_distributing == False):
        await cfg.admin_msg.edit(embed=admin_embed_view(),
                                 components=cfg.next_menu +
                                 admin_cancel_button + admin_reward_buttons)
    else:
        await cfg.admin_msg.edit(embed=admin_embed_view(),
                                 components=admin_reward_buttons)


async def update_raider_view():
    await cfg.raider_msg.edit(embed=raider_embed_view())


async def send_loot_message(loot_names):
    cfg.is_distributing = True
    for loot_name in loot_names:
        await cfg.raider_channel.send(
            embed=loot_embed_view(loot_name),
            components=loot_button(loot_name),
            delete_after=constant.loot_announcement_duration)

        await cfg.admin_channel.send(
            embed=loot_embed_view(loot_name),
            components=loot_button(loot_name),
            delete_after=constant.loot_announcement_duration)


async def send_loot_result_message(loot_names):
    for loot_name in loot_names:
        await cfg.raider_channel.send(
            embed=loot_result_embed_view(loot_name),
            delete_after=constant.loot_announcement_duration)

        menus = loot_raider_menu(loot_name)
        if (len(menus) != 0):
            await cfg.admin_channel.send(
                embed=loot_result_embed_view(loot_name), components=menus)
    cfg.is_distributing = False
