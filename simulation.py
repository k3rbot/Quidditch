from random import randint
pointvifdor = 0
pointvifdor2 = 0
while pointvifdor != 25 and pointvifdor2 != 25 :
    pointball = randint(1,3)
    if pointball == 2:
        pointball =10
    pointvifdor = randint(1,50)
    if pointvifdor == 25:
        pointvifdor = 150
    point_equipe_1 = pointball + pointvifdor 
    pointball2 = randint(1,3)
    if pointball2 == 2:
        pontball2 = 10
    pointvifdor2 = randint(1,50)
    if pointvifdor2==25:
        pointvifdor2=150
    point_equipe_2 = pointball2 + pointvifdor2
print(f"lequipe 1 a marqué {point_equipe_1},et l'equipe 2 a marqué {point_equipe_2}")