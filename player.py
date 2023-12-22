from abc import abstractmethod
import random
import copy


BOARD_SIZE = 3


def check_winner(board,  player_symbol):
    # check row
    for row in range(BOARD_SIZE):
        if all(board[row][column] == player_symbol for column in range(BOARD_SIZE)):
            return f'{player_symbol} wins'

    # check column
    for column in range(BOARD_SIZE):
        if all(board[row][column] == player_symbol for row in range(BOARD_SIZE)):
            return f'{player_symbol} wins'

    # check left diagonal
    if all(board[row][row] == player_symbol for row in range(BOARD_SIZE)):
        return f'{player_symbol} wins'

    # check right diagonal
    if all(board[row][2 - row] == player_symbol for row in range(BOARD_SIZE)):
        return f'{player_symbol} wins'

    if all(row.count(' ') == 0 for row in board):
        return 'Draw'

    return 'No winner'


def get_empty_cells(board):
    empty_cells = []
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if board[row][column] == ' ':
                empty_cells.append((row, column))
    return empty_cells


class AIPlayer:
    def __init__(self, player_symbol):
        self.player_symbol = player_symbol

    @abstractmethod
    def make_move(self, board):
        pass


class EasyPlayer(AIPlayer):
    def __init__(self, player_symbol):
        super().__init__(player_symbol)

    def make_move(self, board):
        random.seed()
        available_spot = random.choice(get_empty_cells(board))
        random_row_position = available_spot[0]
        random_column_position = available_spot[1]
        board[random_row_position][random_column_position] = self.player_symbol
        return random_row_position, random_column_position


class MediumPlayer(AIPlayer):
    def make_move(self, board):
        # logic one: check if the computer has two in a row and can win with one further move
        for row, row_cells in enumerate(board):
            if row_cells.count(self.player_symbol) == 2 and row_cells.count(' '):
                col = row_cells.index(' ')
                row_cells[col] = self.player_symbol
                return row, col

        opponent_symbol = 'O' if self.player_symbol == 'X' else 'X'

        # logic two: check if the opponent can win with one move, it plays the move necessary to block this
        temp_board = copy.deepcopy(board)  # temp board to guess opponent next optimal move and block it.

        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if temp_board[row][column] == ' ':
                    temp_board[row][column] = opponent_symbol
                    if check_winner(temp_board, opponent_symbol) == f'{opponent_symbol} wins':
                        board[row][column] = self.player_symbol
                        return row, column
                    else:
                        temp_board[row][column] = ' '

        # if the above two logics are not achieved make easy move
        player = EasyPlayer(self.player_symbol)
        return player.make_move(board)


class HardPlayer(AIPlayer):
    def __init__(self, player_symbol):
        super().__init__(player_symbol)
        self.MINIMIZING_PLAYER = 'O' if player_symbol == 'X' else 'X'
        self.MAXIMIZING_PLAYER = player_symbol
        self.terminal_states: dict[str, int] = {'Draw': 0, f'{self.MAXIMIZING_PLAYER} wins': 1,
                                                f'{self.MINIMIZING_PLAYER} wins': -1}

    def calculate_minmax_score(self, board, player_symbol):
        #  terminal case: when there is win, or tie
        status = check_winner(board, player_symbol)
        if status != 'No winner':
            return self.terminal_states[status]

        valid_states = get_empty_cells(board)
        if player_symbol == self.MAXIMIZING_PLAYER:
            max_val = float('-inf')
            for r, c in valid_states:
                board[r][c] = self.MAXIMIZING_PLAYER
                val = self.calculate_minmax_score(board, self.MINIMIZING_PLAYER)
                max_val = max(max_val, val)
                board[r][c] = ' '
            return max_val

        else:  # minimizing player
            min_val = float('inf')
            for r, c in valid_states:
                board[r][c] = self.MINIMIZING_PLAYER
                val = self.calculate_minmax_score(board, self.MAXIMIZING_PLAYER)
                board[r][c] = ' '
                min_val = min(min_val, val)
            return min_val

    def make_move(self, board):
        best_move = (-1, -1)
        available_moves = get_empty_cells(board)
        max_score = float('-inf')

        for row, column in available_moves:
            board[row][column] = self.MAXIMIZING_PLAYER
            score = self.calculate_minmax_score(board, self.MINIMIZING_PLAYER)
            if score > max_score:
                max_score = score
                best_move = (row, column)
            board[row][column] = ' '
        board[best_move[0]][best_move[1]] = self.MAXIMIZING_PLAYER
        return best_move
