from discord_components import Button, ButtonStyle

import constant


admin_cancel_button = Button(label='Cancel',
                  custom_id=constant.admin_cancel_id,
                  style=ButtonStyle.blue)


admin_confirm_button = Button(label='Confirm',
                  custom_id=constant.admin_confirm_id,
                  style=ButtonStyle.blue)
