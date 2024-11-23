import math,random
import pygame
from pygments.styles.dracula import background

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""
class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen

    def set_cell_value(self, value):
        self.value = value
    def set_sketched_value(self, value):
        self.value = value
    def draw(self):
        if(self.value!=0):
            pass



class SudokuGenerator:
    '''
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''
    def __init__(self, row_length, removed_cells):
        pass

    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''
    def get_board(self):
        pass

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''
    def print_board(self):
        pass

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row
	
	Return: boolean
    '''
    def valid_in_row(self, row, num):
        pass

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column
	
	Return: boolean
    '''
    def valid_in_col(self, col, num):
        pass

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''
    def valid_in_box(self, row_start, col_start, num):
        pass
    
    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''
    def is_valid(self, row, col, num):
        pass

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''
    def fill_box(self, row_start, col_start):
        pass
    
    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''
    def fill_diagonal(self):
        pass

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled
	
	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called
    
    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''
    def remove_cells(self):
        pass

'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

def main():
    # Initialize screen
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku")


    # Fill background option 1
    background_image = pygame.image.load('Sudoku_BG.jpg')
    background_image = pygame.transform.scale(background_image,(1280,720))

    # Fill background option 2
    lines = [[random.randint(0,SCREEN_WIDTH), random.randint(-SCREEN_HEIGHT,SCREEN_HEIGHT)] for i in range(50)]

    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    PURPLE = (128,0,128)


    # Welcome text
    welcome_font = pygame.font.Font(None, 80)
    welcome_text = welcome_font.render("Welcome to Sudoku!",1,WHITE)
    welcome_textpos = welcome_text.get_rect()
    welcome_textpos.centerx = screen.get_rect().centerx
    welcome_textpos.centery = 200


    # Select game mode text gm_text == gamemodetext
    gm_font = pygame.font.Font(None, 50)
    gm_text = gm_font.render("Select Game Mode:",1,WHITE)
    gm_textpos = gm_text.get_rect()
    gm_textpos.centerx = screen.get_rect().centerx
    gm_textpos.centery = 350

    # default font for button text
    button_font = pygame.font.Font(None, 48)

    # easy
    easy_rect = pygame.Rect(300,250,320,500)
    easy_text = button_font.render("Easy",1,WHITE)
    easy_button = easy_text.get_rect(center=easy_rect.center)

    # medium
    medium_rect = pygame.Rect(300, 250, 640, 500)
    medium_text = button_font.render("Medium", 1, WHITE)
    medium_button = medium_text.get_rect(center=medium_rect.center)

    # hard
    hard_rect = pygame.Rect(300, 250, 960, 500)
    hard_text = button_font.render("Hard", 1, WHITE)
    hard_button = hard_text.get_rect(center=hard_rect.center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if easy_button.collidepoint(mouse_x,mouse_y):
                    print("Easy button pressed!")
                if medium_button.collidepoint(mouse_x,mouse_y):
                    print("Medium button pressed!")
                if hard_button.collidepoint(mouse_x,mouse_y):
                    print("Hard button pressed!")

        # cool purple animated background
        screen.fill(BLACK)
        for line in lines:
            pygame.draw.line(screen, PURPLE, (line[0], line[1]), (line[0], line[1] + 50), 2)
            line[1] += .5
            if line[1] > SCREEN_HEIGHT:
                line[1] = random.randint(-100, 0)

        # placing everything on the screen
        screen.blit(welcome_text, welcome_textpos)
        screen.blit(gm_text,gm_textpos)
        pygame.draw.rect(screen,PURPLE,easy_button)
        screen.blit(easy_text,easy_button)
        pygame.draw.rect(screen, PURPLE, medium_button)
        screen.blit(medium_text,medium_button)
        pygame.draw.rect(screen, PURPLE, hard_button)
        screen.blit(hard_text,hard_button)
        pygame.display.flip()

if __name__ == "__main__":
    main()

