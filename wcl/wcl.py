from wcl.wcl_object import ReportCharacter, Fight, FightEvent
from wcl.query import basic_report_query, event_query

import json
import requests

token = None
report_fights = {}
report_characters = {}
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

    result = _send_gql_request(
        basic_report_query(code))["data"]["reportData"]["report"]

    current_fights = result["fights"]
    for idx, fight in enumerate(current_fights):
        report_fights.update({
            fight["id"]:
            Fight(fight["id"], fight['name'], fight["startTime"],
                  fight["endTime"])
        })

    current_character = result["masterData"]["actors"]
    for idx, character in enumerate(current_character):
        if (character['subType'] != 'Unknown'):
            report_characters.update({
                character["id"]:
                ReportCharacter(character["id"], character['name'])
            })

    # (TODO) Consider remove this with other feature
    for fight in report_fights.values():
        if (report_potion_usage.get(fight.NAME) == None):
            print(fight.NAME)
            query_brust_and_mana_potion(code, fight.ID)


def query_brust_and_mana_potion(code, fight_id):
    if (token == None):
        initilization()

    if (report_fights.get(fight_id) == None):
        return
    # 28499: 大蓝
    # 41617: 毒蛇大蓝
    # 41617: 要塞大蓝
    # 28508: 毁灭药水
    # 28507: 加速药水
    tracking_spell_id = [28499, 41617, 41618, 28508, 28507]

    tracking_events = []
    for spell_id in tracking_spell_id:
        result = _send_gql_request(
            event_query(
                code, report_fights[fight_id],
                spell_id))["data"]["reportData"]["report"]["events"]["data"]
        for event in result:
            tracking_events.append(
                FightEvent(event["sourceID"], event["abilityGameID"]))

    potion_dic = {}
    for event in tracking_events:
        game_id = report_characters[event.ACTOR_ID].NAME;
        if (potion_dic.get(game_id) == None):
            potion_dic.update({game_id: 1})
        else:
            potion_dic[game_id] += 1

    report_potion_usage.update({report_fights[fight_id].NAME: potion_dic})


def _send_gql_request(query):
    response = requests.post(
        "https://cn.classic.warcraftlogs.com/api/v2/client",
        headers={"authorization": f"Bearer {token}"},
        json={"query": query})
    return response.json()
