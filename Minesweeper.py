import pygame
import random
import time
import json
import os

pygame.init()
pygame.font.init()

gameState = 'Menu'
file = open('{}\Settings.txt'.format(os.getcwd()), 'r')
settings = json.load(file)
file.close()

Black = pygame.Color(0, 0, 0)
White = pygame.Color(255, 255, 255)
Red = pygame.Color(255, 0, 0)
Green = pygame.Color(0, 255, 0)
DarkGreen = pygame.Color(0, 150, 0)
Blue = pygame.Color(0, 0, 255)
Grey = pygame.Color(169, 169, 169)
DarkGrey = pygame.Color(100, 100, 100)
Purple = pygame.Color(75, 0, 130)
Maroon = pygame.Color(128, 0, 0)
Turquoise = pygame.Color(0, 206, 209)

textColors = {1:Blue, 2:Green, 3:Red, 4:Purple,
              5:Maroon, 6:Turquoise, 7:Black, 8:DarkGrey}

font = pygame.font.SysFont('TIMESNEWROMAN', 15)
fontBig = pygame.font.SysFont('TIMESNEWROMAN', 40)
fontSet = pygame.font.SysFont('TIMESNEWROMAN', 25)

class Tile:
    opened = False
    flagged = False
    pos = (0,0)
    button = 0
    num = 0

    def __init__(self, num, pos, opened = False):
        self.num = num
        self.pos = (pos[0] * 25 + 50, pos[1] * 25 + 50)
        self.button = pygame.Rect(self.pos[0], self.pos[1], 25, 25)
        self.opened = opened

    def Draw(self):
        if self.flagged == True:
            pygame.draw.rect(screen, DarkGrey, (self.pos[0], self.pos[1], 25, 25))
            pygame.draw.rect(screen, Black, (self.pos[0], self.pos[1], 25, 25), 1)
            pygame.draw.line(screen, Black, (self.pos[0] + 18, self.pos[1] + 20),
                             (self.pos[0] + 18, self.pos[1] + 5))
            pygame.draw.polygon(screen, Red, [(self.pos[0] + 18, self.pos[1] + 5),
                                              (self.pos[0] + 18, self.pos[1] + 15),
                                              (self.pos[0] + 5, self.pos[1] + 10)])
        elif self.opened == False:
            pygame.draw.rect(screen, DarkGrey, (self.pos[0], self.pos[1], 25, 25))
            pygame.draw.rect(screen, Black, (self.pos[0], self.pos[1], 25, 25), 1)
        else:
            if self.num == -1:
                pygame.draw.rect(screen, Grey, (self.pos[0], self.pos[1], 25, 25))
                pygame.draw.rect(screen, DarkGrey, (self.pos[0], self.pos[1], 25, 25), 1)
                pygame.draw.circle(screen, Black, (self.pos[0] + 12.5, self.pos[1] + 12.5), 10)
            elif self.num > 0 and self.num < 9:
                pygame.draw.rect(screen, Grey, (self.pos[0], self.pos[1], 25, 25))
                pygame.draw.rect(screen, DarkGrey, (self.pos[0], self.pos[1], 25, 25), 1)
                text = font.render('{}'.format(self.num), True, textColors[self.num])
                screen.blit(text, (self.pos[0] + 10, self.pos[1] + 5))
            elif self.num == 0:
                pygame.draw.rect(screen, Grey, (self.pos[0], self.pos[1], 25, 25))
                pygame.draw.rect(screen, DarkGrey, (self.pos[0], self.pos[1], 25, 25), 1)
                

