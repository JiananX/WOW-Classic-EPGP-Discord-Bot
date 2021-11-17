from discord_components import ActionRow, Button, ButtonStyle

import constant

admin_cancel_button = [
    Button(label='Cancel',
           custom_id=constant.admin_cancel_id,
           style=ButtonStyle.blue)
]

admin_confirm_button = [
    Button(label='Confirm',
           custom_id=constant.admin_confirm_id,
           style=ButtonStyle.blue)
]

admin_bundle_button = [
    ActionRow(admin_confirm_button[0], admin_cancel_button[0])
]
