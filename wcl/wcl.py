from wcl.wcl_object import Fight, FightEvent
from wcl.query import basic_report_query, event_query, death_query, find_latest_report

import math
import json
import requests
import time

# 28499: 大蓝
# 41617: 毒蛇大蓝
# 41617: 要塞大蓝
# 28508: 毁灭药水
# 28507: 加速药水
# 28714: 烈焰菇
# 27869: 黑暗符文
# 17528: 强效怒气药水
# 28495: 治疗药水
# 28515: 铁盾药水
tracking_spell_id = [
    28499, 41617, 41618, 28508, 28507, 28714, 27869, 17528, 28495, 28515
]

token = None

report_fights = {}
report_players = set()
report_deaths = {}
report_potion_usage = {}


def initilization():
    global token

    client_id = None
    client_secret = None
    with open('wcl/auth.json') as infile:
        data = json.load(infile)
        client_id = data['client_id']
        client_secret = data['client_secret']

    response = requests.post('https://www.warcraftlogs.com/oauth/token',
                             data={'grant_type': 'client_credentials'},
                             auth=(client_id, client_secret))

    token = json.loads(response.text)["access_token"]


def query_basic_report(code):
    if (token == None):
        initilization()

    # code = _send_gql_request(find_latest_report(round(time.time() * 1000)-604800000
    # ))
    #["data"]["reportData"]["reports"]["data"][0]['code']

    result = _send_gql_request(
        basic_report_query(code))["data"]["reportData"]["report"]

    current_players = {}
    current_fights = {}
    for player in result["masterData"]["actors"]:
        if (player['subType'] != 'Unknown'):
            report_players.add(player['name'])

            current_players.update({player["id"]: player['name']})

    for fight in result["fights"]:
        all_player_names = []

        for player_id in fight['friendlyPlayers']:
            all_player_names.append(current_players[player_id])

        report_fights.update({
            fight["name"]:
            Fight(fight["id"], fight['name'], fight["startTime"],
                  fight["endTime"], all_player_names)
        })
        current_fights.update({
            fight["name"]:
            Fight(fight["id"], fight['name'], fight["startTime"],
                  fight["endTime"], all_player_names)
        })

    for fight in current_fights.values():
        #print(fight.NAME)
        # Assume the events are in the time order
        deaths = _send_gql_request(death_query(
            code, fight))["data"]["reportData"]["report"]["events"]["data"]

        fight_deaths = {}
        for death in deaths:
            fight_deaths.update(
                {current_players[death["targetID"]]: death["timestamp"]})

        report_deaths.update({fight.fight_name: fight_deaths})

        tracking_events = []
        for spell_id in tracking_spell_id:
            result = _send_gql_request(event_query(
                code, fight,
                spell_id))["data"]["reportData"]["report"]["events"]["data"]
            for event in result:
                tracking_events.append(
                    FightEvent(current_players[event["sourceID"]],
                               event["abilityGameID"]))

        potion_dic = {}
        for event in tracking_events:
            if (potion_dic.get(event.player_name) == None):
                potion_dic.update({event.player_name: 1})
            else:
                potion_dic[event.player_name] += 1

        report_potion_usage.update({fight.fight_name: potion_dic})


def send_out_res():
    res = ''
    for fight in report_fights.values():
        time_overlap = fight.end_time - fight.start_time
        res += '%s(%s分钟),' % (
            fight.fight_name, round(time_overlap / 60000.0, 3), )

    res += '\n'
    for player in report_players:
        res += player + ' '
        for fight in report_fights.values():
            potion_usage = report_potion_usage[fight.fight_name]

            if (player not in fight.player_names):
                res += 'X '
            else:
                actual = 0
                if (potion_usage.get(player) != None):
                    actual = potion_usage[player]

                
                if (player in report_deaths[fight.fight_name].keys()):
                    res += '[%s]'%(actual)
                else:
                  res += str(actual)
                
                res += ' '

        res += '\n'

    print(res)


def _send_gql_request(query):
    # Why cn cannot working API nmot working
    response = requests.post("https://classic.warcraftlogs.com/api/v2/client",
                             headers={"authorization": f"Bearer {token}"},
                             json={"query": query})
    return response.json()
