from menu_callback.epgp_callback import adjust_epgp, decay
from menu_callback.loot_callback import loot_announcement
from menu_callback.raider_callback import standby
from menu_callback.system_callback import on_system_operation_callback

# The order of this callback list must be the same as [all_paths] in menu.menu
all_paths_callback = [
    adjust_epgp,
    adjust_epgp,
    adjust_epgp,
    decay,
    loot_announcement,
    standby,
    on_system_operation_callback
]