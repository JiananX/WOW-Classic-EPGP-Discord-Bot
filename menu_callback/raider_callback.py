import cfg
import constant


def standby():
    raider_names = []
    if cfg.admin_path_values.get(constant.raider_menu_id + '1') is not None:
        raider_names = cfg.admin_path_values[constant.raider_menu_id + '1']
    elif cfg.admin_path_values.get(constant.raider_menu_id + '2') is not None:
        raider_names = cfg.admin_path_values[constant.raider_menu_id + '2']

    for raider in cfg.raider_dict.values():
        if raider.name in raider_names:
            raider.standby = True
    
    cfg.event_msg = 'Standby successfully'
