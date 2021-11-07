class ReportCharacter:
    def __init__(self, ID, NAME):
        self.ID = ID
        self.NAME = NAME

class Fight:
    def __init__(self, ID, NAME, STARTTIME, ENDTIME):
        self.ID = ID
        self.NAME = NAME
        self.STARTTIME = STARTTIME
        self.ENDTIME = ENDTIME

class FightEvent:
    def __init__(self, ACTOR_ID, SPELL_ID):
      self.ACTOR_ID = ACTOR_ID
      self.SPELL_ID = SPELL_ID
