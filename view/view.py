from discord_components import ActionRow

from view.embed.admin_embed import admin_embed_view
from view.embed.loot_embed import loot_embed_view
from view.embed.raider_embed import raider_embed_view

from view.button.admin_button import admin_cancel_button, admin_confirm_button
from view.button.loot_button import loot_button

from view.menu.epgp_menu import adjust_menu, epgp_menu, percentage_menu
from view.menu.loot_menu import boss_menu, loot_menu
from view.menu.main_menu import main_menu
from view.menu.raider_menu import raider_menu, raider_operation_menu
from view.menu.system_menu import system_menu
from view.menu.menu import all_paths

import cfg
import constant


async def send_initial_message(admin_channel):
    cfg.admin_msg = await admin_channel.send(
        embed=admin_embed_view(),
        components=[main_menu(), admin_cancel_button])

    cfg.raider_msg = await cfg.loot_channel.send(embed=raider_embed_view())


async def send_loot_message(loot):
    return await cfg.loot_channel.send(
        embed=loot_embed_view(loot),
        components=[loot_button],
        delete_after=constant.loot_announcement_duration)


async def update_admin_view():
    if (len(cfg.admin_path) == 0):
        await cfg.admin_msg.edit(embed=admin_embed_view(),
                                 components=[main_menu(),
                                             admin_cancel_button])
    else:
        next_menu = _find_next_menu()

        if (next_menu is not None):
            await cfg.admin_msg.edit(
                embed=admin_embed_view(),
                components=[next_menu, admin_cancel_button])
        else:
            # Do not response 7 for the final message, otherwise the message will be flushed
            await cfg.admin_msg.edit(embed=admin_embed_view(),
                                     components=[
                                         ActionRow(admin_confirm_button,
                                                   admin_cancel_button)
                                     ])


async def update_raider_view():
    await cfg.raider_msg.edit(embed=raider_embed_view())


def _find_next_menu():
    for operation_path in all_paths:
        # 1) No need to care the operation_path is shorter than admin_path
        # 2) If the length if the same, then it means regardless whether it is the correct path, we already reach the end of it and no need to find the next menu
        if (len(operation_path) <= len(cfg.admin_path)):
            continue

        for idx, path in enumerate(cfg.admin_path):
            if (path != operation_path[idx]):
                break

            if (idx == len(cfg.admin_path) - 1):
                return _generate_menu(operation_path[idx + 1])

    return None


def _generate_menu(path):
    if (path in [
            constant.adjust_operation_path, constant.system_operation_path,
            constant.loot_operation_path, constant.raider_operation_path
    ]):
        return main_menu()
    elif (path in [
            constant.reward_adjust_path, constant.loot_adjust_path,
            constant.manual_adjust_path, constant.decay_adjust_path
    ]):
        return adjust_menu
    elif (path == constant.epgp_path):
        return epgp_menu
    elif (path == constant.loot_id_path):
        return loot_menu(cfg.admin_path_values[constant.boss_menu_id][0])
    elif (path == constant.boss_id_path):
        return boss_menu()
    elif (path == constant.percentage_path):
        return percentage_menu
    elif (path == constant.raider_path):
        return raider_menu()
    elif (path == constant.standby_raider_path):
        return raider_operation_menu
    elif (path == constant.system_path):
        return system_menu
