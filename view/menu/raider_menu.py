from discord_components import Select, SelectOption

import cfg
import util


def loot_raider_menu(loot_name):
    menus = []

    if (len(cfg.main_spec[loot_name]) != 0):
        menus.append(
            _try_to_create_menu(cfg.main_spec[loot_name], '主天赋', loot_name,
                                100))

    if (len(cfg.off_spec[loot_name]) != 0):
        menus.append(
            _try_to_create_menu(cfg.off_spec[loot_name], '副天赋', loot_name, 20))

    # if (len(cfg.minor_improve[loot_name]) != 0):
    #     menus.append(
    #         _try_to_create_menu(cfg.minor_improve[loot_name], '小提升', loot_name,
    #                             20))

    if (len(cfg.gbid[loot_name]) != 0):
        menus.append(
            _try_to_create_menu(cfg.gbid[loot_name], '拍金', loot_name, 1))

    return menus


def _try_to_create_menu(user_ids, placeholder, loot_name, percentage):
    options = []
    for user_id in user_ids:
        options.append(
            SelectOption(label='%s' % (util.find_raider_name(user_id)),
                         value=util.find_raider_name(user_id)))

    return Select(placeholder=placeholder,
                  custom_id='distribute -loot %s -percentage %s' %
                  (loot_name, percentage),
                  options=options,
                  max_values=len(options))
