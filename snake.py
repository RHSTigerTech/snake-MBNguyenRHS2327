# Name: Malina Nguyen
# Program: SnakeClone
import time
import random
import pygame
import sys

from pygame.locals import *

# Note that Global variables are generally not recomended to prevent difficult to trace bugs
# Global variables are used in this program.
# The justification is that all of these global variables are actually CONSTANTS
# so thier values should never change (preventing that difficult to trace bug)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CELL_SIZE = 40
assert WINDOW_WIDTH % CELL_SIZE == 0,  "cell size must divide WINDOW_WIDTH"
assert WINDOW_HEIGHT % CELL_SIZE == 0,  "cell size must divide WINDOW_HEIGHT"

CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

WHITE     = (255, 255, 255)  
BLACK     = (  0,   0,   0)  
RED       = (255,   0,   0)  
GREEN     = (  0, 255,   0)  
DARKGREEN = (  0, 155,   0) 
DARKGRAY  = ( 40,  40,  40)  
BGCOLOR = BLACK  

UP = 'up'  
DOWN = 'down'  
LEFT = 'left'  
RIGHT = 'right'  
HEAD = 0        # syntactic sugar: index of the worm's head 
X = 0
Y = 1

def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption("sNaKe_ClOnE")
    zenmode = showStartScreen()  # Not yet defined
    while True:
        runGame(zenmode)  # Needs work


