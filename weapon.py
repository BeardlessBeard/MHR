from typing import List
from combo import Combo

class Weapon:
    def __init__(self, wepType: str):
        self.name = ''
        self.atk = 0
        self.aff = 0
        self.ele = 0
        self.eleType = 'n/a'
        self.sharp = 3
        self.sharpBreak = [0]
        self.l1 = 0
        self.l2 = 0
        self.l3 = 0
        self.phial = ''
        self.powerPhial = 1
        self.elementPhial = 1
        self.dragonPhial = 0
        self.ramps = []
        self.sharpSkills = 0
        self.atkMulti = 1
        self.eleMulti = 1
        self.rampNums = {
            'i': 4,
            'ii': 6,
            'iii': 8,
            'iv': 10
        }
        self.chargeTimes = {
            'power': 45,
            'paralysis': 30,
            'element': 21,
            'exhaust': 21,
            'dragon': 15,
            'poison': 15,
        }
        self.sharpOrder = {
            'red': 0,
            'orange': 1,
            'yellow': 2,
            'green': 3,
            'blue': 4,
            'white': 5
        }
        if wepType.lower() == 'switch axe':
            self.ampCombo = Combo.switchAxeAmped()
            self.unampCombo = Combo.switchAxeUnamped()
    
    def __str__(self):
        return self.name
    
    def getChargeTime(self):
        for key, val in self.chargeTimes.items():
            if key in self.phial:
                return val

    def applyRampUp(self, ramp: str):
        ramp = ramp.lower().strip()
        if 'attack boost' in ramp:
            num = ramp.split()[-1]
            self.atk += self.rampNums[num]
        elif 'element boost' in ramp:
            num = ramp.split()[-1]
            self.ele += self.rampNums[num]
        elif 'affinity boost' in ramp:
            num = ramp.split()[-1]
            self.aff += self.rampNums[num] / 100
        elif ramp == 'sharpness type i':
            self.prevSharp = self.sharpBreak
            self.sharpBreak = [0, 1]
        elif ramp == 'sharpness type iii':
            self.prevSharp = self.sharpBreak
            self.prevSharpSkills = self.sharpSkills
            self.sharpBreak = [0]
            self.sharpSkills = 0
            self.atk -= 10
        elif ramp == 'sharpness type iv':
            self.prevSharp = self.sharp
            self.prevSharpSkills = self.sharpSkills
            self.prevSharpBreak = self.sharpBreak
            self.sharp = 5
            self.sharpSkills = 1
            self.sharpBreak = [0]
            self.atk -= 20
        elif ramp == 'anti-aeriel species':
            self.atkMulti *= 1.05
        elif ramp == 'anti-aquatic species':
            self.atkMulti *= 1.1
        elif ramp == 'valstrax soul':
            self.eleMulti *= 1.2
        elif 'daora' in ramp:
            self.aff += 0.25
    
    def removeRampUp(self, ramp):
        ramp = ramp.lower().strip()
        if 'attack boost' in ramp:
            num = ramp.split()[-1]
            self.atk -= self.rampNums[num]
        elif 'element boost' in ramp:
            num = ramp.split()[-1]
            self.ele -= self.rampNums[num]
        elif 'affinity boost' in ramp:
            num = ramp.split()[-1]
            self.aff -= self.rampNums[num] / 100
        elif ramp == 'sharpness type i':
            self.sharpBreak = self.prevSharp
        elif ramp == 'sharpness type iii':
            self.sharpBreak = self.prevSharp
            self.sharpSkills = self.prevSharpSkills
            self.atk += 10
        elif ramp == 'sharpness type iv':
            self.sharp = self.prevSharp
            self.sharpSkills = self.prevSharpSkills
            self.sharpBreak = self.prevSharpBreak
            self.atk += 20
        elif ramp == 'anti-aeriel species':
            self.atkMulti /= 1.05
        elif ramp == 'anti-aquatic species':
            self.atkMulti /= 1.1
        elif ramp == 'valstrax soul':
            self.eleMulti /= 1.2
        elif ramp == " daora’s soul":
            self.aff -= 0.25

    @staticmethod
    def loadWeapons(filename: str) -> list:
        with open(filename, 'r') as f:
            contents = f.read()
        contents = contents.split('\n')
        contents.pop()

        weapons = []
        for line in contents[1:]:
            line = line.split(',')
            wep = Weapon('switch axe')
            wep.name = line[0].strip()
            wep.atk = int(line[1])
            wep.aff = float(line[2]) / 100
            wep.ele = int(line[3])
            wep.eleType = line[4].strip()
            wep.sharp = wep.sharpOrder[line[5].strip()]
            wep.sharpBreak = [int(num) for num in line[6].split(';')]
            wep.l1 = int(line[7])
            wep.l2 = int(line[8])
            wep.l3 = int(line[9])
            wep.phial = line[10].lower().strip()
            if wep.phial == 'power':
                wep.powerPhial = 1.15
            elif wep.phial == 'element':
                wep.elementPhial = 1.45
            elif 'dragon' in wep.phial:
                wep.dragonPhial = int(line[10].split(';')[-1])
            wep.ramps = [ramp for ramp in line[11].split(';')]
            wep.sharpSkills = int(line[12])
            weapons.append(wep)
        return weapons