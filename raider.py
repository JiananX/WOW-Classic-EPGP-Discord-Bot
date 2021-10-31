import json

class Raider:
  def __init__(self, ID, EP, GP, in_raid):
    self.ID = ID
    self.EP = EP
    self.GP = GP
    self.in_raid = False

  def __str__(self):
    return f'{self.ID}  EP: {self.EP} GP: {self.GP} PR: {round(self.EP/self.GP, 3)}';

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__)