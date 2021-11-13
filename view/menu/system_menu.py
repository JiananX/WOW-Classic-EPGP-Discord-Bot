from discord_components import Select, SelectOption

import constant
import util

sync_epgp_from_gsheet_to_json = SelectOption(
    label='EPGP gsheet => json',
    value=util.build_admin_path(constant.system_path,
                                'sync_epgp_from_gsheet_to_json'))
sync_loot_from_gsheet_to_json = SelectOption(
    label='Loot gsheet => json',
    value=util.build_admin_path(constant.system_path,
                                'sync_loot_from_gsheet_to_json'))
load_epgp_from_json_to_memory = SelectOption(
    label='EPGP json => memory',
    value=util.build_admin_path(constant.system_path,
                                'load_epgp_from_json_to_memory'))
load_loot_from_json_to_memory = SelectOption(
    label='Loot json => memory',
    value=util.build_admin_path(constant.system_path,
                                'load_loot_from_json_to_memory'))
dump_epgp_from_memory_to_json = SelectOption(
    label='**EPGP memory => json',
    value=util.build_admin_path(constant.system_path,
                                'dump_epgp_from_memory_to_json'))
dump_loot_from_memory_to_json = SelectOption(
    label='Loot memory => json',
    value=util.build_admin_path(constant.system_path,
                                'dump_loot_from_memory_to_json'))

system_menu = Select(
    custom_id=constant.system_menu_id,
    options=[
        sync_epgp_from_gsheet_to_json, sync_loot_from_gsheet_to_json,
        load_epgp_from_json_to_memory, load_loot_from_json_to_memory,
        dump_epgp_from_memory_to_json, dump_loot_from_memory_to_json
    ])
