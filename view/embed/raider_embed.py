import cfg
import discord
import util


def raider_embed_view():
    embed = discord.Embed(title='欢迎参加老年团活动', color=discord.Color.random())

    all_raiders = {}
    for raider in cfg.raider_dict.values():
        if (raider.in_raid == True):
            all_raiders.update({raider: util.calculate_pr(raider.name)})

    # return List of key-value tuple/pair entry
    sorted_pr_list = sorted(all_raiders.items(),
                            key=lambda x: x[1],
                            reverse=True)

    raiders_on_pr = ''
    for entry in sorted_pr_list:
        raider = entry[0]
        raiders_on_pr += raider.name + ' '

    if (len(raiders_on_pr) != 0):
        embed.add_field(name='__*活动团员名单(根据PR排序)*__',
                        value='>>> %s' % raiders_on_pr)
    else:
        embed.add_field(name='__*活动团员名单(根据PR排序)*__', value='>>> 无团员')

    embed.add_field(name='__*无法找到自己的名字?*__',
                    value='>>> 跟我私信 __**Update 游戏ID**__. 例如 Update Akitainu',
                    inline=False)
    embed.add_field(name='__*想查询团员的具体EPGP信息?*__',
                    value='>>> 跟我私信 __**PR 游戏ID**__. 例如 PR Akitainu',
                    inline=False)

    return embed
