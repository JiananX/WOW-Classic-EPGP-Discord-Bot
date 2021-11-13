import cfg
import constant

def standby():
    game_ids = cfg.admin_path_values[constant.raider_menu_id]

    for raider in cfg.raider_dict.values():
        if raider.ID in game_ids:
            raider.stand_by = True
