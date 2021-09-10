import os
from itertools import product
from math import floor

class Weapon:
    def __init__(self):
        self.atk = 0
        self.aff = 0
        self.ele = 0
        self.powerPhial = 1
        self.elementPhial = 1
        self.dragonPhial = 0
        self.numSkills = 0
        self.sharpBreak = [0]
        self.atkMulti = 1
        self.eleMulti = 1
        self.sharpSkills = 0
        self.sharp = 'green'
        self.eleAtk = 0

        self.rampNums = {
            'i': 4,
            'ii': 6,
            'iii': 8,
            'iv': 10
        }
    
    def applyRampUp(self, ramp):
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
        elif ramp == 'elemental boost ii':
            self.ele += 7
        elif ramp == 'sharpness type i':
            self.sharpBreak = [0, 1]
        elif ramp == 'sharpness type iii':
            self.sharpBreak = [0]
            self.sharpSkills = 0
            self.atk -= 10
        elif ramp == 'sharpness type iv':
            self.sharp = 'white'
            self.sharpSkills = 1
            self.sharpBreak = [0]
            self.atk -= 20
        elif ramp == 'anti-aeriel species':
            self.atkMulti *= 1.05
        elif ramp == 'anti-aquatic species':
            self.atkMulti *= 1.1
        elif ramp == 'valstrax soul':
            self.eleMulti *= 1.2

class Atk:
    def __init__(self, mv, type, isMorph=False, name=''):
        self.name = name
        self.mv = mv
        self.type = type.lower()
        self.isMorph = isMorph
    
    def __str__(self):
        return str(self.mv)

class Skill:
    def __init__(self, name, levels):
        self.name = name
        self.levels = levels
        self.skillLevels = range(levels+1)
        self.atkUp = [0] * (levels+1)
        self.atkPct = [1] * (levels+1)
        self.aff = [0] * (levels+1)

class Calculator:
    def __init__(self):
        self.sharpOrder = {
            'red': 0,
            'orange': 1,
            'yellow': 2,
            'green': 3,
            'blue': 4,
            'white': 5
        }

        self.sharpChart = {
            0: (0.5, 0.25),
            1: (0.75, 0.5),
            2: (1, 0.75),
            3: (1.05, 1),
            4: (1.2, 1.0625),
            5: (1.32, 1.15),
        }

    def calcDmg(self, wep, skills, buffs, motionValue, hzv):
        atkUp = sum(buffs)
        atkPct = 1
        critAtkDmg = 1.25

        eleUp = [0, 2, 3, 4, 4, 4]
        elePct = [1, 1, 1, 1.05, 1.1, 1.2]
        wepEle = max(wep.dragonPhial, wep.ele)
        critEleDmg = 1

        aff = wep.aff
        sharpIdx = self.sharpOrder[wep.sharp]

        for skill, level in skills.values():
            atkUp += skill.atkUp[level]
            atkPct *= skill.atkPct[level]
            aff += skill.aff[level]

        handi = skills.get('Handicraft')
        if handi != None:  sharpIdx += handi[0].misc[handi[1]]
        critBoost = skills.get('Critical Boost')
        if critBoost != None: critAtkDmg = critBoost[0].misc[critBoost[1]]
        critEle = skills.get('Critical Element')
        if critEle != None: critEleDmg = critEle[0].misc[critEle[1]]
        if aff >= 1: aff = 1

        # For Bludgeoner
        if sharpIdx == 3:
            bludArr = [1, 1, 1, 1.1]
            blud = skills.get('Bludgeoner')
            if blud[0] != None: atkPct *= bludArr[blud[1]]
        elif sharpIdx < 3:
            bludArr = [1, 1.05, 1.1, 1.1]
            blud = skills.get('Bludgeoner')
            if blud[0] != None: atkPct *= bludArr[blud[1]]

        atkSharp = self.sharpChart[sharpIdx][0]
        eleSharp = self.sharpChart[sharpIdx][1]

        atkDmg = floor(wep.atk*(atkPct)+atkUp+0.1)
        eleDmg = floor(wepEle*(elePct[wep.eleAtk])+eleUp[wep.eleAtk]+0.1)

        dmg = 0
        for atk in motionValue:
            atkHit = atkDmg * atkSharp * hzv[0] * atk.mv * wep.atkMulti
            eleHit = eleDmg * eleSharp * hzv[1] * wep.eleMulti
            
            rm = skills.get('Rapid Morph')
            if atk.isMorph and rm != None: atkHit *= rm[0].misc[rm[1]]
            if atk.type != 'axe':
                atkHit *= wep.powerPhial
                eleHit *= wep.elementPhial
            else:
                if wep.dragonPhial != 0: eleHit = 0

            if atk.type != 'amp':
                atkCrit = round(atkHit * critAtkDmg)
                eleCrit = round(eleHit * critEleDmg)
            else:
                atkCrit = round(atkHit)
                eleCrit = round(eleHit)
            
            atkHit = round(atkHit)
            eleHit = round(eleHit)
            
            dmg += atkHit*(1-aff) + atkCrit*aff + eleHit*(1-aff) + eleCrit*aff
        
        return dmg

