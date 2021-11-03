import cfg
import gsheet
import pandas as pd
import json
import raider
import loot


async def sync_epgp_from_gsheet_to_json(message):
    epgp_from_gsheet = gsheet.get_epgp_from_gsheet()
    df = pd.DataFrame.from_dict(epgp_from_gsheet)
    raiders = []
    for index, row in df.iterrows():
        r = raider.Raider(row['ID'], row['EP'], row['GP'], False)
        cfg.raider_dict[row['ID']] = r
        print(r)
        raiders.append(r)
    jstr = json.dumps([ob.__dict__ for ob in raiders])
    with open('epgp.txt', 'w') as outfile:
        outfile.write(jstr)
    await message.author.send('从google sheet中导入epgp.txt成功')


async def sync_loot_from_gsheet_to_json(message):
    loot_from_gsheet = gsheet.get_loot_from_gsheet()
    df = pd.DataFrame.from_dict(loot_from_gsheet)
    loots = []
    for index, row in df.iterrows():
        l = loot.Loot(row['ID'], row['NAME'], row['GP'], row['BIS'])
        cfg.loot_dict[row['ID']] = l
        print(l)
        loots.append(l)
    jstr = json.dumps([ob.__dict__ for ob in loots])
    with open('loot.txt', 'w') as outfile:
        outfile.write(jstr)
    await message.author.send('从google sheet中导入loot.txt成功')


def load_epgp_from_json_to_memory():
    with open('epgp.txt', 'r') as infile:
        json_data = infile.read()
    raiders = json.loads(json_data)
    for index, value in enumerate(raiders):
        r = raider.Raider(raiders[index]['ID'], raiders[index]['EP'],
                          raiders[index]['GP'], raiders[index]['in_raid'],
                          raiders[index]['stand_by'], raiders[index]['author'],
                          raiders[index]['author_id'])
        cfg.raider_dict[raiders[index]['ID']] = r


def load_loot_from_json_to_memory():
    with open('loot.txt', 'r') as infile:
        json_data = infile.read()
    loots = json.loads(json_data)
    for index, value in enumerate(loots):
        l = loot.Loot(loots[index]['ID'], loots[index]['NAME'],
                      loots[index]['GP'], loots[index]['BIS'])
        cfg.loot_dict[loots[index]['ID']] = l


async def dump_epgp_from_memory_to_json(message):
    raiders = []
    for value in cfg.raider_dict.values():
        raiders.append(value)
    jstr = json.dumps([{
        'ID': ob.ID,
        'EP': ob.EP,
        'GP': ob.GP,
        'PR': round(ob.EP/ob.GP, 3),
        'in_raid': ob.in_raid,
        'stand_by': ob.stand_by,
        'author': str(ob.author),
        'author_id': ob.author_id
    } for ob in raiders])
    with open('epgp.txt', 'w') as outfile:
        outfile.write(jstr)

    await message.channel.send('EPGP write back to json successfully')


def dump_loot_from_memory_to_json():
    loots = []
    for value in cfg.loot_dict.values():
        loots.append(value)
    jstr = json.dumps([ob.__dict__ for ob in loots])
    with open('loot.txt', 'w') as outfile:
        outfile.write(jstr)
