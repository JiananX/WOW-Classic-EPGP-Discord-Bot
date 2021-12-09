import cfg
import discord
import util


def loot_embed_view(loot_name):
    loot = cfg.loot_dict[loot_name]
    embed = discord.Embed(title='Distributing', color=discord.Color.random())
    embed.set_thumbnail(
        url='http://img.yao51.com/jiankangtuku/boiiejodiz.jpeg')

    embed.add_field(name='Name', value='> %s' % (loot.name), inline=False)
    embed.add_field(name='GP', value='> %s' % (loot.gp), inline=False)

    if (len(loot.bis) != 0):
        embed.add_field(name='BIS', value='> %s' % (loot.bis), inline=False)

    return embed


def loot_result_embed_view(loot_name):
    embed = discord.Embed(title=loot_name, color=discord.Color.random())
    embed.set_thumbnail(
        url='http://img.yao51.com/jiankangtuku/boiiejodiz.jpeg')


    if (len(cfg.main_spec[loot_name]) != 0):
        embed.add_field(name='Main Spec',
                        value=_build_loot_result_message(cfg.main_spec[loot_name]),
                        inline=False)

    if (len(cfg.off_spec[loot_name]) != 0):
        embed.add_field(name='Off Spec',
                        value=_build_loot_result_message(cfg.off_spec[loot_name]),
                        inline=False)

    return embed


def _build_loot_result_message(raider_user_ids):
    loot_result_message = '>>> '
    for user_id in raider_user_ids:
        raider_name = util.find_raider_name(user_id)
        if raider_name is not None:
            loot_result_message += '%s (EP: %s, PR: %s)\n' % (
                raider_name, util.get_ep(raider_name),
                util.calculate_pr(raider_name))
        else:
            print('\nCan\'t find WOW account with Discord user id ', user_id)

    return loot_result_message
