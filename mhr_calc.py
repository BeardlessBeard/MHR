import sys
import os
from itertools import combinations_with_replacement
from copy import deepcopy
from math import floor
from typing import List

sys.path.append('.')
from skill import Skill
from weapon import Weapon
from armor import Armor

class Calculator:
    def __init__(self):
        self.sharpChart = {
            0: (0.5, 0.25),
            1: (0.75, 0.5),
            2: (1, 0.75),
            3: (1.05, 1),
            4: (1.2, 1.0625),
            5: (1.32, 1.15),
        }
        self.skills = Skill.genSkills()
    
    def __getAdd(self, skillName):
        return self.skills[skillName].getAdd(self.currBuild.get(skillName, 0))
    def __getPct(self, skillName):
        return self.skills[skillName].getMul(self.currBuild.get(skillName, 0))
    def __getMisc(self, skillName):
        return self.skills[skillName].getMisc(self.currBuild.get(skillName, 0))

    def getComboDmg(self, atkDmg, atkSharp, critAtkDmg, eleDmg, eleSharp, critEleDmg, aff, hz, combo, wep):
        dmg = 0
        for atk in combo.attacks:
            atkHit = atkDmg * atkSharp * hz[0] * atk.mv * wep.atkMulti
            eleHit = eleDmg * eleSharp * hz[1] * wep.eleMulti
            
            rm = self.__getPct('rapid morph')
            if atk.isMorph: atkHit *= rm
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
        return dmg / (combo.timeSeconds - self.__getMisc('rapid morph'))
    
    def calcDmg(self, wep: Weapon, build: dict, buffs: List[float], hzv: List[List[float]]):
        atkUp = sum(buffs)
        atkPct = 1
        eleUp = 0
        elePct = 1
        critAtkDmg = 1.25

        wepEle = max(wep.dragonPhial, wep.ele)
        critEleDmg = 1

        aff = wep.aff
        sharpIdx = wep.sharp

        self.currBuild = build

        # Attack Boost
        atkUp += self.__getAdd('attack boost')
        atkPct *= self.__getPct('attack boost')
        # Element Attack
        eleUp += self.__getAdd('element attack')
        elePct *= self.__getPct('element attack')
        # Teostra Patch
        if build.get("teostra blessing", 0) > 0 and wep.eleType=='fire':
            if build.get("teostra blessing") == 1: elePct *= 1.05
            else: elePct *= 1.1
        # Critical Eye
        aff += self.__getAdd('critical eye')
        aff = min(aff,1)
        # Critical Boost
        critAtkDmg += self.__getAdd('critical boost')
        # Critical Element
        # critEleDmg += self.__getAdd('critical element')
        # Bludgeoner
        '''if sharpIdx == 3:
            bludArr = [1, 1, 1, 1.1]
            atkPct *= bludArr[build.get('bludgeoner', 0)]
        elif sharpIdx < 3:
            bludArr = [1, 1.05, 1.1, 1.1]
            atkPct *= bludArr[build.get('bludgeoner', 0)]'''

        atkSharp = self.sharpChart[sharpIdx][0]
        eleSharp = self.sharpChart[sharpIdx][1]

        atkDmg = floor(wep.atk*(atkPct)+atkUp+0.1)
        eleDmg = floor(wepEle*(elePct)+eleUp+0.1)

        ampLegDps = self.getComboDmg(atkDmg, atkSharp, critAtkDmg, eleDmg, eleSharp, critEleDmg, aff, hzv[1], wep.ampCombo, wep)
        unampLegDps = self.getComboDmg(atkDmg, atkSharp, critAtkDmg, eleDmg, eleSharp, critEleDmg, aff, hzv[1], wep.unampCombo, wep)

        # Weakness Exploit
        aff += self.__getAdd('weakness exploit')
        aff = min(aff,1)
        ampHeadDps = self.getComboDmg(atkDmg, atkSharp, critAtkDmg, eleDmg, eleSharp, critEleDmg, aff, hzv[0], wep.ampCombo, wep)
        unampHeadDps = self.getComboDmg(atkDmg, atkSharp, critAtkDmg, eleDmg, eleSharp, critEleDmg, aff, hzv[0], wep.unampCombo, wep)

        ampDps = ampLegDps*hzv[1][2] + ampHeadDps*hzv[0][2]
        unampDps = unampLegDps*hzv[1][2] + unampHeadDps*hzv[0][2]

        efr = atkDmg*(1+(critAtkDmg-1)*aff)*atkSharp
        efe = eleDmg*(1+(critEleDmg-1)*aff)*eleSharp

        ampPct = (45+self.__getAdd('power prolonger'))/(45+self.__getAdd('power prolonger')+wep.getChargeTime())
        unampPct = 1-ampPct
        dps = ampDps * ampPct + unampDps * unampPct
        
        return (efr, efe, ampPct, unampLegDps,ampLegDps,unampHeadDps,ampHeadDps,dps)

