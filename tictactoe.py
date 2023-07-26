import pygame
import time


pygame.init()


WINDOW_SIZE = 600
BOARD_SIZE = 300
CELL_SIZE = BOARD_SIZE // 3
LINE_WIDTH = 10
MARGIN = (WINDOW_SIZE - BOARD_SIZE) // 2
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))  # Increased the height for the reset button
pygame.display.set_caption('Tic Tac Toe')
clock = pygame.time.Clock()


font = pygame.font.SysFont(None, 40)


board = [[' ' for _ in range(3)] for _ in range(3)]
player_turn = 'X'
winner = None
game_over = False


def draw_board():
    screen.fill(GREY)

    pygame.draw.line(screen, WHITE, (MARGIN + CELL_SIZE, MARGIN), (MARGIN + CELL_SIZE, WINDOW_SIZE - MARGIN), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (MARGIN + 2 * CELL_SIZE, MARGIN), (MARGIN + 2 * CELL_SIZE, WINDOW_SIZE - MARGIN), LINE_WIDTH)


    pygame.draw.line(screen, WHITE, (MARGIN, MARGIN + CELL_SIZE), (WINDOW_SIZE - MARGIN, MARGIN + CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (MARGIN, MARGIN + 2 * CELL_SIZE), (WINDOW_SIZE - MARGIN, MARGIN + 2 * CELL_SIZE), LINE_WIDTH)

    # Draw X and O
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                draw_x(row, col)
            elif board[row][col] == 'O':
                draw_o(row, col)


def draw_x(row, col):
    x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
    y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.line(screen, WHITE, (x - CELL_SIZE // 2, y - CELL_SIZE // 2), (x + CELL_SIZE // 2, y + CELL_SIZE // 2), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (x + CELL_SIZE // 2, y - CELL_SIZE // 2), (x - CELL_SIZE // 2, y + CELL_SIZE // 2), LINE_WIDTH)


def draw_o(row, col):
    x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
    y = MARGIN + row * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, WHITE, (x, y), CELL_SIZE // 2 - LINE_WIDTH // 2, LINE_WIDTH)


def check_winner():
    global winner
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != ' ':
            winner = board[row][0]
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            winner = board[0][col]
            return True
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        winner = board[0][0]
        return True
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        winner = board[0][2]
        return True
    return False


def check_draw():
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                return False
    return True


def reset_game():
    global board, player_turn, winner, game_over
    board = [[' ' for _ in range(3)] for _ in range(3)]
    player_turn = 'X'
    winner = None
    game_over = False


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if MARGIN <= x <= MARGIN + BOARD_SIZE and MARGIN <= y <= MARGIN + BOARD_SIZE:  # Check if click is within the game board area
                row, col = (y - MARGIN) // CELL_SIZE, (x - MARGIN) // CELL_SIZE
                if not game_over and board[row][col] == ' ':
                    board[row][col] = player_turn
                    if check_winner():
                        game_over = True
                    elif MARGIN <= x <= MARGIN + BOARD_SIZE and WINDOW_SIZE - 100 <= y <= WINDOW_SIZE:
                        if game_over:
                            reset_game()
                    elif check_draw():
                        game_over = True  # Check for a draw
                        winner = 'Draw'
                    else:
                        player_turn = 'O' if player_turn == 'X' else 'X'
            elif MARGIN <= x <= MARGIN + BOARD_SIZE and WINDOW_SIZE - 100 <= y <= WINDOW_SIZE:  # Check if click is within the reset button area
                reset_game()

    screen.fill(GREY)  

   
    pygame.draw.line(screen, BLACK, (0, WINDOW_SIZE - 100), (WINDOW_SIZE, WINDOW_SIZE - 100), 2)

    draw_board()

    # Draw text on top of the game board
    text = f"Player {player_turn}'s turn" if not game_over else f"Winner: {winner}" if winner != 'Draw' else "It's a Draw!"
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, MARGIN // 2))  # Adjust vertical position
    screen.blit(text_surface, text_rect)

    reset_text = font.render('Reset', True, WHITE)
    reset_rect = reset_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE - 50))  # Adjust vertical position
    pygame.draw.rect(screen, BLACK, reset_rect)
    screen.blit(reset_text, reset_rect)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
