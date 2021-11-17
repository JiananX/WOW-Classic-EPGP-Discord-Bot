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


def raider_menu():
    raiders = []
    if (cfg.admin_path_values.get(
            constant.adjust_menu_id) == ['manual_adjust_ep_gp']):
        for raider in cfg.raider_dict.values():
            raiders.append(raider)
    else:
        for raider in cfg.raider_dict.values():
            if (raider.in_raid == True and raider.standby == False):
                raiders.append(raider)

    raiders = sorted(raiders, key=lambda x: x.name)
    if (len(raiders) == 0):
        return []

    options = []
    for raider in raiders:
        options.append(
            SelectOption(label='%s' % (raider.name),
                         value=util.build_admin_path(constant.raider_path,
                                                     raider.name)))

    if (len(raiders) <= 25):
        return [
            Select(placeholder='All Raider',
                   custom_id=constant.raider_menu_id + '1',
                   options=options,
                   max_values=len(raiders)),
        ]
    else:
        splice_index = 0

        for raider in raiders:
            if raider.name.startswith('N'):
                break
            else:
                splice_index += 1

        return [
            Select(placeholder='A - M',
                   custom_id=constant.raider_menu_id + '1',
                   options=options[:splice_index],
                   max_values=len(options[:splice_index])),
            Select(placeholder='N - Z',
                   custom_id=constant.raider_menu_id + '2',
                   options=options[splice_index:],
                   max_values=len(options[splice_index:]))
        ]
