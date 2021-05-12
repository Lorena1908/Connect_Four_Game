import numpy as np
import pygame
import sys
import math
pygame.font.init()

# COLORS
blue = (0,0,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)
white = (255,255,255)

# ROW AND COLUMN COUNT
row_count = 6
column_count = 7

# FUNCTIONS
def create_board():
    board = np.zeros((row_count, column_count)) # A matrix of 6 rows and 7 columns
    return board

def drop_piece(board, row, column, piece):
    # Make the last empty row become number 1 or 2
    board[row][column] = piece

def is_valid_location(board, column):
    # Checks if the top row is 0 (empty) so the player can drop the "piece" in there
    return board[row_count-1][column] == 0 # Is the position of the last row and column empty?

def get_next_open_row(board, column):
    for row in range(row_count): # It starts at the bottom
        if board[row][column] == 0:
            return row

def print_board(board):
    print(np.flip(board, 0)) # Flip the board in the x axis(0)

def winning_move(board, piece):
    # Check horizontal locations for win
    for column in range(column_count-3): 
        # It's column_count-3 because there are three columns in which you can't start a sequence of four
        for row in range(row_count):
            if board[row][column] == piece and board[row][column+1] == piece and board[row][column+2] and board[row][column+3]:
                return True
    
    # Check vertical locations for win
    for column in range(column_count): 
        # It's row_count-3 because there are three rows in which you can't start a sequence of four
        for row in range(row_count-3):
            if board[row][column] == piece and board[row+1][column] == piece and board[row+2][column] and board[row+3][column]:
                return True
    
    # Check positively sloped diagonols
    for column in range(column_count-3):
        for row in range(row_count-3):
            if board[row][column] == piece and board[row+1][column+1] == piece and board[row+2][column+2] and board[row+3][column+3]:
                return True

    # Check negatively sloped diagonols
    for column in range(column_count-3):
        for row in range(3, row_count):
            if board[row][column] == piece and board[row-1][column+1] == piece and board[row-2][column+2] and board[row-3][column+3]:
                return True

def draw_board(board):
    for column in range(column_count):
        for row in range(row_count):
            pygame.draw.rect(screen, blue, (column*square, row*square+square, square, square))
            pygame.draw.circle(screen, black, (int(column*square+square/2), int(row*square+square+square/2)), radius)
    
    for column in range(column_count):
        for row in range(row_count):
            if board[row][column] == 1:
                pygame.draw.circle(screen, red, (int(column*square+square/2), height-int(row*square+square/2)), radius)
            elif board[row][column] == 2:
                pygame.draw.circle(screen, yellow, (int(column*square+square/2), height-int(row*square+square/2)), radius)
    pygame.display.update()

# VARIABLES
square = 100
width = column_count * square # (= 700)
height = (row_count+1) * square # (= 700)
size = (width, height)
radius = int(square/2 - 5) # (= 45)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Conect Four')

def main():
    board = create_board()
    game_over = False
    turn = 0

    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont('monospace', 75)

    # MAIN GAME LOOP
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, black, (0,0, width, square))
                posx = event.pos[0] # Position of the mouse
                if turn == 0:
                    pygame.draw.circle(screen, red, (posx, int(square/2)), radius)
                else:
                    pygame.draw.circle(screen, yellow, (posx, int(square/2)), radius)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, black, (0,0, width, square))
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    column = int(math.floor(posx/square)) # It returns a number between 0 and 6

                    if is_valid_location(board, column):
                        row = get_next_open_row(board, column) # The next row is where the piece should be droped
                        drop_piece(board, row, column, 1)

                        if winning_move(board, 1):
                            label = myfont.render('Red Wins!', 1, red)
                            screen.blit(label, (width/2 - label.get_width()/2,10))
                            game_over = True

                # Ask for Player 2 Input
                else:
                    posx = event.pos[0]
                    column = int(math.floor(posx/square))

                    if is_valid_location(board, column):
                        row = get_next_open_row(board, column)
                        drop_piece(board, row, column, 2)

                        if winning_move(board, 2):
                            label = myfont.render('Yellow Wins!', 1, yellow)
                            screen.blit(label, (width/2 - label.get_width()/2,10))
                            game_over = True
    
                draw_board(board)

                turn += 1
                turn %= 2 # This alternate between the numbers 1 and 0

                if game_over:
                    pygame.time.wait(2000)

def main_menu():
    run = True

    while run:
        screen.fill((0,0,0))
        font = pygame.font.SysFont('monospace', 80)
        text = font.render('Click to Play', 1, white)
        screen.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()

while True:
    main_menu()