class Armor:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.skills = {}
        self.l3 = 0
        self.l2 = 0
        self.l1 = 0
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def loadArmor(filename) -> dict:
        with open(filename, 'r') as f:
            contents = f.read()
        contents = contents.split('\n')
        collection = {
            'helm': [],
            'chest': [],
            'gloves': [],
            'waist': [],
            'legs': [],
            'charm': []
        }
        for line in contents[1:]:
            line = line.split(',')
            armor = Armor()
            armor.name = line[0].lower()
            armor.type = line[1].lower()
            if line[2] != '':
                for skill in line[2].split(';'):
                    skill, lv = skill.split('-') 
                    armor.skills[skill.lower().strip()] = int(lv)
            armor.l3 = int(line[3])
            armor.l2 = int(line[4])
            armor.l1 = int(line[5])
            collection[armor.type].append(armor)
        return collection