def SaveGame(numLeft):
    saveSlot = 0
    
    pygame.draw.rect(screen, DarkGrey, (48, 48, 204, 104))
    pygame.draw.rect(screen, Grey, (50, 50, 200, 100))
    
    slot1 = pygame.Rect(60, 60, 50, 30)
    pygame.draw.rect(screen, White, slot1)
    text = font.render('Slot 1', True, Black)
    screen.blit(text, (slot1.x + 5, slot1.y + 5))

    slot2 = pygame.Rect(120, 60, 50, 30)
    pygame.draw.rect(screen, White, slot2)
    text = font.render('Slot 2', True, Black)
    screen.blit(text, (slot2.x + 5, slot2.y + 5))

    slot3 = pygame.Rect(180, 60, 50, 30)
    pygame.draw.rect(screen, White, slot3)
    text = font.render('Slot 3', True, Black)
    screen.blit(text, (slot3.x + 5, slot3.y + 5))

    cancel = pygame.Rect(120, 110, 50, 30)
    pygame.draw.rect(screen, White, cancel)
    text = font.render('Cancel', True, Black)
    screen.blit(text, (cancel.x + 5, cancel.y + 5))
    
    pygame.display.update()

    while saveSlot == 0:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cancel.collidepoint(event.pos):
                    return 0
                if slot1.collidepoint(event.pos):
                    saveSlot = 1
                if slot2.collidepoint(event.pos):
                    saveSlot = 2
                if slot3.collidepoint(event.pos):
                    saveSlot = 3

    if saveSlot == 1:
        file = open('{}/Save1.txt'.format(os.getcwd()), 'w')
    elif saveSlot == 2:
        file = open('{}/Save2.txt'.format(os.getcwd()), 'w')
    elif saveSlot == 3:
        file = open('{}/Save3.txt'.format(os.getcwd()), 'w')

    save = board
    for i in range(settings['width']):
        for j in range(settings['height']):
            tile = board[i][j]
            pos = ((tile.pos[0] - 50) / 25, (tile.pos[1] - 50) / 25)
            save[i][j] = [tile.opened, tile.flagged, pos, tile.num]
    file.writelines([json.dumps(settings) + '\n', f'{numLeft}\n', json.dumps(save)])
    file.close()
    return 1

def DrawBoard(menuButton, saveButton):
    screen.fill(Black)
    for i in range(settings['width']):
        for j in range(settings['height']):
            board[i][j].Draw()
    pygame.draw.rect(screen, DarkGrey, (menuButton.x - 2, menuButton.y - 2,
                                        menuButton.width + 4, menuButton.height + 4))
    pygame.draw.rect(screen, Grey, menuButton)
    menuText = fontSet.render('Menu', True, White)
    screen.blit(menuText, (menuButton.x + 10, menuButton.y + 5))

    pygame.draw.rect(screen, DarkGrey, (saveButton.x - 2, saveButton.y - 2,
                                        saveButton.width + 4, saveButton.height + 4))
    pygame.draw.rect(screen, Grey, saveButton)
    saveText = fontSet.render('Save', True, White)
    screen.blit(saveText, (saveButton.x + 25, saveButton.y + 5))
    pygame.display.update()

def OpenArea(x, y, num):
    for i in range(3): 
        for j in range(3):
            if i == 1 and j == 1:
                continue
            else:
                try:
                    if x+i > 0 and y+j > 0:
                        if board[x+i-1][y+j-1].num == 0:
                            if board[x+i-1][y+j-1].opened == False:
                                board[x+i-1][y+j-1].opened = True
                                num -= 1
                                num = OpenArea(x+i-1, y+j-1, num)
                        else:
                            if board[x+i-1][y+j-1].opened == False:
                                num -= 1
                                board[x+i-1][y+j-1].opened = True
                except:
                    continue
    return num

