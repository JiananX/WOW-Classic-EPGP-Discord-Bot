import asyncio
import cfg
import view
import util
'''
Command
'''


async def announcement(message):
    if (cfg.main_spec != None or cfg.off_spec != None):
        await cfg.admin.send(
            'This is another loot in session, please cancel first')
        return

    loot_id = message.content.split(" ")[1]

    if (cfg.loot_dict.get(loot_id) == None):
        await cfg.admin.send('Cannot find this loot')
        return

    cfg.current_loot = cfg.loot_dict[loot_id]
    cfg.main_spec = []
    cfg.off_spec = []

    distribute_msg = await cfg.loot_channel.send(embed=view.loot_view_embed(25),
                                components=view.loot_view_component())

    util.log_msg('开始分配[%s]' % (cfg.current_loot.NAME))
    await asyncio.sleep(10)

    await distribute_msg.edit(embed=view.loot_view_embed(15),
                                components=view.loot_view_component())
    
    await asyncio.sleep(10)

    await distribute_msg.edit(embed=view.loot_view_embed(5),
                                components=view.loot_view_component())

    await asyncio.sleep(5)
    await distribute_msg.edit(embed=view.loot_view_embed(0),
                            components=view.loot_view_component())                          
    await _calculate_result()


'''
Message Interaction
'''


async def cancel():
    util.log_msg('[%s]分配取消' % (cfg.current_loot.NAME))
    await _reset()


async def confirm(factor):
    game_id = util.find_game_id(cfg.current_winner)
    before_gp = util.get_gp(game_id)
    loot_gp = int(cfg.current_loot.GP * factor)
    gp = loot_gp + before_gp
    util.set_gp(game_id, gp)
    util.log_msg(
        '[%s]按照%s%%GP(%s)分配给%s, 分配前GP: %s, 分配后GP: %s' %
        (cfg.current_loot.NAME, factor * 100, loot_gp, game_id, before_gp, gp))
    await _reset()


'''
Util
'''


async def _calculate_result():
    highest_pr = 0
    min_ep = 0
    winner = None

    factor = 0;
    all_bis_class = []
    if len(cfg.current_loot.BIS) != 0:
      for bis in cfg.current_loot.BIS.split(' '):
        all_bis_class.append(bis[len(bis) - 2])
    
    all_bis_class = set(all_bis_class)

    if (len(all_bis_class) == 1):
      factor = 0.5
    elif (len(all_bis_class) > 1):
      factor = 0.8
      
    if (len(cfg.main_spec) == 0):
        for user_id in cfg.off_spec:
            pr = util.calculate_pr(util.find_game_id(user_id))
            if (pr > highest_pr):
                highest_pr = pr
                winner = user_id
    else:
        for user_id in cfg.main_spec:
            ep = util.get_ep(util.find_game_id(user_id))
   
            if (ep * factor > min_ep):
                min_ep = ep * factor
        
        for user_id in cfg.main_spec:
            pr = util.calculate_pr(util.find_game_id(user_id))
            if (pr > highest_pr and util.get_ep(util.find_game_id(user_id)) >= min_ep):
                highest_pr = pr
                winner = user_id

    if (winner != None):
        cfg.current_winner = winner

        loot_result_message = 'Winner: __***%s***__\n\n' % (
            util.find_game_id(winner))

        for user_id in cfg.main_spec:
            loot_result_message += '**Main Spec**\n'
            game_id = util.find_game_id(user_id)
            loot_result_message += '%s (EP: %s, PR: %s)\n' % (
                game_id, util.get_ep(game_id), util.calculate_pr(game_id))

        for user_id in cfg.off_spec:
            loot_result_message += '**Off Spec**\n'
            game_id = util.find_game_id(user_id)
            loot_result_message += '%s (EP: %s, PR: %s)\n' % (
                game_id, util.get_ep(game_id), util.calculate_pr(game_id))

        await cfg.loot_channel.send(loot_result_message)

        await view.update_admin_view(enable_confirm_button=True,
                                     enable_cancel_button=True)
    else:
        await cfg.loot_channel.send('Nobody want this loot :(')

        await view.update_admin_view(enable_cancel_button=True)


async def _reset():
    cfg.main_spec = None
    cfg.off_spec = None
    cfg.current_loot = None
    cfg.current_winner = None

    # Clear the last two messages in the channel
    async for message in cfg.loot_channel.history(limit=2):
        await message.delete()

    await view.update_admin_view()
    await view.update_raider_view()
