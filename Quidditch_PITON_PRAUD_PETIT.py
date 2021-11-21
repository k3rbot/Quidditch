# On importe les modules nécéssaires
from random import randint
import pygame as pg
import os

from pygame import display

pg.init()   # On initialise PyGame

os.environ["SDL_VIDEO_CENTERED"] = "1"  # On centre la fenêtre PyGame
screen_width = 800  # On définit la longueur de la fenêtre
screen_height = 600     # On définit la largeur de la fenêtre
# On initialise la fenêtre de 800 par 600 pixels
screen = pg.display.set_mode((screen_width, screen_height))

# On définit plusieurs couleurs au format rgb
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (34, 139, 34)
violet = (128, 0, 128)
blue = (0, 0, 255)
yellow = (255, 255, 0)
golden = (212, 175, 55)
silver = (192, 192, 192)
bronze = (205, 127, 50)
orange = (255, 140, 0)

# On utilise une police d"écriture spécifique
font = "HarryPotterFont.ttf"

# On sélectionne "Start" au lancement du programme
selected = "Start"
# On est au menu principal au lancement du programme
is_this_main_menu = True
# Dictionnaire permettant de savoir la maison qui joue,
# son score et sa couleur
houses = {
    "Ravenclaw": {
        "Playing": False,
        "Color": "blue",
        "Points": 0
    },
    "Gryffindor": {
        "Playing": False,
        "Color": "red",
        "Points": 0
    },
    "Hufflepuff": {
        "Playing": False,
        "Color": "yellow",
        "Points": 0
    },
    "Slytherin": {
        "Playing": False,
        "Color": "green",
        "Points": 0
    }
}
# On stocke toutes les données du fichier csv dans un
# tableau contenant des dictionnaires
characters = []
with open("Characters.csv", mode='r', encoding='utf-8') as f:
    lines = f.readlines()
    key_line = lines[0].strip()
    keys = key_line.split(";")
    for line in lines[1:]:
        line = line.strip()
        values = line.split(';')
        character = {"Points": 2}
        for i in range(len(keys)):
            if i != 0:
                character[keys[i]] = values[i]
        characters.append(character)

# On initialise une fréquence de rafraichissement
clock = pg.time.Clock()
FPS = 30


def text_format(message, textFont, textSize, textColor):
    """
    Fonction permettant de préparer l'affichage de texte

    Entrée: le texte à afficher, la police d'écriture,
    la taille de la police et la couleur du texte
    Sortie: la surface sur laquelle à été affiché le texte
    """

    newFont = pg.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)
    return newText


def main_menu(first_menu):
    """
    Affichage du menu principal ou du sous-menu

    Entrée: un booléen qui indique si l'on se
            situe au premier menu ou au second
    """

    global selected, is_this_main_menu

    # On liste tous les évenements qui se sont
    # déroulés entre les deux frames
    for event in pg.event.get():
        # L"utilisateur ferme la fenêtre,
        # on quitte donc le programme
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        # L'utilisateur a appuyé sur le clavier
        if event.type == pg.KEYDOWN:
            # L'utilisateur a appuyé sur la flèche du haut
            if event.key == pg.K_UP:
                if first_menu:
                    # On change donc le texte sélectionné
                    selected = "Start"
                elif selected == "Back":
                    selected = "Single game"
                else:
                    selected = "10 bets"
            # L'utilisateur a appuyé sur la flèche du bas
            elif event.key == pg.K_DOWN:
                if first_menu:
                    selected = "Quit"
                elif selected == "Single game":
                    selected = "Back"
                elif selected != "Back":
                    selected = "Single game"
            # L'utilisateur a appuyé sur entrée
            elif event.key == pg.K_RETURN:
                if first_menu:
                    if selected == "Start":
                        # On change de menu
                        selected = "10 bets"
                        is_this_main_menu = False
                    elif selected == "Quit":
                        pg.quit()
                        quit()
                else:
                    if selected == "Single game":
                        game(True)
                    elif selected == "10 bets":
                        game(False)
                    else:
                        is_this_main_menu = True
                        selected = "Start"

    screen.fill(blue)   # On met le fond en bleu

    # On affiche un titre au menu et on met en plus gros
    # et en blanc ce qui est sélectionné par l'utilisateur,
    # le reste du texte est en noir
    if first_menu:  # Texte du premier menu
        title = text_format("Quidditch", font, 150, yellow)
        if selected == "Start":
            text1 = text_format("START", font, 80, white)
        else:
            text1 = text_format("START", font, 60, black)
        if selected == "Quit":
            text2 = text_format("QUIT", font, 80, white)
        else:
            text2 = text_format("QUIT", font, 60, black)

    else:   # Texte du sous-menu
        title = text_format("Select your mode", font, 100, yellow)
        if selected == "Single game":
            text2 = text_format("Single game", font, 80, white)
        else:
            text2 = text_format("Single game", font, 60, black)
        if selected == "10 bets":
            text1 = text_format("10 bets", font, 80, white)
        else:
            text1 = text_format("10 bets", font, 60, black)
        if selected == "Back":
            text3 = text_format("Back", font, 80, white)
        else:
            text3 = text_format("Back", font, 60, black)

        text3_rect = text3.get_rect()
        screen.blit(text3, (screen_width/2 - (text3_rect[2]/2), 425))

    # On récupère des infos sur le rectangle du texte pour pouvoir le centrer
    title_rect = title.get_rect()
    text1_rect = text1.get_rect()
    text2_rect = text2.get_rect()

    # On affiche tous les textes
    screen.blit(title, (screen_width/2 - (title_rect[2]/2), 50))
    screen.blit(
        text1,
        (screen_width / 2 - (text1_rect[2] / 2),
         300 if first_menu else 225))
    screen.blit(
        text2,
        (screen_width / 2 - (text2_rect[2] / 2),
         400 if first_menu else 325))