def DrawSettings(buttons, selected, screen, sliders):
    screen.fill(Black)
    text = fontSet.render('Choose a difficulty', True, White)
    screen.blit(text, (400, 50))
    
    pygame.draw.rect(screen, DarkGrey, (buttons[0].x - 2, buttons[0].y - 2,
                                        buttons[0].width + 4, buttons[0].height + 4))
    pygame.draw.rect(screen, Grey, buttons[0])
    pygame.draw.rect(screen, DarkGrey, (buttons[1].x - 2, buttons[1].y - 2,
                                        buttons[1].width + 4, buttons[1].height + 4))
    pygame.draw.rect(screen, Grey, buttons[1])
    pygame.draw.rect(screen, DarkGrey, (buttons[2].x - 2, buttons[2].y - 2,
                                        buttons[2].width + 4, buttons[2].height + 4))
    pygame.draw.rect(screen, Grey, buttons[2])
    pygame.draw.rect(screen, DarkGrey, (buttons[3].x - 2, buttons[3].y - 2,
                                        buttons[3].width + 4, buttons[3].height + 4))
    pygame.draw.rect(screen, Grey, buttons[3])

    if selected != 0:
        pygame.draw.rect(screen, DarkGreen, (selected.x - 2, selected.y - 2,
                                             selected.width + 4, selected.height + 4))
        pygame.draw.rect(screen, Green, selected)
    
    pygame.draw.line(screen, White, (0, 398), (1000, 398), 4)
    
    pygame.draw.rect(screen, DarkGrey, (buttons[4].x - 2, buttons[4].y - 2,
                                        buttons[4].width + 4, buttons[4].height + 4))
    pygame.draw.rect(screen, Grey, buttons[4])

    easyText = fontSet.render('Easy', True, White)
    screen.blit(easyText, (buttons[0].x + 50, buttons[0].y + 10))
    mediumText = fontSet.render('Medium', True, White)
    screen.blit(mediumText, (buttons[1].x + 35, buttons[1].y + 10))
    hardText = fontSet.render('Hard', True, White)
    screen.blit(hardText, (buttons[2].x + 50, buttons[2].y + 10))
    expertText = fontSet.render('Expert', True, White)
    screen.blit(expertText, (buttons[3].x + 40, buttons[3].y + 10))
    backText = fontSet.render('Back', True, White)
    screen.blit(backText, (buttons[4].x + 20, buttons[4].y + 10))
    text1 = fontSet.render('Or create a custom game', True, White)
    screen.blit(text1, (375, 425))
    widthText = fontSet.render('Width:', True, White)
    screen.blit(widthText, (100, 510))
    heightText = fontSet.render('Height:', True, White)
    screen.blit(heightText, (100, 585))
    bombsText = fontSet.render('Bombs:', True, White)
    screen.blit(bombsText, (100, 660))

    pygame.draw.line(screen, White, (200, 525), (800, 525), 10)
    pygame.draw.circle(screen, DarkGrey, (sliders[0], 525), 15)
    pygame.draw.line(screen, White, (200, 600), (800, 600), 10)
    pygame.draw.circle(screen, DarkGrey, (sliders[1], 600), 15)
    pygame.draw.line(screen, White, (200, 675), (800, 675), 10)
    pygame.draw.circle(screen, DarkGrey, (sliders[2], 675), 15)

    width = sliders[0] - 200
    width = width / 600
    width = int(width * 47) + 3
    widthText = fontSet.render('{}'.format(width), True, White)
    screen.blit(widthText, (900, 510))
    height = sliders[1] - 200
    height = height / 600
    height = int(height * 47) + 3
    heightText = fontSet.render('{}'.format(height), True, White)
    screen.blit(heightText, (900, 585))
    bombs = sliders[2] - 200
    bombs = bombs / 600
    bMax = int((width * height) / 1.5)
    bMin = int((width * height) / 50)
    if bMin < 1:
        bMin = 1
    bombs = int(bombs * (bMax - bMin) + bMin)
    bombsText = fontSet.render('{}'.format(bombs), True, White)
    screen.blit(bombsText, (900, 660))
    
    pygame.display.update()

