from sudoku_alg import valid, solve, find_empty   # --- Imported these functions from another .py file
from copy import deepcopy   # --- A deep copy constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original.
from sys import exit   # ---(sys). This module provides access to some objects used or maintained by the interpreter and to functions that interact strongly with the interpreter.
import pygame   # --- imports the pygame library module for GUI.
import time    # --- time module to add a timer to the GUI Game.
import random   # --- Random variable generators.
pygame.init()   # -- to initiate the pygame module.

def generate():
    '''A function to Randomly generates a Sudoku grid/board'''
    while True:   # --- return will interrupt the loop
        for event in pygame.event.get():   # --- getting the event type in pygame
            if event.type == pygame.QUIT:
                exit()
        board = [[0 for i in range(9)] for j in range (9)]
        # puts one random number, then solves the board to generate a board
        for i in range(9):
            for j in range(9):
                # --- Return a random integer N such that 1 <= N <= 10.
                if random.randint(1, 10) >= 5:   # --- checks if the random integer is >= 5.
                    board[i][j] = random.randint(1, 9)   # --- plug in random number at random spot
                    if valid(board, (i, j), board[i][j]):   # --- calling the valid function to check the validity of the random integer .
                        continue
                    else:
                        board[i][j] = 0
        partialBoard = deepcopy(board) #copies board without being modified after solve is called
        if solve(board):   # --- calling the solve function to check the board against it.
            return partialBoard
