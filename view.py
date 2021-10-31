from discord_components import Button, ActionRow, ButtonStyle

import cfg
import constant
import discord
import user


# raid pr list
def raid_pr_button():
    return Button(label="团队PR列表",
                  custom_id=constant.user_raid_pr_list_id + cfg.stamp,
                  style=ButtonStyle.blue)


def raid_pr_embed():
    embed = discord.Embed(title='团队PR列表',
                          description=user.raid_pr_list(),
                          color=discord.Color.random())
    add_loot_secion(embed)
    return embed


# my pr
def my_pr_button():
    return Button(label="你的PR",
                  custom_id=constant.user_my_pr_id + cfg.stamp,
                  style=ButtonStyle.blue)


def my_pr_embed(author):
    embed = discord.Embed(title='你的PR',
                          description=user.my_pr(author),
                          color=discord.Color.random())

    add_loot_secion(embed)
    return embed


#loot
def main_spec_button(enable_loot_button):
    return Button(label="Main Spec",
                    custom_id=constant.user_main_spec_id + cfg.stamp,
                    style=ButtonStyle.red,
                    disabled=(enable_loot_button == False))


def user_view_component(enable_loot_button):
    return ActionRow(ActionRow(raid_pr_button(), my_pr_button()),
                     ActionRow(main_spec_button(enable_loot_button)))


def gbid_confirm_button(enabled):
    return Button(label="20% reward",
                  custom_id=constant.loot_gbid_confirm_id + cfg.stamp,
                  style=ButtonStyle.blue,
                  disabled=(enabled == False))


def main_spec_confirm_button(enabled):
    return Button(label="100% reward",
                  custom_id=constant.loot_main_spec_confirm_id + cfg.stamp,
                  style=ButtonStyle.blue,
                  disabled=(enabled == False))


def loot_cancel_button(enabled):
    return Button(label="cancel",
                  custom_id=constant.loot_cancel_id + cfg.stamp,
                  style=ButtonStyle.blue,
                  disabled=(enabled == False))


def loot_admin_embed():
    embed = discord.Embed(title='分配', color=discord.Color.random())
    add_loot_secion(embed)

    return embed


def add_loot_secion(embed):
    if (cfg.current_loot == None):
        embed.add_field(name="正在分配物品", value='未知')
    else:
        embed.add_field(name="正在分配物品", value=cfg.current_loot.name)

    if (cfg.current_loot == None):
        embed.add_field(name="GP", value="未知")
    else:
        embed.add_field(name="GP", value="%s" % (cfg.current_loot.gp))

    embed.add_field(name="分配结果", value='%s' % (cfg.loot_message), inline=False)


def loot_admin_view_component(enable_confirm_button, enable_cancel_button):
    return ActionRow(
        ActionRow(gbid_confirm_button(enable_confirm_button),
                  main_spec_confirm_button(enable_confirm_button)),
        ActionRow(loot_cancel_button(enable_cancel_button)))
