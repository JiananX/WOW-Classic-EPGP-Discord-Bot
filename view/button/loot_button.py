from discord_components import Button, ActionRow, ButtonStyle

import constant


def loot_button(loot_name):
    return [
        ActionRow(
            Button(label='Main Spec',
                   custom_id='%s %s' % (constant.loot_main_spec_id, loot_name),
                   style=ButtonStyle.red),
            Button(label='Off Spec',
                   custom_id='%s %s' % (constant.loot_off_spec_id, loot_name),
                   style=ButtonStyle.red))
    ]
