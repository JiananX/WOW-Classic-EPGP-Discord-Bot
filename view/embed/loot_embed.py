import cfg
import discord
import util
import constant


def loot_embed_view(loot_name):
    loot = cfg.loot_dict[loot_name]
    embed = discord.Embed(title='分配物品', color=discord.Color.random())

    embed.add_field(name='物品名称', value='> %s' % (loot.name), inline=False)
    embed.add_field(name='GP', value='> %s' % (loot.gp), inline=False)

    if (len(loot.bis) != 0):
        bis_str = ''
        for bis in loot.bis:
            bis_str += constant.specs.get(bis) + ' | '
            
        embed.add_field(name='BIS天赋', value='以下天赋只能出分不能出g \n> %s' % (bis_str), inline=False)

    return embed


def loot_result_embed_view(loot_name):
    embed = discord.Embed(title=loot_name, color=discord.Color.random())

    if (len(cfg.main_spec[loot_name]) != 0):
        embed.add_field(name='主天赋',
                        value=_build_loot_result_message(
                            cfg.main_spec[loot_name]),
                        inline=False)

    if (len(cfg.off_spec[loot_name]) != 0):
        embed.add_field(name='副天赋',
                        value=_build_loot_result_message(
                            cfg.off_spec[loot_name]),
                        inline=False)

    # if (len(cfg.minor_improve[loot_name]) != 0):
    #     embed.add_field(name='小提升',
    #                     value=_build_loot_result_message(
    #                         cfg.minor_improve[loot_name]),
    #                     inline=False)

    if (len(cfg.gbid[loot_name]) != 0):
        embed.add_field(name='拍金',
                        value=_build_loot_result_message(cfg.gbid[loot_name]),
                        inline=False)

    return embed


def _build_loot_result_message(raider_user_ids):
    loot_result_message = '>>> '
    for user_id in raider_user_ids:
        raider_name = util.find_raider_name(user_id)
        loot_result_message += '%s (EP: %s, PR: %s)\n' % (
            raider_name, util.get_ep(raider_name),
            util.calculate_pr(raider_name))

    return loot_result_message
