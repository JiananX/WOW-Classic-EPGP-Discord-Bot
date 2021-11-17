import cfg
import discord


def admin_embed_view():
    embed = discord.Embed(title='Admin Panel', color=discord.Color.red())

    total_raider = 0
    standby_raider = ''
    for raider in cfg.raider_dict.values():
        if (raider.in_raid == True):
            total_raider += 1
        if (raider.standby == True):
            standby_raider += '%s\n' % (raider.name)

    if (len(standby_raider) == 0):
        standby_raider = 'Nobody'

    embed.add_field(name='Total Count',
                    value='> %s' % (total_raider),
                    inline=False)

    embed.add_field(name='Standby',
                    value='>>> %s' % (standby_raider),
                    inline=False)

    operation_event = ''
    for menu_id, values in cfg.admin_path_values.items():
        operation_event += '%s:  %s\n' % (menu_id, values)

    if (len(operation_event) == 0):
        operation_event = 'No events'
    embed.add_field(name='Operation events',
                    value='>>> %s' % (operation_event),
                    inline=False)

    embed.add_field(name='Event Message',
                    value='>>> %s' % (cfg.event_msg),
                    inline=False)

    return embed