def Menu():
    global gameState
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Menu')
    screen.fill(Black)
    text = fontBig.render('MINESWEEPER', True, White)
    screen.blit(text, (100, 50))
    playButton = pygame.Rect(175, 150, 150, 50)
    pygame.draw.rect(screen, DarkGrey, (playButton.x - 2, playButton.y - 2,
                                        playButton.width + 4, playButton.height + 4))
    pygame.draw.rect(screen, Grey, playButton)
    settingsButton = pygame.Rect(175, 250, 150, 50)
    pygame.draw.rect(screen, DarkGrey, (settingsButton.x - 2, settingsButton.y - 2,
                                        settingsButton.width + 4, settingsButton.height + 4))
    pygame.draw.rect(screen, Grey, settingsButton)
    quitButton = pygame.Rect(175, 350, 150, 50)
    pygame.draw.rect(screen, DarkGrey, (quitButton.x - 2, quitButton.y - 2,
                                        quitButton.width + 4, quitButton.height + 4))
    pygame.draw.rect(screen, Grey, quitButton)
    text1 = fontBig.render('Play', True, White)
    text2 = fontBig.render('Settings', True, White)
    text3 = fontBig.render('Quit', True, White)
    screen.blit(text1, (playButton.x + 40, playButton.y + 5))
    screen.blit(text2, (settingsButton.x + 10, settingsButton.y + 5))
    screen.blit(text3, (quitButton.x + 40, quitButton.y + 5))
    pygame.display.update()
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if playButton.collidepoint(event.pos):
                        menu = False
                        gameState = 'Setup'
                    elif settingsButton.collidepoint(event.pos):
                        menu = False
                        gameState = 'Settings'
                    elif quitButton.collidepoint(event.pos):
                        menu = False
                        gameState = 'Quit'
    pygame.display.quit()

def Settings():
    global gameState
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('Settings')

    easyButton = pygame.Rect(50, 200, 150, 50)
    mediumButton = pygame.Rect(300, 200, 150, 50)
    hardButton = pygame.Rect(550, 200, 150, 50)
    expertButton = pygame.Rect(800, 200, 150, 50)
    backButton = pygame.Rect(10, 740, 100, 50)
    selected = 0
    buttons = [easyButton, mediumButton, hardButton, expertButton, backButton]

    slide1 = False
    slide2 = False
    slide3 = False
    sliders = [500, 500, 500]
    edit = True
    while edit:
        DrawSettings(buttons, selected, screen, sliders)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if slide1 == False and slide2 == False and slide3 == False:
                        if easyButton.collidepoint(event.pos):
                            settings['width'] = 9
                            settings['height'] = 9
                            settings['bombs'] = 10
                            selected = easyButton
                        elif mediumButton.collidepoint(event.pos):
                            settings['width'] = 16
                            settings['height'] = 16
                            settings['bombs'] = 40
                            selected = mediumButton
                        elif hardButton.collidepoint(event.pos):
                            settings['width'] = 30
                            settings['height'] = 16
                            settings['bombs'] = 99
                            selected = hardButton
                        elif expertButton.collidepoint(event.pos):
                            settings['width'] = 30
                            settings['height'] = 30
                            settings['bombs'] = 200
                            selected = expertButton
                        elif backButton.collidepoint(event.pos):
                            edit = False
                            gameState = 'Menu'
                            file = open('{}/Settings.txt'.format(os.getcwd()), 'w')
                            file.write(json.dumps(settings))
                            file.close()
                        elif abs(event.pos[0] - sliders[0]) <= 15 and abs(event.pos[1] - 525) <= 15:
                            slide1 = True
                            selected = 0
                        elif abs(event.pos[0] - sliders[1]) <= 15 and abs(event.pos[1] - 600) <= 15:
                            slide2 = True
                            selected = 0
                        elif abs(event.pos[0] - sliders[2]) <= 15 and abs(event.pos[1] - 675) <= 15:
                            slide3 = True
                            selected = 0
                    else:
                        if slide1 == True:
                            slide1 = False
                        elif slide2 == True:
                            slide2 = False
                        elif slide3 == True:
                            slide3 = False
            elif event.type == pygame.MOUSEMOTION:
                if slide1 == True:
                    sliders[0] = event.pos[0]
                elif slide2 == True:
                    sliders[1] = event.pos[0]
                elif slide3 == True:
                    sliders[2] = event.pos[0]
                for x in range(len(sliders)):
                    if sliders[x] < 200:
                        sliders[x] = 200
                    if sliders[x] > 800:
                        sliders[x] = 800
                if slide1 == True or slide2 == True or slide3 == True:
                    width = sliders[0] - 200
                    width = width / 600
                    width = int(width * 47) + 3
                    settings['width'] = width
                    height = sliders[1] - 200
                    height = height / 600
                    height = int(height * 47) + 3
                    settings['height'] = height
                    bombs = sliders[2] - 200
                    bombs = bombs / 600
                    bMax = int((width * height) / 1.5)
                    bMin = int((width * height) / 50)
                    if bMin < 1:
                        bMin = 1
                    bombs = int(bombs * (bMax - bMin) + bMin)
                    settings['bombs'] = bombs

