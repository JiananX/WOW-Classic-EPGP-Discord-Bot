from discord_components import Button, ActionRow, ButtonStyle

import constant


loot_button = ActionRow(
        Button(label='Main Spec',
               custom_id=constant.loot_main_spec_id,
               style=ButtonStyle.red),
        Button(label='Off Spec',
               custom_id=constant.loot_off_spec_id,
               style=ButtonStyle.red))
