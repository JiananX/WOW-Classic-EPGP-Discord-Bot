from discord_components import Button, ActionRow, ButtonStyle

import cfg
import constant
import discord
import user
''' Button '''


def raid_pr_button():
    return Button(label="团队PR列表",
                  custom_id=constant.user_raid_pr_list_id + cfg.stamp,
                  style=ButtonStyle.blue)


def my_pr_button():
    return Button(label="你的PR",
                  custom_id=constant.user_my_pr_id + cfg.stamp,
                  style=ButtonStyle.blue)


def main_spec_button(enable_loot_button):
    return Button(label="Main Spec",
                  custom_id=constant.user_main_spec_id + cfg.stamp,
                  style=ButtonStyle.red,
                  disabled=(enable_loot_button == False))


def off_spec_button(enable_loot_button):
    return Button(label="Off Spec",
                  custom_id=constant.user_off_spec_id + cfg.stamp,
                  style=ButtonStyle.red,
                  disabled=(enable_loot_button == False))


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


def my_pr_embed(author):
    embed = discord.Embed(title='你的PR',
                          description=user.my_pr(author),
                          color=discord.Color.random())

    add_loot_secion(embed)
    return embed


def raid_pr_embed():
    embed = discord.Embed(title='团队PR列表',
                          description=user.raid_pr_list(),
                          color=discord.Color.random())
    add_loot_secion(embed)
    return embed


def loot_admin_embed():
    embed = discord.Embed(title='Raid管理员功能', color=discord.Color.random())

    roster_string = '编号  游戏ID StandBy\n'
    counter = 1
    for raider in cfg.raider_dict.values():
        if (raider.in_raid == True):
            roster_string += '%s  %s  %s\n' % (counter, raider.ID,
                                               raider.stand_by == True)
            counter += 1

    embed.add_field(name="Raid 名单", value=roster_string, inline=False)

    add_loot_secion(embed)

    return embed


''' View component '''


def user_view_component(enable_loot_button):
    return ActionRow(
        ActionRow(raid_pr_button(), my_pr_button()),
        ActionRow(main_spec_button(enable_loot_button),
                  off_spec_button(enable_loot_button)))


def loot_admin_view_component(enable_confirm_button, enable_cancel_button):
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


''' Util '''


def add_loot_secion(embed):
    if (cfg.current_loot == None):
        embed.add_field(name="正在分配物品", value='未知', inline=False)
    else:
        embed.add_field(name="正在分配物品",
                        value='> %s' % (cfg.current_loot.NAME),
                        inline=False)

    if (cfg.current_loot == None):
        embed.add_field(name="GP", value="未知", inline=False)
    else:
        embed.add_field(name="GP",
                        value="%s" % (cfg.current_loot.GP),
                        inline=False)

    if (cfg.current_loot != None):
        # In case there is no bis indication
        if (len(cfg.current_loot.BIS) != 0):
            embed.add_field(name="BIS:",
                            value='%s' % (cfg.current_loot.BIS),
                            inline=False)
        embed.add_field(name="分配结果",
                        value='%s' % (cfg.loot_message),
                        inline=False)
