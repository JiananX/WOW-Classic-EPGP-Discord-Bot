from discord_components import Select, SelectOption

import cfg
import constant
import util

standby_raider_operation = SelectOption(label='Standby',
                                        value=util.build_admin_path(
                                            constant.standby_raider_path,
                                            'make_raider_standby'))

raider_operation_menu = [
    Select(custom_id=constant.raider_operation_menu_id,
           options=[standby_raider_operation])
]


# TODO: Need to support more than 25 raiders, or 0 raiders
def raider_menu():
    # based on different config build different raider list
    raiders = []
    for raider in cfg.raider_dict.values():
        if ((raider.in_raid == True) & (raider.stand_by == False)):
            raiders.append(raider)

    options = []

    for raider in raiders:
        options.append(
            SelectOption(label='%s' % (raider.ID),
                         value=util.build_admin_path(constant.raider_path,
                                                     raider.ID)))

    return [
        Select(custom_id=constant.raider_menu_id + '1', options=options),
        Select(custom_id=constant.raider_menu_id + '2', options=options)
    ]
