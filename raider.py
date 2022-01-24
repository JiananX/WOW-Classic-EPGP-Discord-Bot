class Raider:
    def __init__(self, name, ep, gp, user_id, spec):
        self.name = name
        self.ep = ep
        self.gp = gp
        self.user_id = user_id
        self.spec = spec

        self.in_raid = False
        self.standby = False
