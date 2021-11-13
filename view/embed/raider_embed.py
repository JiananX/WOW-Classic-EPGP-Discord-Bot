import cfg
import discord
import util


def raider_embed_view():
    embed = discord.Embed(title='Raider Panel', color=discord.Color.random())

    all_raiders = {}
    for raider in cfg.raider_dict.values():
        if (raider.in_raid == True):
            all_raiders.update({raider: util.calculate_pr(raider.ID)})

    # return List of key-value tuple/pair entry
    sorted_pr_list = sorted(all_raiders.items(),
                            key=lambda x: x[1],
                            reverse=True)

    for entry in sorted_pr_list:
        raider = entry[0]
        embed.add_field(name=raider.ID,
                        value='> EP:%s GP:%s, PR:%s' %
                        (raider.EP, raider.GP, entry[1]))

    return embed
