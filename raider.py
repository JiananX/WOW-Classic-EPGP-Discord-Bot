class Raider:
  def __init__(self, name, ep, gp, in_raid):
    self.name = name
    self.ep = ep
    self.gp = gp
    self.in_raid = False

  def __str__(self):
    return f'{self.name} ep: {self.ep} gp: {self.gp}';