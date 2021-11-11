from discord_components import Button, ActionRow, ButtonStyle

import cfg
import constant
import discord
import util
''' Button '''


def main_spec_confirm_button(enabled):
    return Button(label="100% Main Spec GP",
                  custom_id=constant.loot_main_spec_confirm_id + cfg.stamp,
                  style=ButtonStyle.blue,
                  disabled=(enabled == False))


def off_spec_confirm_button(enabled):
    return Button(label="50% Off Spec GP",
                  custom_id=constant.loot_off_spec_confirm_id + cfg.stamp,
                  style=ButtonStyle.blue,
                  disabled=(enabled == False))


def loot_cancel_button(enabled):
    return Button(label="cancel",
                  custom_id=constant.loot_cancel_id + cfg.stamp,
                  style=ButtonStyle.blue,
                  disabled=(enabled == False))


''' Embed '''


def loot_view_embed(count_down):
    embed = discord.Embed(title='开始分配物品', color=discord.Color.random())

    embed.add_field(name='Loot Name',
                    value='> %s' % (cfg.current_loot.NAME),
                    inline=False)
    embed.add_field(name='GP',
                    value='> %s' % (cfg.current_loot.GP),
                    inline=False)
    embed.add_field(name='BIS',
                    value='> %s' % (cfg.current_loot.BIS),
                    inline=False)

    embed.add_field(name='Countdown', value='> %ss'%(count_down), inline=False)
    return embed


def admin_embed_view():
    embed = discord.Embed(title='Admin Panel', color=discord.Color.random())

    total_raider = 0
    standby_raider = []
    for raider in cfg.raider_dict.values():
        if (raider.in_raid == True):
            total_raider += 1
        if (raider.stand_by == True):
            standby_raider.append(raider.ID)

    embed.add_field(name='Total Count',
                    value='> %s' % (total_raider),
                    inline=False)
    embed.add_field(name='Standby',
                    value='>>> %s' % ('\n'.join(standby_raider)),
                    inline=False)

    if (cfg.current_loot is not None):
        embed.add_field(name='Current Loot',
                        value='> %s' % (str(cfg.current_loot.NAME)),
                        inline=False)
        embed.add_field(name='Current Loot Winner',
                        value='> %s' % (cfg.current_winner),
                        inline=False)

    return embed


def raider_view_embed():
    embed = discord.Embed(title='Raider Panel', color=discord.Color.random())

    all_raiders = {}
    for raider in cfg.raider_dict.values():
        if (raider.in_raid == True):
            all_raiders.update({raider: util.calculate_pr(raider.ID)})

    # return List of key-value tuple/pair entry
    sorted_pr_list = sorted(all_raiders.items(),
                            key=lambda x: x[1],
                            reverse=True)

    pr_message = ''
    for entry in sorted_pr_list:
        raider = entry[0]
        pr_message += '%s (EP:%s GP:%s, PR:%s)\n' % (raider.ID, raider.EP,
                                                     raider.GP, entry[1])

    embed.add_field(name="PR列表", value='>>> %s' % (pr_message))

    return embed


''' View component '''


def loot_view_component():
    return ActionRow(
        ActionRow(
            Button(label="Main Spec",
                   custom_id=constant.loot_main_spec_id + cfg.stamp,
                   style=ButtonStyle.red),
            Button(label="Off Spec",
                   custom_id=constant.loot_off_spec_id + cfg.stamp,
                   style=ButtonStyle.red)))


def admin_view_component(enable_confirm_button=False,
                         enable_cancel_button=False):
    return ActionRow(
        ActionRow(
            Button(label="Reward 20EP",
                   custom_id=constant.reward_20_ep + cfg.stamp,
                   style=ButtonStyle.red),
            Button(label="Reward 150EP",
                   custom_id=constant.reward_150_ep + cfg.stamp,
                   style=ButtonStyle.red),
            Button(label="Reward 200EP",
                   custom_id=constant.reward_200_ep + cfg.stamp,
                   style=ButtonStyle.red)),
        ActionRow(main_spec_confirm_button(enable_confirm_button),
                  off_spec_confirm_button(enable_confirm_button),
                  loot_cancel_button(enable_cancel_button)))


'''
Util
'''


async def update_admin_view(target_source=None,
                            enable_confirm_button=False,
                            enable_cancel_button=False):
    if (cfg.admin_msg is None):
        cfg.admin_msg = await target_source.send(
            embed=admin_embed_view(),
            components=admin_view_component(enable_confirm_button,
                                            enable_cancel_button))
    else:
        await cfg.admin_msg.edit(embed=admin_embed_view(),
                                 components=admin_view_component(
                                     enable_confirm_button,
                                     enable_cancel_button))


async def update_raider_view(target_source=None):
    if (cfg.raider_msg is None):
        cfg.raider_msg = await target_source.send(embed=raider_view_embed())
    else:
        await cfg.raider_msg.edit(embed=raider_view_embed())
