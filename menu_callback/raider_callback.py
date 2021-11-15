import cfg
import constant


def standby():
    game_ids = []
    if cfg.admin_path_values.get(constant.raider_menu_id + '1') is not None:
        game_ids = cfg.admin_path_values[constant.raider_menu_id + '1']
    elif cfg.admin_path_values.get(constant.raider_menu_id + '2') is not None:
        game_ids = cfg.admin_path_values[constant.raider_menu_id + '2']

    for raider in cfg.raider_dict.values():
        if raider.ID in game_ids:
            raider.stand_by = True
