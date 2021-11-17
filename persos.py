projet_tab = []
nb = 0 

with open("Characters.csv", mode='r', encoding='utf-8') as f:
    lines = f.readlines()
    key_line = lines[0].strip()
    keys = key_line.split(";")
    for line in lines[1:5]:
        line = line.strip()
        values = line.split(';')
        dico = {}
        for i in range(len(keys)):
            if i != 0:
                dico[keys[i]] = values[i]
            else:
                dico["Points"] = 0
        projet_tab.append(dico)
    
print(projet_tab)

print(sorted(projet_tab, key=lambda x: x["Points"], reverse = True))