def addSkills(build, armor):
    for skill, lv in armor.skills.items():
        if build.get(skill) == None:
            build[skill] = 0
        build[skill] += lv
    return

def removeSkills(build, armor):
    for skill, lv in armor.skills.items():
        build[skill] -= lv
    return

def verifyBuild(build, skills):
    for skill, lv in build.items():
        if skills.get(skill) != None:
            if lv > skills.get(skill).levels:
                return False
    return True

def main():
    hzv = [[0.6, 0.2, 0.5], [0.4, 0.15, 0.5]]
    powercharm = 6
    powertalon = 9
    dangoBooster = 9
    mightSeed = 10
    demonPowder = 10
    demondrug = 5
    megaDemondrug = 7
    buffs = [powercharm, powertalon, demondrug]

    srpToStr = ['red','orange','yellow','green','blue','white']

    calc = Calculator()

    weapons = Weapon.loadWeapons('weapons.csv')
    armor = Armor.loadArmor('armor.csv')
    with open ('out.csv', 'w') as f:
        f.write(
            'weapon,attack,affinity,element,element type,sharpness,phial,ramp,'+\
            'helm,chest,gloves,waist,legs,charm,decos,element attack,'+\
            'efr,efe,amped %,unamped leg dps,amped leg dps,unamped head dps,amped head dps,dps\n'
        )
    for wep in weapons:
        bestDmg = 0
        bestBuild = []
        for ramp in wep.ramps:
            wep.applyRampUp(ramp)
            build = {}
            for helm in armor['helm']:
                addSkills(build, helm)
                for chest in armor['chest']:
                    addSkills(build, chest)
                    for gloves in armor['gloves']:
                        # Dragonheart no amp patch
                        if 'valstrax' in gloves.name and wep.eleType not in ('n/a', 'dragon'):
                            continue
                        addSkills(build, gloves)
                        # verify build hasn't maxed out a key skill
                        if verifyBuild(build, calc.skills) == False:
                            removeSkills(build, gloves)
                            continue
                        for waist in armor['waist']:
                            addSkills(build, waist)
                            # verify build hasn't maxed out a key skill
                            if verifyBuild(build, calc.skills) == False:
                                removeSkills(build, waist)
                                continue
                            for legs in armor['legs']:
                                addSkills(build, legs)
                                # verify build hasn't maxed out a key skill
                                if verifyBuild(build, calc.skills) == False:
                                    removeSkills(build, legs)
                                    continue
                                for charm in armor['charm']:
                                    addSkills(build, charm)
                                    # verify build hasn't maxed out a key skill
                                    if verifyBuild(build, calc.skills) == False:
                                        removeSkills(build, charm)
                                        continue
                                    # Handicraft
                                    for i in range(len(wep.sharpBreak)):
                                        # l1 stuff
                                        l1 = helm.l1+chest.l1+gloves.l1+waist.l1+legs.l1+charm.l1+wep.l1
                                        if wep.eleType != 'n/a':
                                            build['element attack'] = min(l1, 5)
                                        # l2 stuff
                                        l2 = helm.l2+chest.l2+gloves.l2+waist.l2+legs.l2+charm.l2+wep.l2+\
                                            helm.l3+chest.l3+gloves.l3+waist.l3+legs.l3+charm.l3+wep.l3
                                        l3 = helm.l3+chest.l3+gloves.l3+waist.l3+legs.l3+charm.l3+wep.l3
                                        if build.get('evade extender', 0) == 0: 
                                            l2 -= 1
                                        # Sharpness
                                        handiReq = wep.sharpBreak[i] - build['handicraft']
                                        sharpSkills = wep.sharpSkills if i == 0 else 3
                                        sharpSkills = sharpSkills+handiReq-build.get('protective polish', 0)
                                        l2 -= sharpSkills
                                        # End early if invalid
                                        if l2 < 0 or handiReq > l3:
                                            break
                                        if sharpSkills < 0: 
                                            continue
                                        wep.sharp += i
                                        # Remove already maxed skills to save some time
                                        decoSkills = list(calc.skills.keys())
                                        for skill in calc.skills.keys():
                                            if build.get(skill, 0) >= calc.skills[skill].levels:
                                                decoSkills.remove(skill)
                                        for decos in combinations_with_replacement(decoSkills, l2):
                                            # Add decos to build
                                            for skill in decos:
                                                if build.get(skill) == None:
                                                    build[skill] = 0
                                                build[skill] += 1
                                            # Check if decos went over the skill size
                                            if verifyBuild(build, calc.skills) == False:
                                                for skill in decos:
                                                    build[skill] -= 1
                                                continue
                                            dmg = calc.calcDmg(wep, build, buffs, hzv)
                                            dps = dmg[7]
                                            if(dps > bestDmg):
                                                bestDmg = dps
                                                bestBuild = [{
                                                    'weapon': deepcopy(wep),
                                                    'ramp': ramp,
                                                    'helm': str(helm), 
                                                    'chest': str(chest), 
                                                    'gloves': str(gloves), 
                                                    'waist': str(waist), 
                                                    'legs': str(legs),
                                                    'charm': str(charm),
                                                    'decos': decos,
                                                    'eleAtk': build.get('element attack', 0),
                                                    'dmg': dmg,
                                                }]
                                            elif(dps == bestDmg):
                                                bestBuild.append({
                                                    'weapon': deepcopy(wep),
                                                    'ramp': ramp,
                                                    'helm': str(helm), 
                                                    'chest': str(chest), 
                                                    'gloves': str(gloves), 
                                                    'waist': str(waist), 
                                                    'legs': str(legs),
                                                    'charm': str(charm),
                                                    'decos': decos,
                                                    'eleAtk': build.get('element attack', 0),
                                                    'dmg': dmg,
                                                })
                                            # Undo decos
                                            for skill in decos:
                                                build[skill] -= 1
                                        # Undo Sharp
                                        wep.sharp -= i
                                    # Undo Charm
                                    removeSkills(build, charm)
                                # Undo Legs
                                removeSkills(build, legs)
                            # Undo Waist
                            removeSkills(build, waist)
                        # Undo Gloves
                        removeSkills(build, gloves)
                    # Undo Chest
                    removeSkills(build, chest)
                # Undo Helm
                removeSkills(build, helm)
            # Undo Ramp
            wep.removeRampUp(ramp)
        with open('out.csv', 'a') as f:
            for build in bestBuild:
                print(f'writing for {build["weapon"]}')
                f.write(
                    f"{build['weapon'].name},{build['weapon'].atk},{build['weapon'].aff},{build['weapon'].ele},"+\
                    f"{build['weapon'].eleType},{srpToStr[build['weapon'].sharp]},{build['weapon'].phial},"+\
                    f"{build['ramp']},{build['helm']},{build['chest']},{build['gloves']},{build['waist']},"+\
                    f"{build['legs']},{build['charm']},\"{build['decos']}\",{build['eleAtk']},"+\
                    f"{build['dmg'][0]},{build['dmg'][1]},{build['dmg'][2]},{build['dmg'][3]},{build['dmg'][4]},"+\
                    f"{build['dmg'][5]},{build['dmg'][6]},{build['dmg'][7]}\n"
                )

if __name__ == '__main__':
    exit(main())