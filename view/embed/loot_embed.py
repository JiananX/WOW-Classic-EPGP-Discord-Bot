import cfg
import discord
import util


def loot_embed_view(loot):
    embed = discord.Embed(title='Distributing', color=discord.Color.random())
    embed.set_thumbnail(
        url='http://img.yao51.com/jiankangtuku/boiiejodiz.jpeg')

    embed.add_field(name='Name', value='> %s' % (loot.name), inline=False)
    embed.add_field(name='GP', value='> %s' % (loot.gp), inline=False)

    if (len(loot.bis) != 0):
        embed.add_field(name='BIS', value='> %s' % (loot.bis), inline=False)

    return embed


def loot_result_embed_view(loot, winner_user_id):
    embed = discord.Embed(title=loot.name, color=discord.Color.random())
    embed.set_thumbnail(
        url='http://img.yao51.com/jiankangtuku/boiiejodiz.jpeg')

    if (winner_user_id == None):
        embed.add_field(name='Winner', value='Nobody', inline=False)
    else:
        embed.add_field(name='Winner',
                        value=util.find_raider_name(winner_user_id),
                        inline=False)

        if (len(cfg.main_spec) != 0):
            embed.add_field(name='Main Spec',
                            value=_build_loot_result_message(cfg.main_spec),
                            inline=False)

        if (len(cfg.off_spec) != 0):
            embed.add_field(name='Off Spec',
                            value=_build_loot_result_message(cfg.off_spec),
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