def match_anouncement():
    """
    Annoncement du match qui va opposer deux équipes,
    c'est en fait une petite animation qui va permettre
    de décider les deux équipes joueuses
    """

    # Si l'utilisateur veut fermer la fenêtre on quitte l'application
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()

    screen.fill(black)
    title = text_format("The match will be", font, 60, violet)

    # On détermine au hasard soit un match
    # Gryffondor - Serpentard soit Poufsouffle - Serdaigle
    if randint(0, 1) == 0:
        houses["Hufflepuff"]["Playing"] = True
        houses["Ravenclaw"]["Playing"] = True
        playing = ["Hufflepuff", "Ravenclaw"]
    else:
        houses["Gryffindor"]["Playing"] = True
        houses["Slytherin"]["Playing"] = True
        playing = ["Gryffindor", "Slytherin"]

    # On prépare l'affichage du nom des deux équipes s'affrontant
    team1 = text_format(playing[0], font, 60, houses[playing[0]]["Color"])
    team2 = text_format(playing[1], font, 60, houses[playing[1]]["Color"])
    v = text_format("V", font, 200, houses[playing[0]]["Color"])
    s = text_format("S", font, 200, houses[playing[1]]["Color"])

    title_rect = title.get_rect()
    team1_rect = team1.get_rect()
    team2_rect = team2.get_rect()
    v_rect = v.get_rect()
    s_rect = s.get_rect()

    # On affiche le titre "The match will be"
    screen.blit(title, (screen_width/2 - (title_rect[2]/2), 50))
    # On actualise l'écran pour y afficher notre interface
    pg.display.update()
    pg.time.wait(1000)  # On attends un petit peu avant d'afficher la suite

    # On affiche le nom de la première équipe
    screen.blit(
        team2,
        (screen_width / 2 - 225 - (team2_rect[2] / 2),
         screen_height / 2 - 50))
    pg.display.update()
    pg.time.wait(750)

    # On affiche le nom de la deuxième équipe
    screen.blit(
        team1,
        (screen_width / 2 + 225 - (team1_rect[2] / 2),
         screen_height / 2 - 50))
    pg.display.update()
    pg.time.wait(750)

    # On affiche le VS entre les deux noms d'équipe
    screen.blit(
        v, (screen_width / 2 - 25 - (v_rect[2] / 2),
            screen_height / 2 - 100))
    screen.blit(
        s, (screen_width / 2 + 25 - (s_rect[2] / 2),
            screen_height / 2 - 100))
    pg.display.update()
    pg.time.wait(450)


