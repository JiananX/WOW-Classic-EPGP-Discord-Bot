from discord_components import Button, ActionRow, ButtonStyle

import constant


def loot_button(loot_name):
    return [
        ActionRow(
            Button(label='主天赋',
                   custom_id='%s %s' % (constant.loot_main_spec_id, loot_name),
                   style=ButtonStyle.red),
            Button(label='副天赋',
                   custom_id='%s %s' % (constant.loot_off_spec_id, loot_name),
                   style=ButtonStyle.red),
       #      Button(label='小提升',
       #             custom_id='%s %s' %
       #             (constant.loot_minor_improve_id, loot_name),
       #             style=ButtonStyle.red),
            Button(label='拍金',
                   custom_id='%s %s' % (constant.loot_gbid_id, loot_name),
                   style=ButtonStyle.red)),
    ]
