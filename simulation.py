from random import randint
points = [0, 0]
vifdor = False
while not(vifdor):
    for equipe in range(2):
        if randint(1,3) == 2:
            points[equipe] += 10
        if randint(1,50) == 25:
            points[equipe] = 150
            vifdor = True
print(f"lequipe 1 a marqué {points[0]}, et l'equipe 2 a marqué {points[1]}")