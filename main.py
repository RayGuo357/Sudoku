import pygame
import math

pygame.font.init()

window = pygame.display.set_mode((600, 600))

tileSize = 600 / 9
adjustX = tileSize / 3
adjustY = tileSize / 6
tileColor = (255, 60, 60)

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

rectGroup = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

selectedMouseX = 0
selectedMouseY = 0

def draw():
    window.blit(pygame.font.SysFont("comicsans", 40).render("Test", 1, (255, 255, 255)), (20, 570)) 
    for i in range(9):
        for j in range(9):
            if j == selectedMouseY and i == selectedMouseX:
                rectGroup[j][i] = pygame.draw.rect(window, (0, 0, 0), (i * tileSize, j * tileSize, tileSize, tileSize))
            else:
                rectGroup[j][i] = pygame.draw.rect(window, tileColor, (i * tileSize, j * tileSize, tileSize, tileSize))
            
            if grid[j][i] != 0:
                window.blit(pygame.font.SysFont("TimesRoman", 40). render(str(grid[j][i]), 1, (255, 255, 255)), ((i * tileSize) + adjustX, (j * tileSize) + adjustY))
            
    for i in range(8):
        if (i + 1) % 3 != 0: 
            pygame.draw.line(window, (255, 255, 255), ((i + 1) * tileSize, 0), ((i + 1) * tileSize, 600))
            pygame.draw.line(window, (255, 255, 255), (0, (i + 1) * tileSize), (600, (i + 1) * tileSize))
        else: 
            pygame.draw.line(window, (255, 255, 255), ((i + 1) * tileSize, 0), ((i + 1) * tileSize, 600), 4)
            pygame.draw.line(window, (255, 255, 255), (0, (i + 1) * tileSize), (600, (i + 1) * tileSize), 4)

run = True

while run:
    window.fill((60, 60, 60))
    
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            selectedMouseX = math.floor(pygame.mouse.get_pos()[0] / tileSize)
            selectedMouseY = math.floor(pygame.mouse.get_pos()[1] / tileSize)

            rectGroup[selectedMouseY][selectedMouseX].inflate(2, 2)
            grid[selectedMouseY][selectedMouseX] = (grid[selectedMouseY][selectedMouseX] + 1) % 10
            print("Selected tile: " + "(" + str(selectedMouseX) + ", " + str(selectedMouseY) + ")")
        if e.type == pygame.QUIT:
            run = False
    
    draw()


    pygame.display.update()

pygame.quit()