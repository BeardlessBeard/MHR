from attack import Attack

class Combo:
    def __init__(self):
        self.attacks = []
        self.timeSecond = 0
    
    @staticmethod
    def switchAxeAmped():
        rv = Combo()
        ampExp = Attack(0.1, 'amp')
        doubleSlash1 = Attack(0.28, 'sword')
        doubleSlash2 = Attack(0.36, 'sword')
        morphAxe1 = Attack(0.3, 'axe', isMorph=True)
        morphAxe2 = Attack(0.6, 'axe', isMorph=True)
        morphSword = Attack(0.23, 'sword', isMorph=True)
        rv.attacks = [doubleSlash1, doubleSlash2, morphAxe1, morphAxe2, morphSword] + [ampExp] * 5
        rv.timeSeconds = 5.1
        return rv
    
    @staticmethod
    def switchAxeUnamped():
        rv = Combo()
        ohs = Attack(0.32, 'sword')
        doubleSlash1 = Attack(0.3, 'sword')
        doubleSlash2 = Attack(0.6, 'sword')
        heavenFury1 = Attack(0.3, 'sword')
        heavenFury2 = Attack(0.38, 'sword')
        rv.attacks = [ohs, doubleSlash1, doubleSlash2, heavenFury1, heavenFury2]
        rv.timeSeconds = 5.3
        return rv


