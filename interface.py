# On importe les modules nécéssaires
from random import randint
import pygame as pg
import os

pg.init()   # On initialise PyGame

os.environ['SDL_VIDEO_CENTERED'] = '1'  # On centre la fenêtre PyGame
screen_width = 800  # On définit la longueur de la fenêtre
screen_height = 600 # On définit la largeur de la fenêtre
screen = pg.display.set_mode((screen_width, screen_height)) # On initialise la fenêtre de 800 par 600 pixels

# On définit plusieurs couleurs au format rgb 
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (34,139,34)
violet = (238,130,238)
blue = (0, 0, 255)
yellow = (255, 255, 0)

font = "HarryPotterFont.ttf"    # On utilise une police d'écriture spécifique

selected = "Start"  # On sélectionne "Start" au lancement du programme
is_this_main_menu = True    # On est au menu principal au lancement du programme

# On initialise une fréquence de rafraichissement
clock = pg.time.Clock()
FPS = 30


# Fonction permettant de préparer l'affichage de texte
def text_format(message, textFont, textSize, textColor):
    newFont=pg.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
    return newText

# Affichage du menu principal et du sous-menu en fonction du paramètre entré 
def main_menu(first_menu):
    global selected, is_this_main_menu

    for event in pg.event.get():    # On liste tous les évenements qui se sont déroulés entre les deux frames
        if event.type == pg.QUIT:   # L'utilisateur ferme la fenêtre, on quitte donc le programme
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:    # L'utilisateur a appuyé sur le clavier
            if event.key == pg.K_UP:    # L'utilisateur a appuyé sur la flèche du haut
                if first_menu: selected = "Start"
                elif selected == "Back": selected = "Single game"
                else: selected = "10 games"
            elif event.key == pg.K_DOWN:    # L'utilisateur a appuyé sur la flèche du bas
                if first_menu: selected = "Quit"
                elif selected == "Single game": selected = "Back"
                elif selected != "Back": selected = "Single game"
            elif event.key == pg.K_RETURN:    #L'utilisateur a appuyé sur entrée
                if first_menu:
                    if selected == "Start":
                        selected = "10 games"
                        is_this_main_menu = False
                    elif selected == "Quit":
                        pg.quit()
                        quit()
                else:
                    if selected == "Single game":
                        game(True)
                    elif selected == "10 games":
                        game(False)
                    else:
                        is_this_main_menu = True
                        selected = "Start"


    screen.fill(blue)   # On met le fond en bleu
    # On affiche un titre au menu et on met en plus gros et en blanc ce qui est sélectionné par l'utilisateur, le reste est noir
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

    else: # Texte du sous-menu
        title = text_format("Select your mode", font, 100, yellow)
        if selected == "Single game":
            text2 = text_format("Single game", font, 80, white)
        else:
            text2 = text_format("Single game", font, 60, black)
        if selected == "10 games":
            text1 = text_format("10 games", font, 80, white)
        else:
            text1 = text_format("10 games", font, 60, black)
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
    screen.blit(text1, (screen_width/2 - (text1_rect[2]/2), 300 if first_menu else 225))
    screen.blit(text2, (screen_width/2 - (text2_rect[2]/2), 400 if first_menu else 325))

# Si on a sélectionné une partie, une petite animation des équipes s'affrontant se lance
def match_anouncement():
    screen.fill(black)
    title = text_format("The match will be", font, 60, violet)

    if randint(0, 1) == 0:  # On détermine au hasard soit un match Gryffondor - Serpentard soit Poufssouffle - Serdaigle
        team1 = text_format("Gryffindor", font, 60, red)
        team2 = text_format("Slytherin", font, 60, green)
        v = text_format("V", font, 200, red)
        s = text_format("S", font, 200, green)
    else:
        team1 = text_format("Hufflepuff", font, 60, yellow)
        team2 = text_format("Ravenclaw", font, 60, blue)
        v = text_format("V", font, 200, yellow)
        s = text_format("S", font, 200, blue)

    title_rect = title.get_rect()
    team1_rect = team1.get_rect()
    team2_rect = team2.get_rect()
    v_rect = v.get_rect()
    s_rect = s.get_rect()

    screen.blit(title, (screen_width/2 - (title_rect[2]/2), 50))
    pg.display.update()
    pg.time.wait(2000)  # On attends un petit peu avant d'afficher la suite

    screen.blit(team1, (screen_width/2 + 225 - (team1_rect[2]/2), screen_height/2 - 50))
    pg.display.update()
    pg.time.wait(1000)

    screen.blit(team2, (screen_width/2 - 225 - (team2_rect[2]/2), screen_height/2 -50))
    pg.display.update()
    pg.time.wait(1000)

    screen.blit(v, (screen_width/2 - 25 - (v_rect[2]/2), screen_height/2 - 100))
    screen.blit(s, (screen_width/2 + 25 - (s_rect[2]/2), screen_height/2 - 100))
    pg.display.update()
    pg.time.wait(1000)

# On affiche un classement des scores des joueurs pariants et un classement des maisons
def leaderboard():
    print("Leaderboard")

# On simule la partie ou les 10 parties en fonction du paramètre entré (une partie - ou - 10 parties)
def game(single):
    if single:  # Si on ne simule qu'une partie, on lance l'animation de l'annoncement du match + celle des points gagnés par chaque équipe par rapport à la simu
        match_anouncement()
    else:
        print("10 games!")
    leaderboard() # Display leaderboard of characters and houses

def running():
    while 1:
        main_menu(True if is_this_main_menu else False)  # Si on est sur le menu principal on affiche le menu principal sinon on affiche le sous-menu
        pg.display.update() # On rafraichit l'image
        clock.tick(FPS) # On définit la vitesse de rafraichissement
        pg.display.set_caption("Quidditch simulator 💀")    # On définit le titre de la fenêtre

running()
pg.quit()
quit()
