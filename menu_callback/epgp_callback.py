import cfg
import constant
import util


def adjust_epgp():
    game_ids = []
    ep = 0
    gp = 0
    percentage = 1

    if cfg.admin_path_values.get(constant.raider_menu_id) is not None:
        game_ids = cfg.admin_path_values[constant.raider_menu_id]
    else:
        for raider in cfg.raider_dict.values():
            if ((raider.in_raid == True) & (raider.stand_by == False)):
                game_ids.append(raider.ID)

    if cfg.admin_path_values.get(constant.epgp_menu_id) is not None:
        epgp_value = cfg.admin_path_values[constant.epgp_menu_id][0].split('_')

        if epgp_value[1] == 'EP':
            ep = int(epgp_value[0])
        else:
            gp = int(epgp_value[0])

    if cfg.admin_path_values.get(constant.loot_menu_id) is not None:
        gp = cfg.loot_dict[cfg.admin_path_values[constant.loot_menu_id][0]].GP

    if cfg.admin_path_values.get('percentage') is not None:
        percentage = float(cfg.admin_path_values[constant.percentage_menu_id][0])

    for game_id in game_ids:
        util.set_ep(game_id, util.get_ep(game_id) + ep)
        util.set_gp(game_id, util.get_gp(game_id) + int(gp * percentage))


def decay():
    for raider in cfg.raider_dict.values():
        util.set_ep(raider.ID,
                    int(constant.decay_factor * util.get_ep(raider.ID)))
        util.set_gp(raider.ID,
                    int(constant.decay_factor * util.get_gp(raider.ID)))
