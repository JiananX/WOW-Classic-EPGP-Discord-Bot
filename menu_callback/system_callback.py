from infra.source import sync_epgp_from_gsheet_to_json, sync_loot_from_gsheet_to_json, load_loot_from_json_to_memory, load_epgp_from_json_to_memory, dump_epgp_from_memory_to_json, dump_loot_from_memory_to_json

import constant
import cfg


def on_system_operation_callback():
    system_operation = cfg.admin_path_values[constant.system_menu_id][0]

    if (system_operation == 'sync_epgp_from_gsheet_to_json'):
        sync_epgp_from_gsheet_to_json()
    elif (system_operation == 'sync_loot_from_gsheet_to_json'):
        sync_loot_from_gsheet_to_json()
    elif (system_operation == 'load_loot_from_json_to_memory'):
        load_loot_from_json_to_memory()
    elif (system_operation == 'load_epgp_from_json_to_memory'):
        load_epgp_from_json_to_memory()
    elif (system_operation == 'dump_epgp_from_memory_to_json'):
        dump_epgp_from_memory_to_json()
    elif (system_operation == 'dump_loot_from_memory_to_json'):
        dump_loot_from_memory_to_json()
    
    cfg.event_msg = 'System operation is finished successfully'
