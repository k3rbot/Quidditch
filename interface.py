import time
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

font = "HarryPotter.ttf"
selected = "start"
menu = "Main menu"

clock = pg.time.Clock()
FPS = 30

def main_menu():
    global selected, menu

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                selected = "start"
            elif event.key == pg.K_DOWN:
                selected = "quit"
            if event.key == pg.K_RETURN:
                if selected == "start":
                    print("Start")
                    menu = "Mode selection"
                    selected = "10 games"
                if selected == "quit":
                    pg.quit()
                    quit()

    screen.fill(blue)
    title = text_format("Quidditch", font, 150, yellow)
    if selected == "start":
        text_start = text_format("START", font, 80, white)
    else:
        text_start = text_format("START", font, 60, black)
    if selected == "quit":
        text_quit = text_format("QUIT", font, 80, white)
    else:
        text_quit = text_format("QUIT", font, 60, black)

    title_rect = title.get_rect()
    start_rect = text_start.get_rect()
    quit_rect = text_quit.get_rect()

    screen.blit(title, (screen_width/2 - (title_rect[2]/2), 50))
    screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
    screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 400))

def mode_selection():
    global games, selected, menu
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                selected = "10 games"
            elif event.key == pg.K_DOWN:
                selected = "Single game"
            if event.key == pg.K_RETURN:
                if selected == "Single game":
                    menu = "Match anouncement"
                if selected == "10 games":
                    menu = "Game"
                    games = 10

    screen.fill(blue)
    title = text_format("Select your mode", font, 100, yellow)
    if selected == "Single game":
        text_start = text_format("Single game", font, 80, white)
    else:
        text_start = text_format("Single game", font, 60, black)
    if selected == "10 games":
        text_quit = text_format("10 games", font, 80, white)
    else:
        text_quit = text_format("10 games", font, 60, black)

    title_rect = title.get_rect()
    start_rect = text_start.get_rect()
    quit_rect = text_quit.get_rect()

    screen.blit(title, (screen_width/2 - (title_rect[2]/2), 50))
    screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 400))
    screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 300))


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
    time.sleep(2)

    screen.blit(team1, (screen_width/2 + 225 - (team1_rect[2]/2), screen_height/2 - 50))
    pg.display.update()
    time.sleep(1)

    screen.blit(team2, (screen_width/2 - 225 - (team2_rect[2]/2), screen_height/2 -50))
    pg.display.update()
    time.sleep(1)

    screen.blit(v, (screen_width/2 - 25 - (v_rect[2]/2), screen_height/2 - 100))
    screen.blit(s, (screen_width/2 + 25 - (s_rect[2]/2), screen_height/2 - 100))
    pg.display.update()
    time.sleep(1)


def game():
    print("game!")
    pg.quit()
    quit()

def running():
    while 1:
        if menu == "Main menu":
            main_menu()
        elif menu == "Mode selection":
            mode_selection()
        elif menu == "Match anouncement":
            match_anouncement()
        elif menu == "Game":
            game()
        
        pg.display.update()
        clock.tick(FPS)
        pg.display.set_caption("Quidditch simulator 💀")

running()
pg.quit()
quit()