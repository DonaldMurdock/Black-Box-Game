#Donald Taylor
#8/18/2020
#GUI for the Black Box Game

import BlackBoxGame
import pygame
import sys
import random

white = 255,255,255
black = 0,0,0
red = 255,0,0
green = 0,200,0

class BlackBoxUI:
    """User Interface for the Black Box Game.
    Has attributes for the screen Surface object, the game BlackBoxGame object, and a list of rect objects.
    """

    def __init__(self):
        """Initializes UI attributes and sets up the display for the game.
        """

        pygame.init()
        self._screen = pygame.display.set_mode((1000, 600))     #_screen is a surface object
        self._game = self.game_init()                           #_game is a BlackBoxGame object

        self._rects = []
        # after setup _rects[0] = New Game Button Rect
        #             _rects[1] = Quit Button Rect
        #             _rects[2] = Atoms Text Rect


        self.set_up_display()

    def game_init(self):
        """Creates the BlackBoxGame object with 4 random atom locations. Returns the object.
        """
        atom_list = []

        #Generate 4 random coordinates
        for i in range(4):
            row = random.randint(1,8)
            col = random.randint(1,8)
            while (row, col) in atom_list:                #Avoid random duplicates
                row = random.randint(1, 8)
                col = random.randint(1, 8)

            atom_list.append((row,col))

        game = BlackBoxGame.BlackBoxGame(atom_list)
        return game

    def set_up_display(self):
        """Displays the game.
        """
        self._screen.fill(white)
        self.display_title()
        self._rects.append(self.display_new_game_button())      #Add new game button rect to rects list
        self._rects.append(self.display_quit_button())          #Add quit button rect to rects list
        self.display_score()
        self._rects.append(self.display_atoms_left())           #Add atoms text rect to rects list
        self.display_game_board()
        pygame.display.flip()

    def display_title(self):
        """Displays 'Black Box Game' Title
        """
        title = pygame.image.load("images/Black Box Title.png")          #title is a Surface object
        self._screen.blit(title, (15,10))

    def display_new_game_button(self):
        """Creates the new game button and returns the associated rectangle
        """
        newGameButton = pygame.image.load("images/New Game Button.png")
        self._screen.blit(newGameButton, (15,450))
        return newGameButton.get_rect(topleft=(15, 450))

    def display_quit_button(self):
        """Creates the quit button and returns the associated rectangle
        """
        quitButton = pygame.image.load("images/Quit Button.png")
        self._screen.blit(quitButton, (205, 450))
        return quitButton.get_rect(topleft=(205, 450))


    def display_score(self):
        """Displays the current score
        """

        font = pygame.font.Font('freesansbold.ttf', 50)
        scoreText = font.render('Score: ' + str(self._game.get_score()), True, black, white)
        scoreTextRect = scoreText.get_rect()
        scoreTextRect.topleft = (52, 125)
        scoreTextRect.inflate_ip(40, 0)           #stretching the rect out so the text gets covered when it changes
        pygame.draw.rect(self._screen, white, scoreTextRect)
        self._screen.blit(scoreText, scoreTextRect)

    def display_atoms_left(self):
        """Displays the number of remaining atoms
        """
        font = pygame.font.Font('freesansbold.ttf', 50)
        atomsText = font.render('Atoms Left: ' + str(self._game.atoms_left()), True, black, white)
        atomsTextRect = atomsText.get_rect()
        atomsTextRect.topleft = (48, 185)
        atomsTextRect.inflate_ip(40, 0)           #stretching the rect out so the text gets covered when it changes
        pygame.draw.rect(self._screen, white, atomsTextRect)
        self._screen.blit(atomsText, atomsTextRect)
        return atomsTextRect

    def display_game_board(self):
        """Displays the game_board
        """
        self.draw_grid()
        self.erase_corners()
        self.draw_black_box()
        self.draw_black_box_grid()

    def draw_grid(self):
        """Draws the initial grid
        """

        gameBoardRect = pygame.Rect(400, 50, 500, 500)  #create game board rectangle
        pygame.draw.rect(self._screen, black, gameBoardRect, 2)  #draw game board (2 is width of line)

        #Draw each line to create the grid
        for x in range(10):
            x_coord = 400 + x * 50
            pygame.draw.line(self._screen, black, (x_coord, 50), (x_coord, 550), 2)
        for y in range(2, 11):
            y_coord = 50 * y
            pygame.draw.line(self._screen, black, (400, y_coord), (900, y_coord), 2)

    def erase_corners(self):
        """Erases the corner squares.
        """

        # top left
        pygame.draw.line(self._screen, white, (400, 50), (449, 50), 2)
        pygame.draw.line(self._screen, white, (400, 50), (400, 99), 2)

        # bottom left
        pygame.draw.line(self._screen, white, (400, 502), (400, 550), 2)
        pygame.draw.line(self._screen, white, (400, 549), (449, 549), 2)

        # top right
        pygame.draw.line(self._screen, white, (852, 50), (900, 50), 2)
        pygame.draw.line(self._screen, white, (899, 50), (899, 99), 2)

        # bottom right
        pygame.draw.line(self._screen, white, (852, 549), (900, 549), 2)
        pygame.draw.line(self._screen, white, (899, 502), (899, 550), 2)

    def draw_black_box(self):
        """Draws the black box inside the game board
        """
        blackBoxRect = pygame.Rect(450, 100, 400, 400)  # create black box rectangle
        pygame.draw.rect(self._screen, black, blackBoxRect)  # draw black box (2 is width of line)

    def draw_black_box_grid(self):
        """Draws the black box grid
        """

        #Draw each line to create the grid
        for x in range(2, 9):
            x_coord = 400 + x * 50
            pygame.draw.line(self._screen, white, (x_coord, 100), (x_coord, 500), 2)
        for y in range(3, 10):
            y_coord = 50 * y
            pygame.draw.line(self._screen, white, (450, y_coord), (850, y_coord), 2)


    def random_color(self):
        """Returns a random color
        """
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)

        color = (r,g,b)
        return color

    def get_square(self, pos):
        """Takes a position tuple as a parameter and returns the associated game square coordinate.
        """

        x_coord = pos[0]
        y_coord = pos[1]
        row = None
        col = None

        #Find row
        for i in range(10):
            if y_coord >= 50 * (i + 1) and y_coord < 50 * (i + 2):
                row = i

        #Find column
        for i in range(10):
            if x_coord >= 50 * (i + 8) and x_coord < 50 * (i + 9):
                col = i

        #If the coordinate is not on the game board
        if row is None or col is None:
            return (None, None)
        else:
            return (row, col)

    def draw_circle(self, grid_coord, color):
        """Takes a game board coordinate tuple and color as parameters. Draws a circle of the given color in
        the given game square.
        """
        row = grid_coord[0]
        col = grid_coord[1]

        #Find the center of the square
        x_coord = 425 + (50 * col)
        y_coord = 75 + (50 * row)

        #White circles are black outlines of circles
        if color == white:
            pygame.draw.circle(self._screen, black, (x_coord, y_coord), 20, 2)
        else:
            pygame.draw.circle(self._screen, color, (x_coord, y_coord), 20)

    def draw_x(self, grid_coord, color):
        """Takes a game board coordinate tuple and color as parameters. Draws an X of the given color in
        the given game square
        """
        row = grid_coord[0]
        col = grid_coord[1]

        #Find the top left corner of the game square
        x_coord = 400 + (col * 50)
        y_coord = 50 + (row * 50)
        pygame.draw.line(self._screen, color, (x_coord + 2, y_coord + 2), (x_coord + 48, y_coord + 48), 2)

        #Top right corner
        x_coord = 450 + (col * 50)
        pygame.draw.line(self._screen, color, (x_coord - 2, y_coord + 2), (x_coord - 48, y_coord + 48), 2)


    def play_game(self):
        """Runs the game
        """

        playing = True                  #Used for our loop. Game will end when playing == False
        game_status = 'ACTIVE'          #When game_status != 'Active' only the new game and quit buttons will do anything.

        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:      #Get each mouse click

                    if self._rects[1].collidepoint(event.pos):        #Quit Button
                        playing = False

                    if self._rects[0].collidepoint(event.pos):         #New Game Button
                        self._game = self.game_init()
                        self.set_up_display()
                        game_status = 'ACTIVE'

                    row = self.get_square(event.pos)[0]
                    col = self.get_square(event.pos)[1]

                    #shoot ray
                    if self._game.is_non_corner_border((row,col)) and game_status == 'ACTIVE':
                        if self._game.shoot_ray(row,col) is None:             #hit
                            self.draw_circle((row,col), black)
                        elif self._game.shoot_ray(row,col) == (row,col):      #reflection
                            self.draw_circle((row,col), white)
                        elif self._game.shoot_ray(row,col) != False:           #deflection
                            color = self.random_color()
                            self.draw_circle((row,col),color)
                            self.draw_circle(self._game.shoot_ray(row,col), color)

                    #guess atom
                    if (row,col) != (None, None) and not self._game.is_border((row,col)) and game_status == 'ACTIVE':
                        if self._game.guess_atom(row,col):
                            self.draw_circle((row,col), red)
                        else:
                            self.draw_x((row,col), red)

                    #update stats
                    self.display_score()
                    self.display_atoms_left()


                font = pygame.font.Font('freesansbold.ttf', 50)

                #Winning condition
                if self._game.atoms_left() == 0:
                    pygame.draw.rect(self._screen, white, self._rects[2])
                    atomsText = font.render('YOU WIN!!!!!!!!', True, green, white)
                    self._screen.blit(atomsText, self._rects[2])
                    game_status = 'OVER'

                #Losing condition
                if self._game.get_score() <= 0:
                    pygame.draw.rect(self._screen, white, self._rects[2])
                    atomsText = font.render('YOU LOSE!!!!!!', True, red, white)
                    self._screen.blit(atomsText, self._rects[2])

                    #display remaining atoms
                    for atom in self._game.get_atoms_dict():
                        self.draw_circle(atom, red)

                    game_status = 'OVER'


            pygame.display.flip()


UI = BlackBoxUI()
UI.play_game()
