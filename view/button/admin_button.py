from discord_components import ActionRow, Button, ButtonStyle

import constant

admin_cancel_button = [
    Button(label='返回主菜单',
           custom_id=constant.admin_cancel_id,
           style=ButtonStyle.blue)
]

admin_reward_buttons = [
    ActionRow(
        Button(label='20GP',
               custom_id=constant.admin_reward_20_id,
               style=ButtonStyle.red),
        Button(label='150GP',
               custom_id=constant.admin_reward_150_id,
               style=ButtonStyle.red),
        Button(label='200GP',
               custom_id=constant.admin_reward_200_id,
               style=ButtonStyle.red),
        Button(label='250GP',
               custom_id=constant.admin_reward_250_id,
               style=ButtonStyle.red))
]
