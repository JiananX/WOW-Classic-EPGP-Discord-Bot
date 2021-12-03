import cfg
import constant
import history
import util


def adjust_epgp():
    raider_names = []
    ep = 0
    gp = 0
    percentage = 1
    loot = None

    if cfg.admin_path_values.get(constant.raider_menu_id + '1') is not None:
        raider_names = cfg.admin_path_values[constant.raider_menu_id + '1']
    elif cfg.admin_path_values.get(constant.raider_menu_id + '2') is not None:
        raider_names = cfg.admin_path_values[constant.raider_menu_id + '2']
    else:
        for raider in cfg.raider_dict.values():
            if ((raider.in_raid == True) & (raider.standby == False)):
                raider_names.append(raider.name)

    if cfg.admin_path_values.get(constant.epgp_menu_id) is not None:
        epgp_value = cfg.admin_path_values[constant.epgp_menu_id][0].split('_')

        if epgp_value[1] == 'EP':
            ep = int(epgp_value[0])
        else:
            gp = int(epgp_value[0])

    if cfg.admin_path_values.get(constant.loot_menu_id) is not None:
        loot = cfg.loot_dict[cfg.admin_path_values[constant.loot_menu_id][0]]
        gp = loot.gp

    if cfg.admin_path_values.get(constant.percentage_menu_id) is not None:
        percentage = float(
            cfg.admin_path_values[constant.percentage_menu_id][0])

    for raider_name in raider_names:
        util.set_ep(raider_name, util.get_ep(raider_name) + ep)
        util.set_gp(raider_name,
                    util.get_gp(raider_name) + int(gp * percentage))

    history.log_adjustment(raider_names, ep=ep, gp=gp, loot=loot)

    cfg.event_msg = 'Adjust successfully'


def decay():
    for raider in cfg.raider_dict.values():
        util.set_ep(raider.name,
                    int(constant.decay_factor * util.get_ep(raider.name)))
        util.set_gp(raider.name,
                    int(constant.decay_factor * util.get_gp(raider.name)))

    cfg.event_msg = 'Decay successfully'
