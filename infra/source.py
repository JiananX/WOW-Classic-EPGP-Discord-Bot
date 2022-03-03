from infra.gsheet import get_epgp_from_gsheet, get_loot_from_gsheet

import cfg
#import deprecation
import pandas as pd
import json
import raider
import loot


def load_epgp_from_json_to_memory():
    with open('epgp.json', 'r') as infile:
        json_data = infile.read()
    raiders = json.loads(json_data)
    for index, value in enumerate(raiders):
        r = raider.Raider(raiders[index]['name'], raiders[index]['ep'],
                          raiders[index]['gp'], raiders[index]['user_id'],
                          raiders[index]['spec'])
        cfg.raider_dict[raiders[index]['name']] = r


def load_loot_from_json_to_memory():
    with open('loot.json', 'r') as infile:
        json_data = infile.read()
    loots = json.loads(json_data)
    for index, value in enumerate(loots):
        l = loot.Loot(loots[index]['name'], loots[index]['gp'],
                      loots[index]['bis'], loots[index]['boss'])
        cfg.loot_dict[loots[index]['name']] = l


def dump_epgp_from_memory_to_json():
    raiders = []
    for value in cfg.raider_dict.values():
        raiders.append(value)
    jstr = json.dumps([{
        'name': ob.name,
        'ep': ob.ep,
        'gp': ob.gp,
        'pr': round(ob.ep / ob.gp, 3),
        'user_id': ob.user_id,
        'spec': ob.spec
    } for ob in raiders],
                      indent=4)
    with open('epgp1.json', 'w') as outfile:
        outfile.write(jstr)


#@deprecation.deprecated()
def sync_epgp_from_gsheet_to_json():
    epgp_from_gsheet = get_epgp_from_gsheet()
    df = pd.DataFrame.from_dict(epgp_from_gsheet)
    raiders = []
    for index, row in df.iterrows():
        r = raider.Raider(row['ID'], row['EP'], row['GP'], False)
        cfg.raider_dict[row['ID']] = r
        print(r)
        raiders.append(r)
    jstr = json.dumps([ob.__dict__ for ob in raiders])
    with open('epgp.json', 'w') as outfile:
        outfile.write(jstr)


#@deprecation.deprecated()
def sync_loot_from_gsheet_to_json():
    loot_from_gsheet = get_loot_from_gsheet()
    df = pd.DataFrame.from_dict(loot_from_gsheet)
    loots = []
    for index, row in df.iterrows():
        bis_spec = []
        bis_input = str(row['BIS'])
        for i in range(int(len(bis_input) / 2)):
            bis_spec.append(bis_input[2 * i:2 * i + 2])
        l = loot.Loot(row['Item Name'], row['Final GP'], bis_spec, row['Boss'])
        cfg.loot_dict[row['Item Name']] = l
        print(l)
        loots.append(l)
    jstr = json.dumps([ob.__dict__ for ob in loots])
    with open('loot.json', 'w') as outfile:
        outfile.write(jstr)


#@deprecation.deprecated()
def dump_loot_from_memory_to_json():
    loots = []
    for value in cfg.loot_dict.values():
        loots.append(value)
    jstr = json.dumps([ob.__dict__ for ob in loots], indent=4)
    with open('loot.json', 'w') as outfile:
        outfile.write(jstr)