class Board:
    '''A sudoku board made out of Tiles'''
    def __init__(self, window):
        self.board = generate()   # --- calling the previous function to the board.
        self.solvedBoard = deepcopy(self.board)   # --- inserting the solved board.
        solve(self.solvedBoard)    # --- calling the solve function to check the self.solvedBoard against it.
        self.tiles = [[Tile(self.board[i][j], window, i*60, j*60) for j in range(9)] for i in range(9)]   # --- Tiles Represents each white tile/box on the grid
        self.window = window

    def draw_board(self):
        '''Fills the board with Tiles and renders their values'''
        for i in range(9):
            for j in range(9):
                if j%3 == 0 and j != 0:  # --- vertical lines
                    pygame.draw.line(self.window, (0, 0, 0), ((j//3)*180, 0), ((j//3)*180, 540), 4)   # --- To draw a line on the screen by using the format pygame.draw.line( window, color, start position(x, y), end position(x, y), width )

                if i%3 == 0 and i != 0:  # --- horizontal lines
                    pygame.draw.line(self.window, (0, 0, 0), (0, (i//3)*180), (540, (i//3)*180), 4)   # --- To draw a line on the screen by using the format pygame.draw.line( window, color, start position(x, y), end position(x, y), width )

                self.tiles[i][j].draw((0,0,0), 1)   # --- to draw the tiles and here the format used is  self.tiles[i][j].draw(color, width)

                if self.tiles[i][j].value != 0:  # --- don't draw 0s on the grid
                    self.tiles[i][j].display(self.tiles[i][j].value, (21+(j*60), (16+(i*60))), (0, 0, 0))   # --- 20,5 are the coordinates of the first tile
        #bottom-most line
        pygame.draw.line(self.window, (0, 0, 0), (0, ((i+1) // 3) * 180), (540, ((i+1) // 3) * 180), 4)

    def deselect(self, tile):
        '''Deselects every tile except the one currently clicked'''
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j] != tile:
                    self.tiles[i][j].selected = False

    def redraw(self, keys, wrong, time):
        '''Redraws board with highlighted tiles'''
        self.window.fill((255,255,255))    # --- fill colour / background colour for the GUI.
        self.draw_board()   # --- calling the draw_board function to be drawn
        for i in range(9):
            for j in range(9):
                if self.tiles[j][i].selected:   # --- draws the border on selected tiles
                    self.tiles[j][i].draw((0,0,255), 4)    # --- fill colour / background colour for the GUI. and the format is ( color, width ).

                elif self.tiles[i][j].correct:
                    self.tiles[j][i].draw((34, 139, 34), 4)

                elif self.tiles[i][j].incorrect:
                    self.tiles[j][i].draw((255, 0, 0), 4)

        if len(keys) != 0:  # --- draws inputs that the user places on board but not their final value on that tile
            for value in keys:
                self.tiles[value[0]][value[1]].display(keys[value], (21+(value[0]*60), (16+(value[1]*60))), (128, 128, 128))

        if wrong > 0:
            font = pygame.font.SysFont('Bauhaus 93', 30)  # --- Red X marks to indicate a wrong answer
            text = font.render('X', True, (255, 0, 0))   # --- rendering the font and color onto the window
            self.window.blit(text, (10, 554))    # --- adding the time by using .blit()

            font = pygame.font.SysFont('Bahnschrift', 40)  # --- Number of Incorrect Inputs
            text = font.render(str(wrong), True, (0, 0, 0))
            self.window.blit(text, (32, 542))

        font = pygame.font.SysFont('Bahnschrift', 40)  # --- Time Display
        text = font.render(str(time), True, (0, 0, 0))
        self.window.blit(text, (388, 542))
        pygame.display.flip()   # --- flip() -> None Update the full display Surface to the screen

    def visualSolve(self, wrong, time):
        '''A function that Showcases how the board is solved via backtracking'''
        for event in pygame.event.get():  # --- so that touching anything doesn't freeze the screen
            if event.type == pygame.QUIT:
                exit()

        empty = find_empty(self.board)   # --- calling the find_empty function and adding the steps for the answer that we got from the self.board
        if not empty:
            return True

        for nums in range(9):
            if valid(self.board, (empty[0],empty[1]), nums+1):   # --- applying the valid function onto the values in the exact positions of values that will be shown
                self.board[empty[0]][empty[1]] = nums+1
                self.tiles[empty[0]][empty[1]].value = nums+1
                self.tiles[empty[0]][empty[1]].correct = True
                pygame.time.delay(63)   # --- show tiles at a slower rate in milliseconds
                self.redraw({}, wrong, time)   # --- calling the redraw function to redraw each change that is being made and output it for the user to see.

                if self.visualSolve(wrong, time):   # --- calling the same function inside again to perform the backtracking procces of going through all of the previous steps again until all of the grid is solved.
                    return True

                self.board[empty[0]][empty[1]] = 0   # --- setting the board back to 0 in case the last if statment was not satisfied
                self.tiles[empty[0]][empty[1]].value = 0   # --- setting the tile values back to 0 in case the last if statment was not satisfied
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(63)
                self.redraw({}, wrong, time)

    def hint(self, keys):
        '''Shows a random empty tile's solved value as a hint'''
        while True:   # --- keeps generating i,j coords until it finds a valid random spot
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if self.board[i][j] == 0:   # --- hint spot has to be empty
                if (j,i) in keys:
                    del keys[(j,i)]   # --- Deletion of a target list recursively deletes each target, from left to right.
                self.board[i][j] = self.solvedBoard[i][j]   # --- getting the correct board and inserts that specific position into the current board.
                self.tiles[i][j].value = self.solvedBoard[i][j]   # --- getting the correct value from the solved version of the tiles into the current tiles.
                return True

            elif self.board == self.solvedBoard:   # --- if there is no empty spaces then it stops
                return False
class Tile:
    '''Represents each white tile/box on the grid'''
    def __init__(self, value, window, x1, y1):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60)   # --- dimensions for the rectangle
        self.selected = False
        self.correct = False
        self.incorrect = False

    def draw(self, color, thickness):
        '''Draws a tile on the board'''
        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display(self, value, position, color):
        '''Displays a number on that tile'''
        font = pygame.font.SysFont('lato', 45)    # --- Create a pygame Font from system font resources.
                                                  # --- This will search the system fonts for the given font name. You can also enable bold or italic styles, and the appropriate system font will be selected if available.
        text = font.render(str(value), True, color)
        self.window.blit(text, position)

    def clicked(self, mousePos):
        '''Checks if a tile has been clicked'''
        if self.rect.collidepoint(mousePos):   # --- checks if a point is inside a rect
            self.selected = True
        return self.selected

def main():
    '''Runs the main Sudoku GUI/Game'''
    screen = pygame.display.set_mode((540, 590))   # --- Surface Initialize a window or screen for display
    screen.fill((255, 255, 255))   # --- background fill for the screen displayed
    pygame.display.set_caption("Sudoku trial ( hope you enjoy :) )")
    icon = pygame.image.load("icon.png")   # ---  Surface load new image from a file (or file-like object)
    pygame.display.set_icon(icon)   # --- set_icon(Surface) -> None Change the system image for the display window

    # --- loading screen when generating grid
    font = pygame.font.SysFont('Bahnschrift', 40)
    text = font.render("Generating", True, (0, 0, 0))
    screen.blit(text, (175, 245))

    font = pygame.font.SysFont('Bahnschrift', 40)
    text = font.render("Grid ...", True, (0, 0, 0))
    screen.blit(text, (230, 290))
    pygame.display.flip()   # --- flip() -> None Update the full display Surface to the screen

    # --- initialize values and variables
    wrong = 0
    board = Board(screen)
    selected = -1,-1   # --- NoneType error when selected = None, easier to just format as a tuple whose value will never be used
    keyDict = {}
    running = True
    startTime = time.time()
    while running:
        elapsed = time.time() - startTime   # --- to change from time to timer
        passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))   # --- formatting the output that the timer will appear in.

        if board.board == board.solvedBoard:   # --- user has solved the board
            for i in range(9):
                for j in range(9):
                    board.tiles[i][j].selected = False
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()   # --- so that it doesnt go to the outer run loop

            elif event.type == pygame.MOUSEBUTTONUP:   # --- allow clicks only while the board hasn't been solved
                mousePos = pygame.mouse.get_pos()   # --- to get the current position of the mouse click
                for i in range(9):
                    for j in range (9):
                        if board.tiles[i][j].clicked(mousePos):   # --- inserting a value in the position that is retrieved from the mousePos varibale.
                            selected = i,j
                            board.deselect(board.tiles[i][j])   # --- deselects every tile except the one currently clicked

            elif event.type == pygame.KEYDOWN:
                if board.board[selected[1]][selected[0]] == 0 and selected != (-1,-1):
                    if event.key == pygame.K_1:
                        keyDict[selected] = 1

                    if event.key == pygame.K_2:
                        keyDict[selected] = 2

                    if event.key == pygame.K_3:
                        keyDict[selected] = 3

                    if event.key == pygame.K_4:
                        keyDict[selected] = 4

                    if event.key == pygame.K_5:
                        keyDict[selected] = 5

                    if event.key == pygame.K_6:
                        keyDict[selected] = 6

                    if event.key == pygame.K_7:
                        keyDict[selected] = 7

                    if event.key == pygame.K_8:
                        keyDict[selected] = 8

                    if event.key == pygame.K_9:
                        keyDict[selected] = 9

                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:   # --- clears tile out
                        if selected in keyDict:
                            board.tiles[selected[1]][selected[0]].value = 0
                            del keyDict[selected]   # --- using the KeyDict dictionary that we created and stored our values in

                    elif event.key == pygame.K_RETURN:
                        if selected in keyDict:
                            if keyDict[selected] != board.solvedBoard[selected[1]][selected[0]]:   # --- clear tile when incorrect value is inputted
                                wrong += 1
                                board.tiles[selected[1]][selected[0]].value = 0
                                del keyDict[selected]
                                break
                            # --- valid and correct entry into cell
                            board.tiles[selected[1]][selected[0]].value = keyDict[selected]   # --- assigns current grid value
                            board.board[selected[1]][selected[0]] = keyDict[selected]   # --- assigns to actual board so that the correct value can't be modified
                            del keyDict[selected]

                if event.key == pygame.K_h:
                    board.hint(keyDict)   # --- Shows a random empty tile's solved value as a hint

                if event.key == pygame.K_SPACE:
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].selected = False
                    keyDict = {}   # --- clear keyDict out
                    board.visualSolve(wrong, passedTime)   # --- calling the visualSolve function after reseting the dictionary.
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].correct = False
                            board.tiles[i][j].incorrect = False   # --- reset tiles
                    running = False

        board.redraw(keyDict, wrong, passedTime)
    while True:   # --- another running loop so that the program ONLY closes when user closes program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
main()   # --- closing the main function for the pygame GUI.
pygame.quit()   # --- Quitting the pygame opened
