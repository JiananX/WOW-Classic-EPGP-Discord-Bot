import constant


reward_adjust_path = [
    constant.adjust_operation_path, constant.reward_adjust_path,
    constant.epgp_path
]
manual_adjust_path = [
    constant.adjust_operation_path, constant.manual_adjust_path,
    constant.raider_path, constant.epgp_path
]
loot_adjust_path = [
    constant.adjust_operation_path, constant.loot_adjust_path,
    constant.boss_id_path, constant.loot_id_path, constant.raider_path,
    constant.percentage_path
]
decay_adjust_path = [
  constant.adjust_operation_path, constant.decay_adjust_path,
]

loot_announce_path = [
    constant.loot_operation_path, constant.boss_id_path, constant.loot_id_path
]

standby_raider_path = [constant.raider_operation_path, constant.standby_raider_path, constant.raider_path]

system_path = [constant.system_operation_path, constant.system_path]

# The order of this menu list must be the same as [all_paths_callback] in menu_callback.menu_callback
all_paths = [
    reward_adjust_path,
    manual_adjust_path,
    loot_adjust_path,
    decay_adjust_path,
    loot_announce_path,
    standby_raider_path,
    system_path
]
