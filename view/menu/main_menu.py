from discord_components import Select, SelectOption

import cfg
import constant
import util


def distribute_operation():
    return SelectOption(label='Loot',
                        value=util.build_admin_path(
                            constant.loot_operation_path,
                            'announce_loot_to_raider'),
                        emoji=cfg.emojis_dict['loot_emoji'],
                        description='Announce the loot')


def adjust_operation():
    return SelectOption(
        label='Adjust',
        value=util.build_admin_path(constant.adjust_operation_path,
                                    'adjust_ep_gp'),
        emoji=cfg.emojis_dict['epgp_emoji'],
        description='Decay, reward, distribute loot and manual adjust')


def raider_operation():
    return SelectOption(
        label='Raider',
        value=util.build_admin_path(constant.raider_operation_path,
                                    'update_raider_status'),
        emoji=cfg.emojis_dict['raider_emoji'],
        description='Raider related operations including standby')


def system_operation():
    return SelectOption(
        label='System',
        value=util.build_admin_path(constant.system_operation_path,
                                    'system_related_operation'),
        emoji=cfg.emojis_dict['system_emoji'],
        description='System operation among gsheet, memory and json')


def main_menu():
    return [
        Select(custom_id=constant.main_menu_id,
               options=[
                   distribute_operation(),
                   adjust_operation(),
                   raider_operation(),
                   system_operation()
               ])
    ]
