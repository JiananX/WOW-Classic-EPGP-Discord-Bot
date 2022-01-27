from view.view import send_loot_message, send_loot_result_message

import asyncio
import cfg
import constant


async def loot_announcement(loot_names):
    if (cfg.is_distributing):
        return

    cfg.main_spec = {}
    cfg.off_spec = {}
    cfg.minor_improve = {}
    cfg.gbid = {}

    for loot_name in loot_names:
        cfg.main_spec.update({loot_name: []})
        cfg.off_spec.update({loot_name: []})
        cfg.minor_improve.update({loot_name: []})
        cfg.gbid.update({loot_name: []})

    await send_loot_message(loot_names)

    await asyncio.sleep(constant.loot_announcement_duration)

    await send_loot_result_message(loot_names)