def anim_scores(round, prev1, prev2, snitch):
    """
    Anime l'augmentation des scores en ajoutant au fur et à mesure
    d'un "temps" les points gagnés toutes les "5 minutes"
    puis affiche le vainqueur du match

    Entrée: la manche à cet instant ce qui permet d'extrapoler
            le temps passé (1 manche = 5 min), le score
            de l'équipe 1 et 2 précédant le tirage au sort
            des points gagnés à cette manche et un booléen indiquant
            si le vif d'or à été capturé ce qui arrêterai la partie
    """

    # On utilise teams pour savoir qui est en train de jouer
    teams = (
        "Hufflepuff", "Ravenclaw") if houses["Ravenclaw"]["Playing"] else(
        "Gryffindor", "Slytherin")
    # variable qui nous permet de stopper le temps
    # quand le vif d'or est capturé
    Time = 0
    # On répète 5 fois la boucle, une fois par "minute",
    # 5 fois pour 5 "minutes"
    for i in range(1, 6):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        screen.fill(black)
        # On affiche un rectangle de 400 par 300 pixels à 200 pixels
        # de la droite de l'écran et 125 du haut
        pg.draw.rect(screen, white, (200, 125, 400, 300), 5)
        title = text_format("Score :", font, 70, yellow)
        title2 = text_format("Time :", font, 30, white)
        team1 = text_format(teams[0], font, 30, white)
        team2 = text_format(teams[1], font, 30, white)
        if snitch:
            title3 = text_format(
                "The snitch has been catched !", font, 60, yellow)
            if round*5 + 1 != Time:     # On "arrête" le temps
                Time = round*5 + 1
            # On se prépare à afficher le temps fictif
            # en plus du nombre de points de chaque équipe
            time = text_format(f"{Time}:00", font, 70, red)
            team1_score = text_format(
                str(houses[teams[0]]["Points"]),
                font, 80, houses[teams[0]]["Color"])
            team2_score = text_format(
                str(houses[teams[1]]["Points"]),
                font, 80, houses[teams[1]]["Color"])
            title3_rect = title3.get_rect()
            screen.blit(title3, (screen_width/2 - (title3_rect[2]/2), 475))
        else:
            # Ici le temps n'est pas statique,
            # il dépends du nombre d'itération de la boucle
            time = text_format(f"{round*5 + i}:00", font, 70, red)
            team1_score = text_format(
                str(int((houses[teams[0]]["Points"] - prev1) / 5 * i + prev1)),
                font, 80, houses[teams[0]]["Color"])
            team2_score = text_format(
                str(int((houses[teams[1]]["Points"] - prev2) / 5 * i + prev2)),
                font, 80, houses[teams[1]]["Color"])

        title_rect = title.get_rect()
        title2_rect = title2.get_rect()
        team1_rect = team1.get_rect()
        team2_rect = team2.get_rect()
        time_rect = time.get_rect()
        team1_score_rect = team1_score.get_rect()
        team2_score_rect = team2_score.get_rect()

        # On affiche tous les textes en plus dess scores et du temps écoulé
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 25))
        screen.blit(title2, (screen_width/2 - (title2_rect[2]/2), 130))
        screen.blit(time, (screen_width/2 - (time_rect[2]/2), 175))
        screen.blit(team1, (screen_width/2 + 100 - (team1_rect[2]/2), 275))
        screen.blit(team2, (screen_width/2 - 100 - (team2_rect[2]/2), 275))
        screen.blit(
            team1_score,
            (screen_width / 2 + 100 - (team1_score_rect[2] / 2),
             325))
        screen.blit(
            team2_score,
            (screen_width / 2 - 100 - (team2_score_rect[2] / 2),
             325))

        # Si on est à la manche 7 et à la 5ème itération
        # de la boucle le temps est écoulé
        if round == 7 and i == 5:
            title = text_format("Time is over !", font, 100, yellow)
            title_rect = title.get_rect()
            screen.blit(title, (screen_width/2 - (title_rect[2]/2), 475))
        pg.display.update()

        # Quand le match est terminé on affiche le vainqueur du match
        if (snitch or round == 7) and i == 5:
            pg.time.wait(1500)
            screen.fill(black)
            if houses[teams[0]]['Points'] == houses[teams[1]]['Points']:
                title = text_format("Draw...", font, 90, yellow)
                image = pg.image.load(f"{teams[0]}.png")
                image2 = pg.image.load(f"{teams[1]}.png")
                image_rect = image.get_rect()
                image2_rect = image2.get_rect()
                screen.blit(
                    image, (screen_width / 2 - 175 - (image_rect[2] / 2), 200))
                screen.blit(image2, (screen_width / 2 + 175 - (
                    image2_rect[2] / 2), 200))
            else:
                title = text_format("And the winner is :", font, 90, yellow)
                image = pg.image.load(
                    f"{teams[0] if houses[teams[0]]['Points'] > houses[teams[1]]['Points'] else teams[1]}.png")
                image_rect = image.get_rect()
                screen.blit(image, (screen_width/2 - (image_rect[2]/2), 200))

            title_rect = title.get_rect()
            screen.blit(title, (screen_width/2 - (title_rect[2]/2), 75))
            pg.display.update()
            pg.time.wait(1500)
        else:
            pg.time.wait(250)