def showStartScreen():
    print("Start the Snake Game!!!")
                            # Hover over render to see what the params mean
    instText = BASIC_FONT.render("Use wasd or Arrows to turn.", True, RED, BLACK)
    startText = BASIC_FONT.render("Press Any key to start", True, GREEN, BLACK)
    DISPLAY_SURF.fill(BLACK)
    DISPLAY_SURF.blit(instText, (WINDOW_WIDTH/10, WINDOW_HEIGHT//8))
    DISPLAY_SURF.blit(startText, (WINDOW_WIDTH/10, WINDOW_HEIGHT-50))
    pygame.display.update()
    while True: 
        ## CHECK FOR USER INPUT ##
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:  
                terminate()
            elif event.type == KEYDOWN: 
                if event.key == K_ESCAPE:  
                    terminate()
                elif event.key == K_z:
                    return True
                return False

 
#done needs 
def drawGrid():
    pygame.draw.rect(DISPLAY_SURF, BLACK, Rect(0,0,WINDOW_WIDTH, WINDOW_HEIGHT))
    # Use loops to draw lines (or rectangles) for the grid background
    
    #vertical lines
    for x in range(CELL_WIDTH):
        pygame.draw.line(DISPLAY_SURF, DARKGRAY, (x*CELL_SIZE, 0), (x*CELL_SIZE, WINDOW_HEIGHT))    
    #horizontal lines
    for y in range(CELL_HEIGHT):
        pygame.draw.line(DISPLAY_SURF, DARKGRAY, (0, y*CELL_SIZE), (WINDOW_WIDTH, y*CELL_SIZE))


def terminate():
    pygame.quit()
    sys.exit()


def drawApple(appleLocation, rot):
    rot_red = (255, 0, 0+(rot*10))
    # print (rot, rot_red)
    apple = pygame.Rect(appleLocation[X]*CELL_SIZE, appleLocation[Y]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAY_SURF, rot_red, apple)


def drawSnake(snakeCoords):
    for segment in snakeCoords:
        snakeBodySeg = pygame.Rect(segment[X]*CELL_SIZE, segment[Y]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, GREEN, snakeBodySeg)
        snakeBodySeg = pygame.Rect(segment[X]*CELL_SIZE+2, segment[Y]*CELL_SIZE+2, CELL_SIZE-4, CELL_SIZE-4)
        pygame.draw.rect(DISPLAY_SURF, DARKGREEN, snakeBodySeg)


def showGameOverScreen():
    # loop to get player "stuck" on game over
    # break the loop when they prpess a button like the start screen
    while True:
        goFont = pygame.font.Font('freesansbold.ttf', 100)
        gameText = goFont.render("Game", True, GREEN, BLACK)
        overText = goFont.render("Over", True, GREEN, BLACK)
        playText = BASIC_FONT.render("Press any key to play again.", True, RED, BLACK)
        DISPLAY_SURF.fill(BLACK)
        DISPLAY_SURF.blit(gameText, (WINDOW_WIDTH/10, WINDOW_HEIGHT//8))
        DISPLAY_SURF.blit(overText, (WINDOW_WIDTH/8, WINDOW_HEIGHT//2))
        DISPLAY_SURF.blit(playText, (WINDOW_WIDTH/10, WINDOW_HEIGHT-50))
        pygame.display.update()
        time.sleep(1)
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:  
                terminate()
            elif event.type == KEYDOWN: 
                if event.key == K_ESCAPE:  
                    terminate()
                elif event.key == K_z:
                    runGame(True)
                else:
                    runGame(False)


def drawScore(score):
    goFont = pygame.font.Font('freesansbold.ttf', 35)
    scoreText = goFont.render(str(score), True, GREEN, None)
    DISPLAY_SURF.blit(scoreText, (0, 0))


def getRandomLocation(snakeCoords):
    # return a tuple (#,#) that represent an x,y corrdinate
    x = random.randint(0, CELL_WIDTH-1)
    while x == snakeCoords[0][0]:
        x = random.randint(0, CELL_WIDTH-1)
    y = random.randint(0, CELL_HEIGHT-1)
    while y == snakeCoords[0][1]:
        y = random.randint(0, CELL_HEIGHT-1)

    return (x, y)

      
def snakeSquirm(snakeCoords, colour, colour_dark):
    c = 0
    for segment in snakeCoords:
        if c %2 == 0 and segment != snakeCoords[HEAD]:
            snakeBodySeg = pygame.Rect(segment[X]*CELL_SIZE, segment[Y]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(DISPLAY_SURF, colour, snakeBodySeg)
            snakeBodySeg = pygame.Rect(segment[X]*CELL_SIZE+(CELL_SIZE/10), segment[Y]*CELL_SIZE+(CELL_SIZE/10), CELL_SIZE-(CELL_SIZE/5), CELL_SIZE-(CELL_SIZE/5))
            pygame.draw.rect(DISPLAY_SURF, colour_dark, snakeBodySeg)

        elif segment == snakeCoords[HEAD]:
            snakeBodySeg = pygame.Rect(segment[X]*CELL_SIZE, segment[Y]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(DISPLAY_SURF, colour, snakeBodySeg)
            snakeBodySeg = pygame.Rect(segment[X]*CELL_SIZE+(CELL_SIZE/10), segment[Y]*CELL_SIZE+(CELL_SIZE/10), CELL_SIZE-(CELL_SIZE/5), CELL_SIZE-(CELL_SIZE/5))
            pygame.draw.rect(DISPLAY_SURF, WHITE, snakeBodySeg)

        else:
            snakeBodySeg = pygame.Rect(segment[X]*CELL_SIZE+(CELL_SIZE/10), segment[Y]*CELL_SIZE+(CELL_SIZE/10), CELL_SIZE-(CELL_SIZE/5), CELL_SIZE-(CELL_SIZE/5))
            pygame.draw.rect(DISPLAY_SURF, colour, snakeBodySeg)
            snakeBodySeg = pygame.Rect(segment[X]*CELL_SIZE+(CELL_SIZE/5), segment[Y]*CELL_SIZE+(CELL_SIZE/5), CELL_SIZE-(CELL_SIZE/2.5), CELL_SIZE-(CELL_SIZE/2.5))
            pygame.draw.rect(DISPLAY_SURF, colour_dark, snakeBodySeg)
        c += 1

def runGame(zenmode):
    if zenmode == True:
        print("welcome to zen mode")
    startX = CELL_WIDTH // 2
    startY = CELL_HEIGHT // 2
    snakeCoords = [[startX, startY]]
    direction = random.choice([RIGHT, LEFT, UP, DOWN])
    apple = getRandomLocation(snakeCoords)
    score = 0
    rot = 0
    count = 0
    speedge = 10
    rand_colour = GREEN
    rand_colour_dark = DARKGREEN
    
    # Event handling loop
    while True: 
        ## CHECK FOR USER INPUT ##
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:  
                terminate()
            elif event.type == KEYDOWN: 
                if direction != RIGHT and (event.key == K_LEFT or event.key == K_a): 
                    direction = LEFT  

                elif direction != LEFT and (event.key == K_RIGHT or event.key == K_d):  
                    direction = RIGHT  
                    
                elif direction != DOWN and (event.key == K_UP or event.key == K_w):  
                    direction = UP  

                elif direction != UP and (event.key == K_DOWN or event.key == K_s):  
                    direction = DOWN 
                elif event.key == K_ESCAPE:  
                    terminate()
                    
            ## END OF USER INPUT ##
            
        ## ~~~~~Game Logic section~~~~##
        # Move the snake (add a new head and remove the tail)
        
        if direction == RIGHT:
            newHead = [snakeCoords[HEAD][X]+1, snakeCoords[HEAD][Y]]
        elif direction == LEFT:
            newHead = [snakeCoords[HEAD][X]-1, snakeCoords[HEAD][Y]]
        elif direction == DOWN:
            newHead = [snakeCoords[HEAD][X], snakeCoords[HEAD][Y]+1]
        elif direction == UP:
            newHead = [snakeCoords[HEAD][X], snakeCoords[HEAD][Y]-1]
        
        snakeCoords.insert(0,newHead)
        snakeCoords.pop()
        # Check for collision If the snake collides what should it do
        #       What is it colliding with ?
        if (snakeCoords[HEAD][X], snakeCoords[HEAD][Y]) == apple:
            apple = getRandomLocation(snakeCoords)
            rand_colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            rand_colour_dark = (random.randint(0, 155), random.randint(0, 155), random.randint(0, 155)) 
            if rot < 12:
                snakeCoords.insert(0,newHead)
                score += 1
                if zenmode == False:
                    speedge += 1
            elif rot > 11  and len(snakeCoords) > 1:
                for i in range(len(snakeCoords)):
                    if i < len(snakeCoords):
                        snakeCoords.pop()
                        score -= 1
                        speedge -= 1
                    else:
                        continue

            rot = 0
            
        for body in range(len(snakeCoords)):
            if snakeCoords[body][X] > CELL_WIDTH-1 and zenmode == True:
                snakeCoords[body][X] = 0
            elif snakeCoords[body][X] < 0 and zenmode == True:
                snakeCoords[body][X] = CELL_WIDTH-1
            elif snakeCoords[body][Y] > CELL_HEIGHT-1 and zenmode == True:
                snakeCoords[body][Y] = 0
            elif snakeCoords[body][Y] < 0 and zenmode == True:
                snakeCoords[body][Y] = CELL_HEIGHT-1
            if snakeCoords[HEAD] == snakeCoords[body] and body > 1 and zenmode == False:
                showGameOverScreen()
            elif snakeCoords[body][X] > CELL_WIDTH-1 or snakeCoords[body][Y] > CELL_HEIGHT-1 or snakeCoords[body][X] < 0 or snakeCoords[body][Y] < 0 and zenmode == False:
                showGameOverScreen()
        
        if count%round((speedge/2), 0) == 0 and len(snakeCoords) > 1 and CELL_SIZE > 5 and zenmode == False:
            rot += 1
        if rot > 22:
            rot = 22.5
        
        
        
        ## ~~~~~End of Logic Section~~~ ##
        
        
        ## Draw stuff then update screen
        
        drawGrid()
        snakeSquirm(snakeCoords, rand_colour, rand_colour_dark)
        drawApple(apple,rot)
        drawScore(score)
        count += 1
        
        pygame.display.update()
        FPS_CLOCK.tick(speedge)




if __name__ == "__main__":
    main()