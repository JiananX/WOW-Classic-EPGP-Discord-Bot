import cfg
from view.view import update_admin_view, update_raider_view


async def update_user_id(message):
    raider_name = message.content.split(" ")[1]

    if (cfg.raider_dict.get(raider_name) == None):
        await message.channel.send('Invalid raider name')
        return

    cfg.raider_dict[raider_name].in_raid = True
    cfg.raider_dict[raider_name].author_id = message.author.id

    await update_admin_view()
    await update_raider_view()

    await message.author.send('User id gets updated successfully')
