import math
import random

import pygame
from pygame import mixer

pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

#background
bg = pygame.image.load("img/background.png")
mixer.music.load('audio/background.wav')
mixer.music.play(-1)

#Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("img/spaceship.png")
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load("img/player.png")
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load("img/enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

#Bullet
bulletImg = pygame.image.load("img/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10

''' Bullet State
Ready - You can't see the bullet on the screen
Fire - The bullet is moving '''

bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over Text
gameOverfont = pygame.font.Font('freesansbold.ttf', 64)

def showScore(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def gameOver_text():
    over = gameOverfont.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over, (200, 250))

def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))

def fireBullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

#Game Loop
running = True

while running:
    screen.fill((0,0,0))
    screen.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # KeyStrokes
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            elif event.key == pygame.K_RIGHT:
                playerX_change = 5
            elif event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("audio/laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change

    #Checking for player & Boundary Collision
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Enemy Movement
    for i in range(numOfEnemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameOver_text()
            break

        enemyX[i] += enemyX_change[i] 
        if enemyX[i] < 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("audio/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
        
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()