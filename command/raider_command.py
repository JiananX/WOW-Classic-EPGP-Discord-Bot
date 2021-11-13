import cfg
from view.view import update_admin_view, update_raider_view

async def update_user_id(message):
    game_id = message.content.split(" ")[1]

    if (cfg.raider_dict.get(game_id) == None):
        await message.channel.send('Invalid game id')
        return

    cfg.raider_dict[game_id].in_raid = True
    cfg.raider_dict[game_id].author_id = message.author.id

    await update_admin_view()
    await update_raider_view()

    await message.author.send('User id gets updated successfully')