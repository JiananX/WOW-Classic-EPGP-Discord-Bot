import cfg
import constant
import util

from raider import Raider

from view.view import update_raider_view


async def update_user_id(message):
    raider_name = message.content.split(" ")[1]
    new_user_id = message.author.id

    if (cfg.raider_dict.get(raider_name) == None):
        cfg.raider_dict.update({
            raider_name:
            Raider(raider_name, constant.initial_ep, constant.initial_gp, [],
                   99)
        })
        await message.channel.send('请联系管理员设置职业天赋',
                                   delete_after=constant.delte_after)

    for name, raider in cfg.raider_dict.items():
        if new_user_id in raider.user_id:
            await message.channel.send('本DC已经绑定给%s, 请联系管理员' % (name),
                                       delete_after=constant.delte_after)
            return

    cfg.raider_dict[raider_name].in_raid = True
    cfg.raider_dict[raider_name].user_id.append(message.author.id)

    await update_raider_view()

    await message.author.send('DC绑定成功', delete_after=constant.delte_after)


async def check_pr(message):
    raider_name = message.content.split(" ")[1]

    if (cfg.raider_dict.get(raider_name) == None):
        await message.channel.send('无法找到%s' % (raider_name),
                                   delete_after=constant.delte_after)
        return

    raider = cfg.raider_dict.get(raider_name)
    await message.author.send(
        ('%s EP: %s GP: %s PR: %s') %
        (raider.name, raider.ep, raider.gp, util.calculate_pr(raider.name)),
        delete_after=constant.delte_after)


async def reset_spec(message):
    spec = message.content.split(" ")[1]

    if (spec not in constant.specs.keys() | spec == 99):
        await message.channel.send('无法找到天赋%s, 请联系管理员' % (spec),
                                   delete_after=constant.delte_after)
        return

    raider_name = util.find_raider_name(message.author.id)

    if (raider_name == None):
        await message.channel.send('无法找到关联的游戏名称%s, 请联系管理员' % (spec),
                                   delete_after=constant.delte_after)
        return

    cfg.raider_dict[raider_name].spec = int(spec)

    await message.channel.send('重置天赋为%s' % (constant.specs[spec]),
                               delete_after=constant.delte_after)