def main():
    hzv = [0.6, 0.2]
    powercharm = 6
    powertalon = 9
    dangoBooster = 9
    mightSeed = 10
    demonPowder = 10
    demondrug = 5
    megaDemondrug = 7
    buffs = [powercharm, powertalon, demondrug]

    ampExp = Atk(0.1, 'amp')
    doubleSlash1 = Atk(0.28, 'sword')
    doubleSlash2 = Atk(0.36, 'sword')
    morphAxe1 = Atk(0.3, 'axe', isMorph=True)
    morphAxe2 = Atk(0.6, 'axe', isMorph=True)
    morphSword = Atk(0.23, 'sword', isMorph=True)

    unampMotionValue = [doubleSlash1, doubleSlash2, morphAxe1, morphAxe2, morphSword]
    ampMotionValue = unampMotionValue + [ampExp] * 5 
    motionValue = ampMotionValue

    atkBoost = Skill('Attack Boost', 7)
    atkBoost.atkUp = [0, 3, 6, 9, 7, 8, 9, 10]
    atkBoost.atkPct = [1, 1, 1, 1, 1.05, 1.06, 1.08, 1.1]

    critEye = Skill('Critical Eye', 7)
    critEye.aff = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4]

    wex = Skill('Weakness Exploit', 3)
    wex.aff = [0, 0.15, 0.3, 0.5]

    critBoost = Skill('Critical Boost', 3)
    critBoost.misc = [1, 1.3, 1.35, 1.4]

    critEle = Skill('Critical Element', 3)
    critEle.misc = [1, 1.05, 1.1, 1.15]

    rapidMorph = Skill('Rapid Morph', 3)
    rapidMorph.misc = [1, 1, 1.1, 1.2]

    blud = Skill('Bludgeoner', 3)

    handi = Skill('Handicraft', 5)

    calc = Calculator()

    while True:
        mode = input('Bulk (b) or Calc (c)? ')

        if mode == 'b':

            # Read file
            with open('weapons.csv', 'r') as f:
                contents = f.read()
            contents = contents.split('\n')
            contents.pop()

            for line in contents[1:]:
                line = line.split(',')
                for ramp in line[9].split(';'):
                    wep = Weapon()
                    wep.numSkills = 17

                    wep.name = line[0]
                    wep.atk = int(line[1])
                    wep.aff = float(line[2]) / 100
                    wep.ele = int(line[3])
                    wep.eleType = line[4]
                    wep.sharp = line[5]
                    wep.sharpBreak = [int(num) for num in line[6].split(';')]
                    wep.numSkills += int(line[7])
                    wep.sharpSkills = int(line[10])
                    wep.eleAtk = int(line[11])

                    wep.phial = line[8].lower()
                    if wep.phial == 'power':
                        wep.powerPhial = 1.15
                        wep.numSkills -= 1
                    elif wep.phial == 'element':
                        wep.elementPhial = 1.45
                    elif 'dragon' in wep.phial:
                        wep.dragonPhial = int(line[8].split(';')[-1])
                    wep.applyRampUp(ramp)

                    if wep.sharp in ('blue', 'white'):
                        blud.skillLevels = [0]
                    else:
                        blud.skillLevels = range(4)

                    handi.misc = wep.sharpBreak
                    handi.skillLevels = range(len(wep.sharpBreak))

                    results = []
                    skillList = [atkBoost, critEye, wex, critBoost, critEle, blud, rapidMorph, handi]
                    for it in product(*(skill.skillLevels for skill in skillList)):
                        skills = {}
                        for n in range(len(skillList)):
                            skills[skillList[n].name] = (skillList[n], it[n])

                        dmg = calc.calcDmg(wep, skills, buffs, motionValue, hzv)
                        if skills['Handicraft'][1] != 0: wep.sharpSkills = 3
                        numSkills = wep.numSkills - wep.sharpSkills
                        if (sum(it) < numSkills and skills['Attack Boost'][1]>=4) or \
                        (sum(it) < numSkills and skills['Critical Eye'][1]>=3) or \
                        (sum(it) < numSkills and skills['Attack Boost'][1]>=2 and skills['Critical Eye'][1]>=1) or\
                        (sum(it) == numSkills and skills['Attack Boost'][1]>=2 and skills['Critical Eye'][1]>= 3) or \
                        (sum(it) == numSkills and skills['Attack Boost'][1]>=4 and skills['Critical Eye'][1]>=2) or \
                        (sum(it) == numSkills and skills['Critical Eye'][1]>=6 and skills['Critical Boost'][1]>=1) or \
                        (sum(it) == numSkills+1 and (skills['Critical Eye'][1]>=6 and skills['Attack Boost'][1]>=2) and skills['Critical Boost'][1]>=1) or \
                        (sum(it) == numSkills+1 and (skills['Critical Eye'][1]>=5 and skills['Attack Boost'][1]>=4) and skills['Critical Boost'][1]>=1) or \
                        (sum(it) == numSkills+1 and (skills['Critical Eye'][1]>=2 and skills['Attack Boost'][1]>=2 and skills['Bludgeoner'][1]>=3)):
                            results.append((it, dmg))

                    results.sort(key=lambda x:x[1])

                    if not os.path.exists('tmp.csv'):
                        with open('tmp.csv', 'w') as f:
                            skillStr = ''
                            for skill in skillList:
                                skillStr += f',{skill.name}'
                            f.write(f'Combo Dmg,Weapon,Rampage Skill,Num Skills{skillStr},Element Attack,Wep Atk,Wep Aff,Wep Ele,Ele Type,Wep Srp,Phial\n')

                    with open('tmp.csv', 'a') as f:
                        numStr = ''
                        result = results[-1]
                        for num in result[0]:
                            numStr += f',{num}'
                        f.write(f'{result[-1]},{wep.name},{ramp},{sum(result[0])}{numStr},{wep.eleAtk},{wep.atk},{wep.aff},{wep.ele},{wep.eleType},{wep.sharp},{wep.phial}\n')

                    print(results[-1])
            break
        elif mode == 'c':
            wep = Weapon()
            wep.numSkills = 13

            wep.name = 'Abyssal Storm Axe'
            wep.atk = 190
            wep.aff = 0 / 100
            wep.ele = 43
            wep.eleType = ''
            wep.sharp = 'blue'
            wep.sharpBreak = [0, 0, 1]
            wep.eleAtk = 5

            wep.phial = 'element'
            if wep.phial == 'power':
                wep.powerPhial = 1.15
            elif wep.phial == 'element':
                wep.elementPhial = 1.45
            elif 'dragon' in wep.phial:
                wep.dragonPhial = int(line[8].split(';')[-1])
            wep.applyRampUp('Attack Boost III')

            if wep.sharp in ('blue', 'white'):
                blud.skillLevels = [0]
            else:
                blud.skillLevels = range(4)

            handi.misc = wep.sharpBreak
            handi.skillLevels = range(len(wep.sharpBreak))

            results = []
            skillList = [atkBoost, critEye, wex, critBoost, critEle, blud, rapidMorph, handi]
            for it in product(*(skill.skillLevels for skill in skillList)):
                skills = {}
                for n in range(len(skillList)):
                    skills[skillList[n].name] = (skillList[n], it[n])

                dmg = calc.calcDmg(wep, skills, buffs, motionValue, hzv)
                if sum(it) == wep.numSkills:
                    results.append((it, dmg))

            results.sort(key=lambda x:x[1])
            for result in results:
                print(result)
            print('AB,CE,WEX,CB,CEle,Blud,RM,Handi')
            break
            

if __name__ == '__main__':
    exit(main())