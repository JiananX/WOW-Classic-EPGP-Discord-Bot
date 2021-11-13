from discord_components import Select, SelectOption

import constant
import util

reward_operation = SelectOption(label='Reward Raid',
                                value=util.build_admin_path(
                                    constant.reward_adjust_path,
                                    'reward_raid'))
manual_operation = SelectOption(label='Manual Adjust',
                                value=util.build_admin_path(
                                    constant.manual_adjust_path,
                                    'manual_adjust_ep_gp'))
loot_operation = SelectOption(label='Based on Loot',
                              value=util.build_admin_path(
                                  constant.loot_adjust_path,
                                  'adjust_gp_based_on_loot'))
decay_operation = SelectOption(label='Decay',
                               value=util.build_admin_path(
                                   constant.decay_adjust_path, 'decay'))


def ep_option(ep):
    return SelectOption(label='%s EP' % (ep),
                        value=util.build_admin_path(constant.epgp_path,
                                                    '%s_EP' % (ep)))


def gp_option(gp):
    return SelectOption(label='%s GP' % (gp),
                        value=util.build_admin_path(constant.epgp_path,
                                                    '%s_GP' % (gp)))


def percentage_option(percentage):
    return SelectOption(label='%s%%' % (int(percentage * 100)),
                        value=util.build_admin_path(constant.percentage_path,
                                                    str(percentage)))


adjust_menu = Select(custom_id=constant.adjust_menu_id,
                     options=[
                         reward_operation, manual_operation, loot_operation,
                         decay_operation
                     ])

epgp_menu = Select(custom_id=constant.epgp_menu_id,
                   options=[
                       ep_option(20),
                       ep_option(100),
                       ep_option(200),
                       gp_option(100),
                       gp_option(200),
                   ])
percentage_menu = Select(custom_id=constant.percentage_menu,
                         options=[
                             percentage_option(0.1),
                             percentage_option(0.2),
                             percentage_option(0.5),
                             percentage_option(1),
                         ])
