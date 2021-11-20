from discord_components import Select, SelectOption

import cfg
import constant
import util

bosses = [
    '奥', '大星术师索兰莉安', '空灵机甲', '凯尔萨斯王子', '风暴要塞小怪', '海度斯', '深水领主', '盲眼', '踏潮',
    '鱼斯拉', '瓦斯琪', '毒蛇神殿小怪'
]


def boss_menu():
    options = []
    for boss in bosses:
        options.append(
            SelectOption(label='%s' % (boss),
                         value=util.build_admin_path(constant.boss_id_path,
                                                     boss)))
    return [Select(custom_id=constant.boss_menu_id, options=options)]


def loot_menu(boss):
    loots = []
    for loot in cfg.loot_dict.values():
        if (loot.boss == boss):
            loots.append(loot)

    options = []
    for loot in loots:
        options.append(
            SelectOption(label='%s' % (loot.name),
                         value=util.build_admin_path(constant.loot_id_path,
                                                     loot.name)))

    return [Select(custom_id=constant.loot_menu_id, options=options, max_values=len(options))]