def play_5min():
    """
    Simulation d'une manche (de "5 minutes") de Quidditch
    Les points vont dans la variable house au niveau des points de l'équipe
    """

    global houses, vifdor
    for equipe in (("Hufflepuff", "Ravenclaw")
                   if
                   houses["Ravenclaw"]["Playing"]
                   else("Gryffindor", "Slytherin")):
        if randint(1, 3) == 2:  # Une chance sur 3 d'avoir 10 points en plus
            houses[equipe]["Points"] += 10
        # Une chance sur 50 d'avoir 150 points en plus et de terminer la partie
        if randint(1, 50) == 25:
            houses[equipe]["Points"] += 150
            vifdor = True
            break


def bet():
    """
    Fait parier tous les joueurs faisant partie d'une des équipe jouant
    Les paris vont dans la variable characters au niveau du pari de chaque
    personnage
    """

    global characters
    playing = (
        "Gryffindor", "Slytherin") if houses["Gryffindor"]["Playing"] else(
        "Hufflepuff", "Ravenclaw")
    for i in range(len(characters)):
        # Si un personnage fait partie d'une des équipes jouant à cette partie
        # et qu'il à plus d'un point alors il peut parier, on lui retire donc
        # un point et il parie un nombre aléatoire multiple de 10
        # entre la valeur max et la minimum
        if (characters[i]["House"] == playing[0] or characters[i][
                "House"] == playing[1]) and characters[i]["Points"] > 0:
            characters[i]["Points"] -= 1
            characters[i]["Bet"] = randint(1, 23)*10
        else:
            characters[i]["Bet"] = 0


def distribute_points():
    """
    Distribue 5 points aux joueurs de l'équipe gagnante et 30
    à la personne la plus proche du score
    """

    global characters
    playing = (
        "Gryffindor", "Slytherin") if houses["Gryffindor"]["Playing"] else(
        "Hufflepuff", "Ravenclaw")
    winner = playing[0] if houses[playing[0]][
        "Points"] > houses[playing[1]]["Points"] else playing[1]
    best_bet = [999, 0]
    # On itère dans toute la liste de personnages pour leur rajouter
    # des points ou non seulement si il y a un vainqueur
    if houses[playing[0]]["Points"] != houses[playing[1]]["Points"]:
        for i in range(len(characters)):
            if characters[i]["House"] == winner:
                characters[i]["Points"] += 5
                # Si une personne à plus ou moins le score le plus proche
                # on sauvegarde son score si une autre personne fait mieux
                if characters[i]["Bet"] - houses[winner]["Points"] < best_bet[
                    0]and characters[i]["Bet"] - houses[winner][
                        "Points"] > -best_bet[0]:
                    best_bet[0] = characters[i]["Bet"]
                    best_bet[1] = i
        characters[best_bet[1]]["Points"] += 30


def anim_games(nb_game):
    """
    Affichage de toutes les parties éffectuées (20) au fur et à mesures
    qu'elles sont jouées, on y affiche le score coloré en fonction
    de l'équipe et le numéro du match

    Entrée: le nombre de parties jouées (jusqu'à 20)
    """

    playing = ("Gryffindor", "Slytherin") if houses["Gryffindor"]["Playing"]\
        else ("Hufflepuff", "Ravenclaw")

    # Au bout de 5 parties on rajoute les rectangles sur la ligne
    # du dessous et ainsi de suite jusqu'à 20 rectangles
    pg.draw.rect(screen, white, (20 + 155 * nb_game - 775*int(nb_game/5),
                                 10 + 156 * int(nb_game/5), 136, 110), 5)
    title = text_format(f"Match {nb_game+1}", font, 25, yellow)
    team1_score = text_format(str(houses[playing[0]]["Points"]), font, 30,
                              houses[playing[0]]["Color"])
    # La couleur du séparateur dépends du vainqueur
    score_separator = text_format(
        ':', font, 30, houses[playing[0]]["Color"]
        if houses[playing[0]]["Points"] >
        houses[playing[1]]["Points"] else houses[playing[1]]["Color"])
    team2_score = text_format(str(houses[playing[1]]["Points"]),
                              font, 30, houses[playing[1]]["Color"])

    title_rect = title.get_rect()
    team1_score_rect = team1_score.get_rect()

    # On affiche le texte au même endroit dans le rectangle pour chaque partie
    screen.blit(title,
                (88 + 155 * nb_game - 775*int(nb_game/5) - (title_rect[2]/2),
                 17 + 156 * int(nb_game/5)))
    screen.blit(score_separator, (88 + 155 * nb_game - 775*int(nb_game/5),
                65 + 156 * int(nb_game/5)))
    screen.blit(team1_score,
                (75 + 155 * nb_game - 775 * int(nb_game / 5) -
                 (team1_score_rect[2]),
                 65 + 156 * int(nb_game / 5)))
    screen.blit(team2_score, (110 + 155 * nb_game - 775*int(nb_game/5),
                              65 + 156 * int(nb_game/5)))

    pg.display.update()
    pg.time.wait(250)


