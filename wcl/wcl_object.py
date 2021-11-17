class Fight:
    def __init__(self, fight_id, fight_name, start_time, end_time, player_names):
        self.fight_id = fight_id
        self.fight_name = fight_name
        self.start_time = start_time
        self.end_time = end_time
        self.player_names = player_names


class FightEvent:
    def __init__(self, player_name, spell_id):
        self.player_name = player_name
        self.spell_id = spell_id
