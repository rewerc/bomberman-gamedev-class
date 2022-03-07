from select import select
import pygame, sys
import random
from math import *
from pygame import mixer
from Game import Game

#Initialize the pygame
pygame.init()

click = False

#Creating Screen
resolution = (975,687)
screen = pygame.display.set_mode(resolution)

#Title and Icon
pygame.display.set_caption("Title")
icon = pygame.image.load("assets/Icon.png")
pygame.display.set_icon(icon)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x,y)
    surface.blit(textobj, textrect)

font = pygame.font.SysFont(None, 50)

#Main Menu
def main():
    click = False
    while True:
        screen.fill((50, 50, 50))

        draw_text('Main Menu', font, (255,255,255), screen, resolution[0]/2, 200)

        mx, my = pygame.mouse.get_pos()

        button_1 =  pygame.Rect(resolution[0]/2-100, 300, 200, 50)
        button_2 =  pygame.Rect(resolution[0]/2-100, 400, 200, 50)
        
        if button_1.collidepoint((mx,my)):
            if click:
                play()
        if button_2.collidepoint((mx,my)):
            if click:
                option()
        
        click = False

        pygame.draw.rect(screen, (155,155,155), button_1)
        draw_text('Play', font, (0,0,0), screen, button_1.centerx, button_1.centery)
        pygame.draw.rect(screen, (155,155,155), button_2)
        draw_text('Options', font, (0,0,0), screen, button_2.centerx, button_2.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                #running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def selectRoom():
    running = True
    click = False
    while running:
        screen.fill((50, 50, 50))
        draw_text('Room', font, (255,255,255), screen, resolution[0]/2, 50)
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                #running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        container = pygame.Rect(resolution[0]/2, resolution[1]/2, resolution[0]-200, resolution[1]-200)
        container.center = (resolution[0]/2, resolution[1]/2)
        pygame.draw.rect(screen, (55,55,55),container)

        back =  pygame.Rect(resolution[0]/2, 400, 150, 50)
        back.topleft = (20, 20)
        pygame.draw.rect(screen, (155,155,155), back)
        draw_text('Back', font, (0,0,0), screen, back.centerx, back.centery)

        join = pygame.Rect(container.topleft[0], container.topleft[0], (container.width-200)/2 + 40, container.height-100)
        join.topleft = (container.topleft[0] + 40 , container.topleft[1] + 50)
        pygame.draw.rect(screen, (155,155,155),join)
        draw_text('Join', font, (0,0,0), screen, join.centerx, join.centery)

        create = pygame.Rect(container.topleft[0], container.topleft[0], (container.width-200)/2 + 40, container.height-100)
        create.topleft = (container.topleft[0] + 120 + (container.width-200)/2, container.topleft[1] + 50)
        pygame.draw.rect(screen, (155,155,155),create)
        draw_text('Create', font, (0,0,0), screen, create.centerx, create.centery)

        if join.collidepoint((mx,my)):
            if click:
                x = check_code(back, container)
                if type(x)== str:
                    room(back, container, x)
                running = False
        
        if create.collidepoint((mx,my)):
            if click:
                x = ''
                for i in range(6):
                    x += str(random.randint(0,9))
                room(back, container, x)
                running = False
    
        if back.collidepoint((mx,my)):
            if click:
                running = False
            
        click = False

        pygame.display.update()

def check_code(back, container):
    user_text = ''
    running = True
    while running:
        screen.fill((50,50,50))
        draw_text('Room', font, (255,255,255), screen, resolution[0]/2, 50)

        pygame.draw.rect(screen, (55,55,55),container)
        pygame.draw.rect(screen, (155,155,155), back)
        draw_text('Back', font, (0,0,0), screen, back.centerx, back.centery)
        
        draw_text('Enter Room Code:', font, (255,255,255), screen, container.centerx, container.centery-100)
        input =  pygame.Rect(resolution[0]/2, 400, 400, 130)
        input.center = (container.centerx, container.centery)
        pygame.draw.rect(screen, (155,155,155), input)

        enter =  pygame.Rect(resolution[0]/2, 400, 200, 50)
        enter.center = (input.centerx, input.centery+150)
        pygame.draw.rect(screen, (155,155,155), enter)
        draw_text('Enter', font, (0,0,0), screen, enter.centerx, enter.centery)

        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if len(user_text)<6:
                        try:
                            int(event.unicode)
                        except ValueError:
                            pass
                        else:
                           user_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        draw_text(user_text, font, (255,255,255), screen, input.centerx, input.centery)

        if back.collidepoint((mx,my)):
            if click:
                running = False
        
        if enter.collidepoint((mx,my)):
            if click:
                if len(user_text)==6:
                    running = False
                    return user_text
                    
        
        click = False

        pygame.display.update()
        


def room(back, container, code):
    running = True
    while running:
        screen.fill((50, 50, 50))
        draw_text('Room', font, (255,255,255), screen, resolution[0]/2, 50)

        pygame.draw.rect(screen, (55,55,55),container)
        pygame.draw.rect(screen, (155,155,155), back)
        draw_text('Back', font, (0,0,0), screen, back.centerx, back.centery)

        roomCode =  pygame.Rect(resolution[0]/2, 400, 200, 50)
        roomCode.center = (container.centerx, container.bottomleft[1]+50)
        pygame.draw.rect(screen, (155,155,155), roomCode)
        draw_text(code, font, (0,0,0), screen, roomCode.centerx, roomCode.centery)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                #running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        start =  pygame.Rect(resolution[0]/2, 400, 200, 50)
        start.bottomright = (resolution[0] - 20, resolution[1] - 20)
        pygame.draw.rect(screen, (155,155,155), start)
        draw_text('Start', font, (0,0,0), screen, start.centerx, start.centery)

        items = [1,2,3,4]
        for i in range(len(items)):
            items[i] = pygame.Rect(container.topleft[0], container.topleft[0], (container.width-200)/4, container.height-100)
            items[i].topleft = (container.topleft[0] + 40 + ((container.width-200)/4 + 40)*i, container.topleft[1] + 50)
            pygame.draw.rect(screen, (155,155,155),items[i])

        if back.collidepoint((mx,my)):
            if click:
                running = False

        if start.collidepoint((mx,my)):
            if click:
                play()
                running = False
        
        click = False

        pygame.display.update()

def option():
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        screen.fill((50, 50, 50))
        draw_text('Option', font, (255,255,255), screen, resolution[0]/2, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        back =  pygame.Rect(resolution[0]/2, 400, 150, 50)
        back.topleft = (20, 20)
        pygame.draw.rect(screen, (155,155,155), back)
        draw_text('Back', font, (0,0,0), screen, back.centerx, back.centery)

        if back.collidepoint((mx,my)):
            if click:
                running = False
        
        click = False

        pygame.display.update()

def game():
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        screen.fill((50, 50, 50))
        draw_text('Game', font, (255,255,255), screen, resolution[0]/2, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        back =  pygame.Rect(resolution[0]/2, 400, 150, 50)
        back.topleft = (20, 20)
        pygame.draw.rect(screen, (155,155,155), back)
        draw_text('Back', font, (0,0,0), screen, back.centerx, back.centery)

        if back.collidepoint((mx,my)):
            if click:
                running = False
        
        click = False

        pygame.display.update()

def play():
    Game()

main()