def average_points():
    """
    Calcul de la moyenne des points gagnés par personnage
    Sortie: la moyenne des points par personnages
    """

    average = 0
    for i in characters:
        average += i["Points"]
    return int(average/140)


def leaderboard():
    """
    Affiche le tableau des scores classés dans l'ordre décroissant avec
    le nom du personnage,
    sa maison (couleur du personnage), son score et son classement
    """

    global selected, is_this_main_menu, characters

    # On trie les perssonnages de characters en fonction de leur score
    # dans l'ordre décroissant
    characters = sorted(characters, key=lambda x: x["Points"], reverse=True)

    screen.fill(black)
    # On commence par le bas du tableau puis on remonte
    for i in range(14, -1, -1):
        pg.draw.rect(screen, white, (100, 17 + 36*(i+1), 600, 37), 1)
        title = text_format("Leaderboard", font, 37, yellow)
        text = text_format(f"Average of {average_points()} points", font,
                           20, white)
        place = text_format(str(i+1), font, 35, golden if i == 0
                            else silver if i == 1 else bronze if i == 2
                            else white)
        person = text_format(characters[i]["Name"], font, 24,
                             houses[characters[i]["House"]]["Color"])
        score = text_format(str(characters[i]["Points"]), font, 32, yellow)

        title_rect = title.get_rect()
        screen.blit(title, (screen_width/2 - title_rect[2]/2, 9))
        screen.blit(text, (600, 9))
        screen.blit(place, (120, 19 + 36*(i+1)))
        screen.blit(person, (170, 19 + 36*(i+1)))
        screen.blit(score, (650, 19 + 36*(i+1)))

        pg.display.update()
        pg.time.wait(250)

    # On réinitialise les points des maison et leur état de jeu
    for team in ("Hufflepuff", "Gryffindor", "Slytherin", "Ravenclaw"):
        houses[team]["Playing"] = False
        houses[team]["Points"] = 0
    # On affiche dans la console le classement complet
    for i in range(len(characters)):
        print(f"{i+1} - {characters[i]['Name']} with {characters[i]['Points']}\
             points")

    # Réinitialise toutes les variables pour se retrouver au menu principal
    # avec comme sélection "Start"
    selected = "Start"
    is_this_main_menu = True


