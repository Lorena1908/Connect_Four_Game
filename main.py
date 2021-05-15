import pygame
from math import floor
pygame.font.init()

class Circle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    
    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

# ROW AND COLUMN COUNT
row_count = 6
column_count = 7

# VARIABLES
square = 100
width = column_count * square # (= 700)
height = (row_count+1) * square # (= 700)
size = (width, height)
radius = int(square/2 - 5) # (= 45)
win = pygame.display.set_mode(size)
pygame.display.set_caption('Conect Four')

def create_board():
    return [[(0,0,0) for _ in range(column_count)] for _ in range(row_count)]

def is_valid_location(board, column):
    return board[0][column] == (0,0,0)

def get_next_row(board, column):
    for row in range(len(board)-1, -1, -1): # The for loop will start at the last number (5)
        if board[row][column] == (0,0,0):
            return row

def winning_move(board, piece):
    # Check horizontal locations for win
    for column in range(column_count-3):
        for row in range(row_count):
            if board[row][column] == piece and board[row][column+1] == piece and board[row][column+2] == piece and board[row][column+3] == piece:
                return True
    
    # Check vertical locations for win
    for column in range(column_count):
        for row in range(row_count-3):
            if board[row][column] == piece and board[row+1][column] == piece and board[row+2][column] == piece and board[row+3][column] == piece:
                return True
    
    # Check positively sloped diagonols
    for column in range(column_count-3):
        for row in range(row_count-3):
            if board[row][column] == piece and board[row+1][column+1] == piece and board[row+2][column+2] == piece and board[row+3][column+3] == piece:
                return True

    # Check negatively sloped diagonols
    for column in range(column_count-3):
        for row in range(3, row_count):
            if board[row][column] == piece and board[row-1][column+1] == piece and board[row-2][column+2] == piece and board[row-3][column+3] == piece:
                return True

def draw_board(board):
    for row in range(len(board)):
        for column in range(len(board[row])):
            pygame.draw.rect(win, (0,0,255), (column * square, row * square + square, square, square))
            pygame.draw.circle(win, board[row][column], (column * square + square/2, row * square + square + square/2), radius)

def main():
    board = create_board()
    game_over = False
    turn = 0
    font = pygame.font.SysFont('monospace', 75)
    player1 = Circle(350, 50, (255,0,0))
    player2 = Circle(350, 50, (255,255,0))
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.0000001
    clicked = False

    draw_board(board)
    while not game_over:
        fall_time += clock.get_rawtime()
        clock.tick()

        # This is always player after the for loop
        if fall_time/1000 >= fall_speed and clicked:
            draw_board(board)
            fall_time = 0

            if turn == 1:
                # This is for the circle at the top to stop blinking
                if player1.y <= square*3:
                    pygame.draw.rect(win, (0,0,0), (0,0, width, square))

                player1.y += 1
                player1.x = column * square + square/2

                if player1.y >= (row+1) * square + square/2:
                    player1.y -= 1

                    if is_valid_location(board, column):
                        board[row][column] = player1.color

                        if winning_move(board, player1.color):
                            pygame.draw.rect(win, (0,0,0), (0,0, width, square))
                            text = font.render('Red Wins!', 1, player1.color)
                            win.blit(text, (width/2 - text.get_width()/2, 10))
                            game_over = True
                player1.draw()
            else:
                # This is for the circle at the top to stop blinking
                if player2.y <= square*3:
                    pygame.draw.rect(win, (0,0,0), (0,0, width, square))
                
                player2.y += 1
                player2.x = column * square + square/2

                if player2.y >= (row+1) * square + square/2:
                    player2.y -= 1

                    if is_valid_location(board, column):
                        board[row][column] = player2.color

                        if winning_move(board, player2.color):
                            pygame.draw.rect(win, (0,0,0), (0,0, width, square))
                            text = font.render('Yellow Wins!', 1, player2.color)
                            win.blit(text, (width/2 - text.get_width()/2, 10))
                            game_over = True
                player2.draw()
            pygame.display.update()
        
        if game_over:
            pygame.time.wait(1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(win, (0,0,0), (0,0, width, square))
                posx1 = event.pos[0]

                if turn == 0:
                    player1.x = posx1
                    player1.draw()
                else:
                    player2.x = posx1
                    player2.draw()
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(win, (0,0,0), (0,0, width, square))
                player1 = Circle(350, 50, (255,0,0))
                player2 = Circle(350, 50, (255,255,0))
                clicked = True
                posx2 = event.pos[0]
                column = int(floor(posx2/square))
                row = get_next_row(board, column)

                draw_board(board)
                pygame.display.update()
                
                turn += 1
                turn %= 2

def main_menu():
    run = True

    while run:
        win.fill((0,0,0))
        font = pygame.font.SysFont('monospace', 80)
        text = font.render('Click to Play', 1, (255,255,255))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

main_menu()