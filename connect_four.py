import numpy as np
import pygame
import sys
import math

# all the required color combinations used in this game
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# no. of rows and columns
ROW_COUNT = 6
COLUMN_COUNT = 7

# creating a game board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# dropping a players's piece
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# if column has no more spaces!
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


# search for a open row
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


# print the game board
def print_board(board):
    print(np.flip(board, 0))


# check if someone wins
def winning_move(board, piece):
    # check all horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and \
                    board[r][c + 3] == piece:
                return True

    # check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and \
                    board[r + 3][c] == piece:
                return True

    # check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                    board[r + 3][c + 3] == piece:
                return True

    # check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                    board[r - 3][c + 3] == piece:
                return True


# draw the board
def draw_board(board):

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):

            # draw a BLUE rectangle for the board
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))

            # draw circles in that rectangle evenly for the pieces to put down
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                               int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):

            # draw a RED circle as soon as player 1 clicks on the board
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                 height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            # draw a YELLOW circle as soon as player 2 clicks on the board
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                    height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    # update the screen
    pygame.display.update()


# main commands

# create a board for the game
board = create_board()

# print the board on the screen
print_board(board)

# initialize the game_over as false for now
game_over = False
turn = 0

# initialize pygame
pygame.init()

# give the size of one square to be 100 X 100
SQUARESIZE = 100

# width and height of the board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

# set the pygame screen to display
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

# font to display the results of the game
my_font = pygame.font.SysFont("monospace", 75)

# the main loop of the game
while not game_over:

    # if user clicks the close button - game over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # detect the motion of the mouse
        if event.type == pygame.MOUSEMOTION:

            # Draw a black screen behind the moving piece to avoid it drawing on the whole rectangle
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

            # save the x axis position of the moving mouse
            posx = event.pos[0]

            # change the color of the moving piece when turns change
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        # record events when mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:

            # create the black rectangle on the top of the screen
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

            # ask for player 1 input
            if turn == 0:

                # record the x axis of the mouse when it is clicked
                posx = event.pos[0]

                col = int(math.floor(posx / SQUARESIZE))

                # if location is valid, search for vacant in row and drop a piece
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    # if player one wins the game
                    if winning_move(board, 1):

                        # render the font to a label
                        label = my_font.render("PLAYER 1 WINS!!", True, RED)

                        # print the label on the screen
                        screen.blit(label, (30, 10))
                        game_over = True

            # ask for player 2 input
            else:

                # record the x axis of the mouse when it is clicked
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                # if location is valid, search for vacant in row and drop a piece
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    # if player one wins the game
                    if winning_move(board, 2):

                        # render the font to a label
                        label = my_font.render("PLAYER 2 WINS!!", True, YELLOW)

                        # print the label on the screen
                        screen.blit(label, (30, 10))
                        game_over = True

            # print the board of this current loop
            print_board(board)

            # draw the pieces on that board of this current loop
            draw_board(board)

            # alternate the turns
            turn += 1
            turn = turn % 2

            if game_over:

                # wait for 4 seconds before closing the game
                pygame.time.wait(4000)