def winner():
    """
    Affiche le vainqueur des paris, celui qui à gagné le plus de points
    et affiches quelques unes de ses caractéristiques
    """

    screen.fill(black)

    title = text_format("The winner is:", font, 70, yellow)
    winner = text_format(characters[0]["Name"], font, 60, violet)
    points = text_format(f"With {characters[0]['Points']} points!",
                         font, 55, golden)
    house_text = text_format("House:", font, 25, orange)
    house = text_format(characters[0]["House"], font, 25,
                        houses[characters[0]["House"]]["Color"])
    wand = text_format(f"Wand: {characters[0]['Wand']}", font, 25, orange)
    job = text_format(f"Job: {characters[0]['Job']}", font, 25, orange)
    gender = text_format(
        f"Gender: {characters[0]['Gender']}", font, 25, orange)
    patronus = text_format(f"Patronus: {characters[0]['Patronus']}", font,
                           25, orange)

    title_rect = title.get_rect()
    winner_rect = winner.get_rect()
    points_rect = points.get_rect()
    house_text_rect = house_text.get_rect()
    house_rect = house.get_rect()
    wand_rect = wand.get_rect()
    job_rect = job.get_rect()
    gender_rect = gender.get_rect()
    patronus_rect = patronus.get_rect()

    screen.blit(title, (screen_width/2 - title_rect[2]/2, 50))
    screen.blit(winner, (screen_width/2 - winner_rect[2]/2, 150))
    screen.blit(points, (screen_width/2 - points_rect[2]/2, 250))
    screen.blit(house_text, (screen_width/2 - 50 - house_text_rect[2]/2, 350))
    screen.blit(house, (screen_width/2 + 50 - house_rect[2]/2, 350))
    screen.blit(wand, (screen_width/2 - wand_rect[2]/2, 390))
    screen.blit(job, (screen_width/2 - job_rect[2]/2, 430))
    screen.blit(gender, (screen_width/2 - gender_rect[2]/2, 470))
    screen.blit(patronus, (screen_width/2 - patronus_rect[2]/2, 510))

    pg.display.update()
    pg.time.wait(10000)

    # On réinitialise les points gagnés et les paris de chaques personnages
    for i in range(len(characters)):
        characters[i]["Points"] = 2
        characters[i]["Bet"] = 0


def game(single):
    """
    On va simuler une ou 20 parties en plus de gérer les paris de
    chaques personnages

    Entrée: une booléen indiquant si il s'agit d'une partie simple
    ou de 20 parties
    """

    global houses, vifdor
    vifdor = False

    # Si on ne simule qu'une partie, on lance l'animation de l'annoncement
    # du match + celle des points gagnés par chaque équipe par rapport
    # à la simulation
    if single:
        match_anouncement()     # On annonce le match
        bet()   # On prends les paris de chaques personnages jouant
        for manche in range(8):     # On joue 8 manches de "5 min" = "40 min"
            prev = (houses["Hufflepuff" if houses["Ravenclaw"]["Playing"]
                    else "Gryffindor"]["Points"], houses["Ravenclaw"
                    if houses["Ravenclaw"]["Playing"] else
                    "Slytherin"]["Points"])
            play_5min()     # On joue une manche
            # On anime le gain de score pendant ces "5 minutes"
            anim_scores(manche, prev[0], prev[1], vifdor)
            if vifdor:  # On arrête la partie si le vif d'or est attrapé
                break
        distribute_points()     # On donne les points aux parieurs
    # On va simuler 20 parties
    else:
        screen.fill(black)
        for game in range(20):  # On répète pour les 20 partie
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            vifdor = False
            # Une fois sur deux ce sera le match Gryffondor contre Serpentard
            # et l'autre fois Poufssoufle contre Serdaigle
            if game % 2 == 0:
                houses["Gryffindor"]["Playing"] = True
                houses["Slytherin"]["Playing"] = True
                houses["Gryffindor"]["Points"] = 0
                houses["Slytherin"]["Points"] = 0
                houses["Hufflepuff"]["Playing"] = False
                houses["Ravenclaw"]["Playing"] = False
            else:
                houses["Hufflepuff"]["Playing"] = True
                houses["Ravenclaw"]["Playing"] = True
                houses["Hufflepuff"]["Points"] = 0
                houses["Ravenclaw"]["Points"] = 0
                houses["Gryffindor"]["Playing"] = False
                houses["Slytherin"]["Playing"] = False
            bet()   # On prends les paris des joueurs
            for _ in range(8):  # On simule une partie de "40 minutes"
                play_5min()
                if vifdor:
                    break
            # On donne les points une fois la partie terminée
            distribute_points()
            anim_games(game)    # On montre le résultat de la partie
    pg.time.wait(1000)
    leaderboard()   # On affiche le classement
    pg.time.wait(5000)
    winner()    # On affiche le vainqueur


def running():
    """
    Fonction qui tourne en boucle jusqu'à l'arrêt commandé par Pygame
    """

    while 1:
        # Si on est sur le menu principal on affiche le menu principal
        # sinon on affiche le sous-menu
        main_menu(True if is_this_main_menu else False)
        # On rafraichit l'image
        pg.display.update()
        # On définit la vitesse de rafraichissement à 30 FPS
        clock.tick(FPS)
        # On définit le titre de la fenêtre
        pg.display.set_caption("Quidditch simulator")


running()   # On lance le programme
pg.quit()   # On quitte tout une fois que la fonction est terminée
quit()
