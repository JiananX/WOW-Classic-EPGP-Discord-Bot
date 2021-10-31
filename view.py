from discord_components import Button, ActionRow, ButtonStyle

import cfg
import constant
import discord
import user

# raid pr list
raid_pr_button = Button(label="团队PR列表",
                        custom_id=constant.raid_pr_list_id,
                        style=ButtonStyle.blue)


def raid_pr_embed():
    return discord.Embed(title='团队PR列表',
                         description=user.raid_pr_list(),
                         color=discord.Color.random())


# my pr
my_pr_button = Button(label="你的PR",
                      custom_id=constant.my_pr_id,
                      style=ButtonStyle.blue)


def my_pr_embed(author):
    embed = discord.Embed(title='你的PR',
                          description=user.my_pr(author),
                          color=discord.Color.random())

    embed.add_field(name="正在分配物品", value="hahah")
    embed.add_field(name="GP", value="100")
    embed.add_field(name="分配结果", value="hahah", inline=False)
    return embed


#loot
def main_spec_button():
    return Button(label="Main Spec",
                  custom_id=constant.main_spec_id,
                  style=ButtonStyle.red)


def user_view_component():
    return ActionRow(ActionRow(raid_pr_button, my_pr_button),
                     ActionRow(main_spec_button()))
