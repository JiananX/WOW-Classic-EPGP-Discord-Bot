from discord_components import Select, SelectOption

import cfg
import constant


def boss_menu():
    options = []
    for boss in _find_bosses():
        options.append(SelectOption(label='%s' % (boss), value=boss))
    return [Select(custom_id=constant.boss_menu_id, options=options)]


def loot_menu(boss):
    loots = []
    for loot in cfg.loot_dict.values():
        if (loot.boss == boss):
            loots.append(loot)

    options = []
    for loot in loots:
        options.append(SelectOption(label='%s' % (loot.name), value=loot.name))

    return [
        Select(custom_id=constant.loot_menu_id,
               options=options,
               max_values=len(options))
    ]


def _find_bosses():
    bosses = []
    for loot in cfg.loot_dict.values():
        bosses.append(loot.boss)

    return set(bosses)