def Setup():
    global board, gameState, screen
    width, height = settings['width'], settings['height']
    screen = pygame.display.set_mode((width * 25 + 200, height * 25 + 200))
    pygame.display.set_caption('Minesweeper')
    board = [[0 for i in range(height)] for j in range(width)]
    tiles = []
    for i in range(width):
        for j in range(height):
            tile = Tile(0, (i, j))
            board[i][j] = tile
            tiles.append(tile)
    for i in range(settings['bombs']):
        bomb = random.choice(tiles)
        bomb.num = -1
        tiles.remove(bomb)
    for i in range(width):
        for j in range(height):
            if board[i][j].num == 0:
                bombs = 0
                for k in range(3):
                    for l in range(3):
                        try:
                            if i+k > 0 and j+l > 0:
                                if board[i+k-1][j+l-1].num == -1:
                                    bombs += 1
                        except:
                            continue
                board[i][j].num = bombs
    DrawBoard(pygame.Rect(50, height * 25 + 125, 100, 50), pygame.Rect(175, height * 25 + 125, 100, 50))
    gameState = 'Game'

def Game(numLeft = settings['width']*settings['height']):
    global gameState
    width, height = settings['width'], settings['height']
    menuButton = pygame.Rect(50, height * 25 + 125, 100, 50)
    saveButton = pygame.Rect(175, height * 25 + 125, 100, 50)
    time.sleep(0.5)
    pygame.event.clear()
    game = True
    while game:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(width):
                        for j in range(height):
                            if board[i][j].button.collidepoint(event.pos) and board[i][j].flagged == False:
                                board[i][j].opened = True
                                numLeft -= 1
                                if board[i][j].num == -1:
                                    game = False
                                    gameState = 'Lose'
                                elif board[i][j].num == 0:
                                    numLeft = OpenArea(i, j, numLeft)
                                elif numLeft == settings['bombs']:
                                    game = False
                                    gameState = 'Win'
                    if menuButton.collidepoint(event.pos):
                        game = False
                        gameState = 'Menu'
                    if saveButton.collidepoint(event.pos):
                        if(SaveGame(numLeft) == 1):
                            game = False
                            gameState = 'Menu'

                elif event.button == 3:
                    for i in range(width):
                        for j in range(height):
                            if board[i][j].button.collidepoint(event.pos):
                                if board[i][j].opened == False:
                                    if board[i][j].flagged:
                                        board[i][j].flagged = False
                                    else:
                                        board[i][j].flagged = True
        if gameState != 'Menu':
            DrawBoard(menuButton, saveButton)

def Win():
    global gameState
    winText = fontSet.render('You win!', True, Green)
    screen.blit(winText, (settings['width'] * 25 + 75, settings['height'] * 25 / 2))
    pygame.display.update()
    menuButton = pygame.Rect(50, settings['height'] * 25 + 125, 100, 50)
    while gameState == 'Win':
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menuButton.collidepoint(event.pos):
                    gameState = 'Menu'

def Lose():
    global gameState
    loseText = fontSet.render('You lose!', True, Red)
    screen.blit(loseText, (settings['width'] * 25 + 75, settings['height'] * 25 / 2))
    pygame.display.update()
    menuButton = pygame.Rect(50, settings['height'] * 25 + 125, 100, 50)
    while gameState == 'Lose':
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menuButton.collidepoint(event.pos):
                    gameState = 'Menu'

def Main():
    main = True
    while main:
        if gameState == 'Menu':
            Menu()
        if gameState == 'Settings':
            Settings()
        if gameState == 'Setup':
            Setup()
        if gameState == 'Game':
            Game()
        if gameState == 'Win':
            Win()
        if gameState == 'Lose':
            Lose()
        if gameState == 'Quit':
            main = False
            pygame.quit()

Main()
