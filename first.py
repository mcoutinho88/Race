import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
dark_green = (0, 200, 0)
red = (255, 0, 0)
dark_red = (200, 0, 0)
blue = (0, 0, 255)

block_color = [(53, 115, 255), (255, 100, 24)]

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Race')
clock = pygame.time.Clock()

carImg = pygame.image.load('mycar.png')
car_dim = carImg.get_size()   #  tuple (width, height)
carIcon = pygame.image.load('carIcon.png')

pygame.display.set_icon(carIcon)

pause = False
#crash = False

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def things(xt, yt, wt, ht, color):
    pygame.draw.rect(gameDisplay,color,[xt,yt,wt,ht])


def car(x, y):
    gameDisplay.blit(carImg, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 100)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)

    game_loop()

def crash():
    #message_display('You Crashed...')
    largeText = pygame.font.Font('freesansbold.ttf', 90)
    TextSurf, TextRect = text_objects("You Crashed...", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # gameDisplay.fill(white)

        button("Play Again", 150, 450, 100, 50, dark_green, green, game_loop)
        button("Exit", 550, 450, 100, 50, dark_red, red, quitgame)

        pygame.display.update()
        clock.tick(15)


def button(msg, x, y, w, h, icolor, acolor, action=None ):
    mouse = pygame.mouse.get_pos()  # [x , y]
    click = pygame.mouse.get_pressed()


    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, acolor, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, icolor, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 15)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w/2)), (y + (h/2)))
    gameDisplay.blit(textSurf, textRect)

def quitgame():
    pygame.quit()
    quit()

def unpause_game():
    global pause
    pause = False

def pause_game():

    largeText = pygame.font.Font('freesansbold.ttf', 90)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #gameDisplay.fill(white)

        button("Continue", 150, 450, 100, 50, dark_green, green, unpause_game)
        button("Exit", 550, 450, 100, 50, dark_red, red, quitgame)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    intro = True;

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 100)
        TextSurf, TextRect = text_objects("Race", largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 150, 450, 100, 50, dark_green, green, game_loop)
        button("Exit", 550, 450, 100, 50, dark_red, red, quitgame)

        pygame.display.update()
        clock.tick(15)

def game_loop():
    x = display_width * 0.45
    y = display_height * 0.8

    gameExit = False
    global pause

    x_change = 0
    thing_count = 1
    thing_w = 100
    thing_h = 100
    thing_x = []
    thing_y = []

    thing_x.append(random.randrange(0, display_width - thing_w))
    print(thing_x)
    #thing_x_start = random.randrange(0, display_width - thing_w)
    thing_y_start = -600
    thing_speed = 3


    dodged = 0

    keys = pygame.key.get_pressed()

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    pause_game()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
            # print(event)
        x += x_change
        gameDisplay.fill(white)


        for i in range(thing_count):
            things(thing_x[i], thing_y_start, thing_w, thing_h, block_color[i])

        thing_y_start += thing_speed
        car(x,y)
        things_dodged(dodged)

        if x > display_width-car_dim[0] or x < 0:
            crash()


        if y < thing_y_start + thing_h:
            for i in range(thing_count):
                if x > thing_x[i] and x < thing_x[i] + thing_w or x + car_dim[0] > thing_x[i] and x + car_dim[0] < thing_x[i] + thing_w:
                    crash()


        if thing_y_start > display_height:
            thing_x.pop()
            if (thing_count > 1):
                thing_x.pop()
            thing_y_start = 0 - thing_h
            thing_x.append(random.randrange(0, display_width - int(thing_w)))
            #print(thing_x)

            if dodged > 3:
                thing_count = 2

            if(thing_count > 1):
                thing_x.append(random.randrange(0, display_width - int(thing_w)))
            dodged += 1

            thing_speed += 1
            #thing_w += (dodged * 1.2)


        pygame.display.update()

        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()
