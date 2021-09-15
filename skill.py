class Skill:
    def __init__(self, name, levels):
        self.name = name
        self.levels = levels
        self.add = [0] * (levels+1)
        self.mul = [1] * (levels+1)
    
    def getAdd(self, idx):
        return self.add[min(self.levels, idx)]
    def getMul(self, idx):
        return self.mul[min(self.levels, idx)]
    def getMisc(self, idx):
        return self.misc[min(self.levels, idx)]

    @staticmethod
    def genSkills() -> dict:
        atkBoost = Skill('attack boost', 7)
        atkBoost.add = [0, 3, 6, 9, 7, 8, 9, 10]
        atkBoost.mul = [1, 1, 1, 1, 1.05, 1.06, 1.08, 1.1]

        eleAtk = Skill('element attack', 5)
        eleAtk.add = [0, 2, 3, 4, 4, 4]
        eleAtk.mul = [1, 1, 1, 1.05, 1.1, 1.2]

        critEye = Skill('critical eye', 7)
        critEye.add = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4]

        wex = Skill('weakness exploit', 3)
        wex.add = [0, 0.15, 0.3, 0.5]

        critBoost = Skill('critical boost', 3)
        critBoost.add = [0, 0.05, 0.1, 0.15]

        critEle = Skill('critical element', 3)
        critEle.add = [0, 0.05, 0.1, 0.15]

        rapidMorph = Skill('rapid morph', 3)
        rapidMorph.mul = [1, 1, 1.1, 1.2]
        rapidMorph.misc = [0, 0.2, 0.4, 0.6]

        blud = Skill('bludgeoner', 3)

        powerProlonger = Skill('power prolonger', 3)
        powerProlonger.add = [0, 15, 27, 45]

        return {
            'attack boost': atkBoost,
            'element attack': eleAtk,
            'critical eye': critEye,
            'weakness exploit': wex,
            'critical boost': critBoost,
            # 'critical element': critEle,
            'rapid morph': rapidMorph,
            'power prolonger': powerProlonger,
            # 'bludgeoner': blud,
            # 'handicraft': handi
        }