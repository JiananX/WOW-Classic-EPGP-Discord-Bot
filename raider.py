import json


class Raider:
    def __init__(self, ID, EP, GP, in_raid, stand_by, author, author_id):
        self.ID = ID
        self.EP = EP
        self.GP = GP
        self.in_raid = in_raid
        self.stand_by = stand_by
        self.author = author
        self.author_id = author_id

    def __str__(self):
        return f'{self.ID}  EP: {self.EP} GP: {self.GP} PR: {round(self.EP/self.GP, 3)}'

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
