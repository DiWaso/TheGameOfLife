import pygame, sys
from pygame.locals import *
pygame.init()

WIDTH = 450
HEIGHT = 550
GAME_HEIGHT = HEIGHT - 100
FPS = 60
clock = pygame.time.Clock()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Game of Life")

cell_size = WIDTH // 10
margin = 5

# Colors
BLUE = (55,96,255)
GRAY = (180, 180, 180)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (120, 120, 120)

# Font
font = pygame.font.SysFont("Roboto", 36)

# Images
next_icon = pygame.transform.scale(pygame.image.load("./images/next.png"), (35, 35))

play_icon = pygame.transform.scale(pygame.image.load("./images/play.png"), (35, 35))

clear_icon = pygame.transform.scale(pygame.image.load("./images/clear.png"), (35, 35))

stop_icon = pygame.transform.scale(pygame.image.load("./images/stop.png"), (35, 35))

class WorldMap:
    def __init__(self):
        self.map = [[0 for _ in range(int(WIDTH*1.2) // cell_size)] for _ in range(HEIGHT // cell_size)]
        self.generations = 0

    def checkGrid(self):
        temp_map = [row[:] for row in self.map]

        for index_row, row in enumerate(self.map):
            for index_col, column in enumerate(row):
                alive_neighbours = 0

                for i in range(-1, 2):
                    for j in range(-1, 2):
                        neighbor_row = index_row + i
                        neighbor_col = index_col + j
                        if (0 <= neighbor_row < len(self.map) and 0 <= neighbor_col < len(self.map[0])) and (i != 0 or j != 0):
                            if self.map[neighbor_row][neighbor_col] == "x":
                                alive_neighbours += 1

                if column == "x":
                    if alive_neighbours < 2 or alive_neighbours > 3:
                        temp_map[index_row][index_col] = 0
                elif column == 0:
                    if alive_neighbours == 3:
                        temp_map[index_row][index_col] = "x"

        self.map = temp_map
        self.generations += 1

    def drawMap(self):
        for index_row, row in enumerate(self.map):
            for index_col, col in enumerate(row):
                if col == 0:
                    pygame.draw.rect(win, GRAY, (index_col * cell_size, index_row * cell_size, cell_size, cell_size))
                elif col == "x":
                    pygame.draw.rect(win, YELLOW, (index_col * cell_size, index_row * cell_size, cell_size, cell_size))

                pygame.draw.rect(win, LIGHT_GRAY, (index_col * cell_size, index_row * cell_size, cell_size, cell_size), 1)

    def userDraw(self, mouse):
        x, y = mouse
        # Removed click initialization here

        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            if y < GAME_HEIGHT:
                if self.map[y // cell_size][x // cell_size] == "x":
                    self.map[y // cell_size][x // cell_size] = 0
                else:
                    self.map[y // cell_size][x // cell_size] = "x"

        pygame.time.wait(135)

    def autoPlay(self, menuObject, mapMenuObject):

        stop_button = Rect(135 + margin*4.5, GAME_HEIGHT + margin*5, 135, 45)
        stop_text = font.render("Stop", True, (255, 255, 255))

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and stop_button.collidepoint(event.pos):
                    run = False

            self.checkGrid()
            self.drawMap()
            mapMenuObject.drawMapMenu()

            menuObject.drawMenu()
            
            pygame.draw.rect(win, BLUE, stop_button, border_radius=10)

            win.blit(stop_icon, (135 + margin*6, GAME_HEIGHT + 5 + margin*5))
            win.blit(stop_text, (185 + margin*6, GAME_HEIGHT + 10 + margin*5))

            pygame.display.update()
            pygame.time.wait(600)

class Menu:
    def __init__(self):
        self.rect = Rect(0, GAME_HEIGHT, WIDTH, HEIGHT - GAME_HEIGHT)

    def drawMenu(self):
        pygame.draw.rect(win, DARK_GRAY, self.rect)

        clear_button = Rect(margin, GAME_HEIGHT + margin*5, 135, 45)
        clear_text = font.render("Clear", True, (255, 255, 255)) 

        play_button = Rect(135 + margin*4.5, GAME_HEIGHT + margin*5, 135, 45)
        play_text = font.render("Play", True, (255, 255, 255))

        next_button = Rect(WIDTH - 135 - margin, GAME_HEIGHT + margin*5, 135, 45)
        next_text = font.render("Next", True, (255, 255, 255))
        
        pygame.draw.rect(win, BLUE, next_button, border_radius=10)
        pygame.draw.rect(win, BLUE, play_button, border_radius=10)
        pygame.draw.rect(win, BLUE, clear_button, border_radius=10)

        win.blit(clear_icon, (margin*3, GAME_HEIGHT + 5 + margin*5))
        win.blit(clear_text, (45 + margin*3, GAME_HEIGHT + 10 + margin*5))

        win.blit(play_icon, (135 + margin*6, GAME_HEIGHT + 5 + margin*5))
        win.blit(play_text, (185 + margin*6, GAME_HEIGHT + 10 + margin*5))

        win.blit(next_icon, (WIDTH - 135, GAME_HEIGHT + 5 + margin*5))
        win.blit(next_text, (320 + margin * 7, GAME_HEIGHT + 10 + margin*5))

        return [clear_button, play_button, next_button]
    
    def menuFunctions(self, menuObjects, mapMenuObject, mouse):
        clear_button = menuObjects[0]
        play_button = menuObjects[1]
        next_button = menuObjects[2]

        click = pygame.mouse.get_pressed()

        if click[0] == 1:
            if clear_button.collidepoint(mouse):
                playGrid.map = [[0 for _ in range(int(WIDTH*1.2) // cell_size)] for _ in range(HEIGHT // cell_size)]
                playGrid.generations = 0
            elif next_button.collidepoint(mouse):
                playGrid.checkGrid()
            elif play_button.collidepoint(mouse):
                playGrid.autoPlay(self, mapMenuObject)

class mapMenu:
    def __init__(self):
        self.surface = pygame.Surface((cell_size*4, cell_size*3))

    def drawMapMenu(self):
        self.surface.set_alpha(180)
        self.surface.fill(DARK_GRAY)
        win.blit(self.surface, (WIDTH - cell_size*4 - margin, GAME_HEIGHT - cell_size*3 - margin))

        gen_text = font.render(str(playGrid.generations), True, (0, 0, 0))
        win.blit(gen_text, (WIDTH - 100, GAME_HEIGHT - 50))

        pygame.display.update()

playGrid = WorldMap()
gameMenu = Menu()
gameMapMenu = mapMenu()

def main():
    run = True

    while run:
        clock.tick(FPS)
        mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        playGrid.drawMap()
        playGrid.userDraw(mouse)
        
        gameMenu.menuFunctions(gameMenu.drawMenu(), gameMapMenu, mouse)

        gameMapMenu.drawMapMenu()

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
