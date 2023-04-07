import pygame
import sys
import random
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.newBlock = False

        self.head_up = pygame.image.load(
            'Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load(
            'Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load(
            'Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load(
            'Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load(
            'Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(
            'Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(
            'Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(
            'Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(
            'Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(
            'Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(
            'Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(
            'Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(
            'Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(
            'Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def drawSnake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            # we need a rect for the position
            x_pos = int(block.x * cellSize)
            y_pos = int(block.y * cellSize)
            blockRect = pygame.Rect(x_pos, y_pos, cellSize, cellSize)

            # what direction the face is heading
            if index == 0:
                screen.blit(self.head, blockRect)
            # we need to update the snake head direction
            elif index == len(self.body) -1:
                screen.blit(self.tail, blockRect)
            else:
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, blockRect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, blockRect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, blockRect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, blockRect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, blockRect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, blockRect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def moveSnake(self):
        if self.newBlock == True:
            bodyCopy = self.body[:]
            # move snake forward
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy[:]
            self.newBlock = False
        else:
            bodyCopy = self.body[:-1]
            # move snake forward
            bodyCopy.insert(0, bodyCopy[0] + self.direction)
            self.body = bodyCopy[:]

    def addBlock(self):
        self.newBlock = True
    
    def munchSound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class Apple:
    def __init__(self):
        # create an x and y position
        self.randomize()

    def drawApple(self):
        appleRect = pygame.Rect(
            int(self.pos.x * cellSize), int(self.pos.y * cellSize), cellSize, cellSize)
        # drawing time
        screen.blit(icon_apple, appleRect)
        # pygame.draw.rect(screen, (126, 111, 114), appleRect)

    def randomize(self):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Apple()

    def update(self):
        self.snake.moveSnake()
        self.appleEaten()
        self.checkEndGame()

    def drawElem(self):
        self.drawGrass()
        self.fruit.drawApple()
        self.snake.drawSnake()
        self.score()

    def appleEaten(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()  # reposition apple
            self.snake.addBlock()  # extend the snake
            self.snake.munchSound()
        
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def checkEndGame(self):
        # if snake head is outside screen or hits itself, then end game
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
            self.gameOver()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()

    def gameOver(self):
        self.snake.reset()
    
    def drawGrass(self):
        grassColor = (167,209,61)

        for row in range(cellNumber):
            if row % 2 ==0:
                for column in range(cellNumber):
                    if column%2 == 0:
                        grassRect = pygame.Rect(column * cellSize, row * cellSize, cellSize,cellSize)
                        pygame.draw.rect(screen, grassColor, grassRect)
            else:
                for column in range(cellNumber):
                    if column%2 != 0:
                        grassRect = pygame.Rect(column * cellSize, row * cellSize, cellSize,cellSize)
                        pygame.draw.rect(screen, grassColor, grassRect)
    
    def score(self):
        scoreText = str(len(self.snake.body) - 3)
        scoreSurface = font.render(scoreText, True, (56,74,12))
        score_x = int(cellSize * cellNumber - 60)
        score_y = int(cellSize * cellNumber - 40)
        scoreRect = scoreSurface.get_rect(center = (score_x, score_y))
        appleRect = icon_apple.get_rect(midright = (scoreRect.left, scoreRect.centery))
        backgroundRect = pygame.Rect(appleRect.left, appleRect.top, appleRect.width + scoreRect.width + 6, appleRect.height)

        pygame.draw.rect(screen, (167,209, 61), backgroundRect)
        screen.blit(scoreSurface, scoreRect)
        screen.blit(icon_apple, appleRect)
        pygame.draw.rect(screen, (56,74,12), backgroundRect, 2)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cellSize = 40
cellNumber = 20
screen = pygame.display.set_mode((cellNumber * cellSize, cellNumber * cellSize))  # main display surface
clock = pygame.time.Clock()  # object to help control time (60 frames/second)
icon_apple = pygame.image.load('Graphics/apple.png').convert_alpha()
font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 150)

main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if the user wants to leave, close app
            pygame.quit()
            sys.exit()

        if event.type == screen_update:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    main_game.drawElem()
    pygame.display.update()  # draw all our elements
    clock.tick(60)
