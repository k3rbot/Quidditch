from random import randint
import pygame as pg
from pygame.locals import *
import os

pg.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'

screen_width = 800
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height))

def text_format(message, textFont, textSize, textColor):
    newFont=pg.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
    return newText

white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (34,139,34)
violet = (238,130,238)
blue = (0, 0, 255)
yellow = (255, 255, 0)

font = "HarryPotterFont.ttf"
selected = "Start"
is_this_main_menu = True

clock = pg.time.Clock()
FPS = 30

def main_menu(first_menu):
    global selected, is_this_main_menu

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                if first_menu: selected = "Start"
                elif selected == "Back": selected = "Single game"
                else: selected = "10 games"
            elif event.key == pg.K_DOWN:
                if first_menu: selected = "Quit"
                elif selected == "Single game": selected = "Back"
                elif selected != "Back": selected = "Single game"
            if event.key == pg.K_RETURN:
                if first_menu:
                    if selected == "Start":
                        selected = "10 games"
                        is_this_main_menu = False
                    if selected == "Quit":
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


    screen.fill(blue)
    if first_menu:
        title = text_format("Quidditch", font, 150, yellow)
        if selected == "Start":
            text1 = text_format("START", font, 80, white)
        else:
            text1 = text_format("START", font, 60, black)
        if selected == "Quit":
            text2 = text_format("QUIT", font, 80, white)
        else:
            text2 = text_format("QUIT", font, 60, black)

    else:
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
    
    title_rect = title.get_rect()
    text1_rect = text1.get_rect()
    text2_rect = text2.get_rect()

    screen.blit(title, (screen_width/2 - (title_rect[2]/2), 50))
    screen.blit(text1, (screen_width/2 - (text1_rect[2]/2), 300 if first_menu else 225))
    screen.blit(text2, (screen_width/2 - (text2_rect[2]/2), 400 if first_menu else 325))

def match_anouncement():
    screen.fill(black)
    title = text_format("The match will be", font, 60, violet)

    if randint(0, 1) == 0:
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
    pg.time.wait(2000)

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


def game(single):
    if single:
        match_anouncement()
    print("game!")
    pg.quit()
    quit()

def running():
    while 1:
        main_menu(True if is_this_main_menu else False)  
        pg.display.update()
        clock.tick(FPS)
        pg.display.set_caption("Quidditch simulator 💀")

running()
pg.quit()
quit()
