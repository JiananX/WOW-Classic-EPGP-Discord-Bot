class Loot:
  def __init__(self, id, name, gp, is_bis):
    self.id = id
    self.name = name
    self.gp = gp
    self.is_bis = False

  def __str__(self):
    return  f'{self.name}  gp: {self.gp} bis: {self.is_bis}';