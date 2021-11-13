import cfg
import discord

def loot_embed_view(loot):
    embed = discord.Embed(title='开始分配物品', color=discord.Color.random())

    embed.add_field(name='Loot Name',
                    value='> %s' % (loot.NAME),
                    inline=False)
    embed.add_field(name='GP',
                    value='> %s' % (loot.GP),
                    inline=False)
    embed.add_field(name='BIS',
                    value='> %s' % (loot.BIS),
                    inline=False)

    return embed