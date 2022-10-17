# write your code here
import random
import re
import time
import math

INF = math.inf
MAXIMIZING_PLAYER = ''
MINIMIZING_PLAYER = ''


# the player who start the game is the maximizing player
def minimax(board, player_turn):
    #  terminal case: when there is win, or tie
    terminal_state = check_for_winner(board)

    if terminal_state != 'No winner':
        if terminal_state == 'Draw':
            return 0  # make the draw state take score value of 0
        elif terminal_state == f'{MAXIMIZING_PLAYER} wins':
            return 1  # make the winning state take score value of 1
        else:
            return -1   # make the losing state take score value of -1

    valid_states = get_available_spots(board)
    if player_turn == MAXIMIZING_PLAYER:
        max_val = INF * -1
        for state in valid_states:
            row, column = state
            board[row][column] = MAXIMIZING_PLAYER  # make a move
            val = minimax(board, MINIMIZING_PLAYER)
            board[row][column] = ' '
            max_val = max(max_val, val)  # undo move
        return max_val
    else:  # minimizing player
        min_val = INF
        for state in valid_states:
            row, column = state
            board[row][column] = MINIMIZING_PLAYER  # make a move
            val = minimax(board, MAXIMIZING_PLAYER)
            board[row][column] = ' '  # undo move
            min_val = min(min_val, val)
        return min_val


def get_valid_coordinates():
    coordinates = input("Enter the coordinates: ")
    if re.match("^\d\s+\d$", coordinates) is None:
        raise Exception("You should enter numbers!")
    elif re.match("^[123]\s+[123]$", coordinates) is None:
        raise Exception("Coordinates should be from 1 to 3!")
    return [int(coordinate) for coordinate in coordinates.split()]


def get_available_spots(board):
    empty_spots = []
    for row in range(3):
        for column in range(3):
            if board[row][column] == ' ':
                empty_spots.append((row, column))
    return empty_spots


def print_x_o_board(board):
    print("---------")
    for row in board:
        print("| ", end='')
        new_row = "".join(row)
        new_row = new_row.replace('_', ' ', new_row.count('_'))  # replace all _ cells with an empty cell
        print(*new_row, sep=' ', end='')
        print(' |')
    print("---------")


def check_for_winner(board):

    # check for each row
    for row in board:
        if row.count('X') == 3:
            return 'X wins'
        elif row.count('O') == 3:
            return 'O wins'

    # check for each column
    if all([board[0][0] == 'X', board[1][0] == 'X', board[2][0] == 'X']) or \
            all([board[0][1] == 'X', board[1][1] == 'X', board[2][1] == 'X']) or \
            all([board[0][2] == 'X', board[1][2] == 'X', board[2][2] == 'X']):
        return 'X wins'
    elif all([board[0][0] == 'O', board[1][0] == 'O', board[2][0] == 'O']) or \
            all([board[0][1] == 'O', board[1][1] == 'O', board[2][1] == 'O']) or \
            all([board[0][2] == 'O', board[1][2] == 'O', board[2][2] == 'O']):
        return 'O wins'

    # check for diagonals
    if all([board[0][0] == 'X', board[1][1] == 'X', board[2][2] == 'X']) or \
            all([board[0][2] == 'X', board[1][1] == 'X', board[2][0] == 'X']):  # left diagonal
        return 'X wins'
    elif all([board[0][0] == 'O', board[1][1] == 'O', board[2][2] == 'O']) or \
            all([board[0][2] == 'O', board[1][1] == 'O', board[2][0] == 'O']):
        return 'O wins'

    # if there is draw
    count_empty_cells = 0
    for row in board:
        count_empty_cells += row.count(' ')
    if count_empty_cells == 0:
        return 'Draw'
    return 'No winner'


def start_game():
    command = input("Enter command: ")
    while re.match("^(exit)|(start\s+(user|easy|medium|hard)\s+(user|easy|medium|hard))$", command) is None:
        print("Bad parameters!")
        command = input("Enter command: ")
    if command == 'exit':
        exit(0)
    return [command.split()[1], command.split()[2]]  # return the type of two user


def human_move(player_move_type, board):
    while True:
        try:
            row_position, column_position = get_valid_coordinates()
            if board[row_position - 1][column_position - 1] in ['X', 'O']:
                print("This cell is occupied! Choose another one!")
            else:
                board[row_position - 1][column_position - 1] = player_move_type
                break
        except Exception as err:
            print(err)


def easy(player_move_type, board):
    random.seed()
    available_spots = get_available_spots(board)
    available_spot = random.choice(available_spots)
    random_row_position = available_spot[0]
    random_column_position = available_spot[1]
    board[random_row_position][random_column_position] = player_move_type


def medium(player_move_type, board):
    # logic one: check if the computer has two in a row and can win with one further move
    for row in board:
        if row.count(player_move_type) == 2 and row.count(' ') == 1:
            row[row.index(' ')] = player_move_type
            return

    opponent_move_type = 'O' if player_move_type == 'X' else 'X'

    # logic one: check if the opponent can win with one move, it plays the move necessary to block this
    temp_board = board.copy()  # temp board to guess opponent next optimal move and block it.
    for row in range(3):
        for column in range(3):
            if temp_board[row][column] == ' ':
                temp_board[row][column] = opponent_move_type
                # check if we make that move the opponent will win then we will block that move.
                if check_for_winner(temp_board) == f'{opponent_move_type} wins':
                    board[row][column] = player_move_type  # block move in the original board.
                    return
                else:
                    temp_board[row][column] = ' '  # undo the change of the board and tyr another cell

    # if the above two logics are not achieve make easy move
    easy(player_move_type, board)


# make level hard using minmax algorithm
def hard(player_move_type, board):
    best_move = (-1, -1)
    available_moves = get_available_spots(board)
    global MAXIMIZING_PLAYER
    MAXIMIZING_PLAYER = player_move_type
    global MINIMIZING_PLAYER
    MINIMIZING_PLAYER = 'O' if player_move_type == 'X' else 'X'
    max_score = INF * -1
    for row, column in available_moves:
        board[row][column] = player_move_type
        score = minimax(board, MINIMIZING_PLAYER)
        if score > max_score:
            max_score = score
            best_move = (row, column)
        board[row][column] = ' '

    board[best_move[0]][best_move[1]] = player_move_type


def computer_move(player_move_type, board, difficulty):
    print(f'Making move level "{difficulty}"')
    if difficulty == 'easy':
        easy(player_move_type, board)
    elif difficulty == 'medium':
        medium(player_move_type, board)
    else:
        hard(player_move_type, board)


def make_move(player, current_move, board):
    if player == 'user':
        human_move(current_move, board)
    else:
        computer_move(current_move, board, player)


def main():
    while True:
        players = start_game()
        board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        moves = ['X', 'O']
        print_x_o_board(board)
        turn = 0  # make the first player play X
        while check_for_winner(board) == 'No winner':
            current_player = players[turn]
            current_move = moves[turn]
            make_move(current_player, current_move, board)
            turn = (turn + 1) % 2  # make turn take only values 0 and 1 so that players take turns
            print_x_o_board(board)
            time.sleep(0.3)
        print(check_for_winner(board))


if __name__ == '__main__':
    main()
    