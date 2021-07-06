import pygame
import math
import requests


pygame.font.init()

window = pygame.display.set_mode((600, 600))

tileSize = 600 / 9
adjustX = tileSize / 3
adjustY = tileSize / 6
tileColor = (255, 60, 70)

pygame.display.set_caption("Sudoku")

grid = [
    [0, 0, 0, 8, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 4, 5, 0, 0, 0],
    [2, 0, 4, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 9, 0, 0, 0, 0, 1],
    [0, 3, 0, 0, 5, 0, 6, 0, 0],
    [5, 0, 0, 6, 0, 0, 8, 2, 0],
    [0, 0, 5, 0, 0, 0, 9, 0, 0],
    [0, 6, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 0, 0, 7, 4]
]

answer = [
    [0, 0, 0, 8, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 4, 5, 0, 0, 0],
    [2, 0, 4, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 9, 0, 0, 0, 0, 1],
    [0, 3, 0, 0, 5, 0, 6, 0, 0],
    [5, 0, 0, 6, 0, 0, 8, 2, 0],
    [0, 0, 5, 0, 0, 0, 9, 0, 0],
    [0, 6, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 0, 0, 7, 4]
]

defaultNumbers = [
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False]
]

selectedMouseX = 0
selectedMouseY = 0

def clearGrid():
    for i in range(9):
        for j in range(9):
            grid[i][j] = 0
            defaultNumbers[i][j] = False

def initBoardNumbers():
    for i in range(9):
        for j in range(9):
            if grid[j][i] != 0:
                defaultNumbers[j][i] = True

def draw(): 
    for i in range(9):
        for j in range(9):
            if j == selectedMouseY and i == selectedMouseX:
                pygame.draw.rect(window, (50, 50, 50), (i * tileSize, j * tileSize, tileSize, tileSize))
            else:
                pygame.draw.rect(window, tileColor, (i * tileSize, j * tileSize, tileSize, tileSize))
            
            if grid[j][i] != 0:
                if defaultNumbers[j][i]:
                    window.blit(pygame.font.SysFont("TimesRoman", 40, True). render(str(grid[j][i]), 1, (200, 200, 200)), ((i * tileSize) + adjustX, (j * tileSize) + adjustY))
                else:
                    window.blit(pygame.font.SysFont("TimesRoman", 40). render(str(grid[j][i]), 1, (255, 255, 255)), ((i * tileSize) + adjustX, (j * tileSize) + adjustY))
            
    for i in range(8):
        if (i + 1) % 3 != 0: 
            pygame.draw.line(window, (255, 255, 255), ((i + 1) * tileSize, 0), ((i + 1) * tileSize, 600))
            pygame.draw.line(window, (255, 255, 255), (0, (i + 1) * tileSize), (600, (i + 1) * tileSize))
        else: 
            pygame.draw.line(window, (255, 255, 255), ((i + 1) * tileSize, 0), ((i + 1) * tileSize, 600), 4)
            pygame.draw.line(window, (255, 255, 255), (0, (i + 1) * tileSize), (600, (i + 1) * tileSize), 4)


def emptyLocations(answer, row_col):
    for row in range(9):
        for col in range(9):
            if answer[row][col] == 0:
                row_col[0] = row
                row_col[1] = col
                return True
    return False

def inRow(answer, row, x):
    for i in range(9):
        if answer[row][i] == x:
            return True
    return False

def inColumn(answer, col, x):
    for i in range(9):
        if answer[i][col] == x:
            return True
    return False

def inBox(answer, row, col, x):
    for i in range(3):
        for j in range(3):
            if answer[i + row][j + col] == x:
                return True
    return False

def checkSafe(answer, row, col, x):
    return not inRow(answer, row, x) and not inColumn(answer, col, x) and not inBox(answer, row - row % 3, col - col % 3, x)

def solver(answer):
    row_col = [0, 0]
    if not emptyLocations(answer, row_col):
        return True

    for x in range(1, 10):
        if checkSafe(answer, row_col[0], row_col[1], x):
            answer[row_col[0]][row_col[1]] = x
            if solver(answer):
                return True
            answer[row_col[0]][row_col[1]] = 0

    return False

def generateNewBoard(difficulty=1):
    response = requests.get("http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&level=" + str(difficulty))

    clearGrid()
    for tile in response.json()['squares']:
        grid[tile['y']][tile['x']] = tile['value']

    for i in range(9):
        for j in range(9):
            answer[i][j] = grid[i][j]
    if solver(answer):
        run = True
    else:
        run = False

    initBoardNumbers()
    return run

run = generateNewBoard()

while run:
    window.fill((255, 255, 255))
    
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            selectedMouseX = math.floor(pygame.mouse.get_pos()[0] / tileSize)
            selectedMouseY = math.floor(pygame.mouse.get_pos()[1] / tileSize)

            print("Selected tile: " + "(" + str(selectedMouseX) + ", " + str(selectedMouseY) + ")")
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w or e.key ==pygame.K_UP:
                selectedMouseY = (selectedMouseY - 1) % 9
            if e.key == pygame.K_a or e.key ==pygame.K_LEFT:
                selectedMouseX = (selectedMouseX - 1) % 9
            if e.key == pygame.K_s or e.key ==pygame.K_DOWN:
                selectedMouseY = (selectedMouseY + 1) % 9
            if e.key == pygame.K_d or e.key ==pygame.K_RIGHT:
                selectedMouseX = (selectedMouseX + 1) % 9
            if not defaultNumbers[selectedMouseY][selectedMouseX]:
                if e.key == pygame.K_0 or e.key == pygame.K_KP0:
                    grid[selectedMouseY][selectedMouseX] = 0
                if e.key == pygame.K_1 or e.key == pygame.K_KP1:
                    grid[selectedMouseY][selectedMouseX] = 1
                if e.key == pygame.K_2 or e.key == pygame.K_KP2:
                    grid[selectedMouseY][selectedMouseX] = 2
                if e.key == pygame.K_3 or e.key == pygame.K_KP3:
                    grid[selectedMouseY][selectedMouseX] = 3
                if e.key == pygame.K_4 or e.key == pygame.K_KP4:
                    grid[selectedMouseY][selectedMouseX] = 4
                if e.key == pygame.K_5 or e.key == pygame.K_KP5:
                    grid[selectedMouseY][selectedMouseX] = 5
                if e.key == pygame.K_6 or e.key == pygame.K_KP6:
                    grid[selectedMouseY][selectedMouseX] = 6
                if e.key == pygame.K_7 or e.key == pygame.K_KP7:
                    grid[selectedMouseY][selectedMouseX] = 7
                if e.key == pygame.K_8 or e.key == pygame.K_KP8:
                    grid[selectedMouseY][selectedMouseX] = 8
                if e.key == pygame.K_9 or e.key == pygame.K_KP9:
                    grid[selectedMouseY][selectedMouseX] = 9
            if e.key == pygame.K_RETURN:
                for i in range(9):
                    for j in range(9):
                        grid[i][j] = answer[i][j]
                print(answer)
            if e.key == pygame.K_SPACE:
                run = generateNewBoard()
        if e.type == pygame.QUIT:
            run = False
    
    draw()
    pygame.display.update()

    if answer == grid:

        window.blit(pygame.font.SysFont("comicsans", 40).render("Test", 1, (255, 255, 255)), (20, 570))

pygame.quit()