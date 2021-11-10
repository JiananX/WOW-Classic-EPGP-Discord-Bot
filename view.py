from discord_components import Button, ActionRow, ButtonStyle

import cfg
import constant
import discord
import user
import util
''' Button '''


def raid_pr_button():
    return Button(label="团队PR列表",
                  custom_id=constant.user_raid_pr_list_id + cfg.stamp,
                  style=ButtonStyle.blue)


def my_pr_button():
    return Button(label="你的PR",
                  custom_id=constant.user_my_pr_id + cfg.stamp,
                  style=ButtonStyle.blue)


def main_spec_button(enable):
    return Button(label="Main Spec",
                  custom_id=constant.user_main_spec_id + cfg.stamp,
                  style=ButtonStyle.red,
                  disabled=(enable == False))


def off_spec_button(enable):
    return Button(label="Off Spec",
                  custom_id=constant.user_off_spec_id + cfg.stamp,
                  style=ButtonStyle.red,
                  disabled=(enable == False))


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


def loot_view_embed():
    embed = discord.Embed(title='开始分配物品', color=discord.Color.random())
    add_raid_pr_section(embed)


def my_pr_embed(author):
    embed = discord.Embed(title='你的PR',
                          description=user.my_pr(author),
                          color=discord.Color.random())
    return embed


def raid_pr_embed():
    embed = discord.Embed(title='团队PR列表',
                          description=user.raid_pr_list(),
                          color=discord.Color.random())
    return embed


def admin_embed():
    embed = discord.Embed(title='Admin Panel', color=discord.Color.random())

    total_raider = 0
    standby_raider = []
    for raider in cfg.raider_dict.values():
        if (raider.in_raid == True):
            total_raider += 1
        if (raider.stand_by == True):
            standby_raider.append(raider.NAME)

    embed.add_field(name='Total Count',
                    value='> %s' % (total_raider),
                    inline=False)
    embed.add_field(name='Standby',
                    value='> %s' % (standby_raider),
                    inline=False)

    embed.add_field(name='Current Loot',
                    value='> %s' % (str(cfg.current_loot)),
                    inline=False)
    embed.add_field(name='Current Loot Winner',
                    value='> %s' % (cfg.current_winner),
                    inline=False)

    return embed


''' View component '''


def loot_view_component(enable_button=True):
    return ActionRow(
        ActionRow(main_spec_button(enable_button),
                  off_spec_button(enable_button)))


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


''' Util '''


def add_raid_pr_section(embed):
    pr_list = {}
    ep_list = {}
    gp_list = {}

    for game_id, raider in cfg.raider_dict.items():
        if (raider.in_raid == True):
            ep_list.update({game_id: raider.EP})
            gp_list.update({game_id: raider.GP})
            pr_list.update({game_id: util.calculate_pr(raider.ID)})

    # return List of key-value tuple/pair entry
    sorted_pr_list = sorted(pr_list.items(), key=lambda x: x[1], reverse=True)

    game_ids = ''
    eps = ''
    gps = ''
    prs = ''
    for entry in sorted_pr_list:
        game_id = entry[0]
        game_ids += game_id + '\n'
        eps += '%s\n' % (ep_list[game_id])
        gps += '%s\n' % (gp_list[game_id])
        prs += '%s\n' % (entry[1])

    embed.add_field(name="游戏ID", value='>>> %s' % (game_ids))
    embed.add_field(name="EP", value='>>> %s' % (eps))
    embed.add_field(name="GP", value='>>> %s' % (gps))
    embed.add_field(name="PR", value='>>> %s' % (prs))
