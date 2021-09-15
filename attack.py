class Attack:
    def __init__(self, mv, type, isMorph=False, name=''):
        self.name = name
        self.mv = mv
        self.type = type.lower()
        self.isMorph = isMorph
    
    def __str__(self):
        return str(self.mv)