from player import HardPlayer, MediumPlayer, EasyPlayer, AIPlayer
from enum import Enum
import time


class PlayerType(Enum):
    HUMAN = 1
    AI_EASY = 2
    AI_MEDIUM = 3
    AI_HARD = 4



class GameError(BaseException):
    def __init__(self, choice):
        self.choice = choice

    def __str__(self):
        return f"invalid choice ({self.choice})"


def create_player(player_choice, player_symbol):
    if player_choice == PlayerType.AI_EASY.value:
        return EasyPlayer(player_symbol)
    elif player_choice == PlayerType.AI_MEDIUM.value:
        return MediumPlayer(player_symbol)
    elif player_choice == PlayerType.AI_HARD.value:
        return HardPlayer(player_symbol)


def end_game():
    exit(0)


class Game:
    BOARD_SIZE = 3

    def __init__(self):
        self.__player1 = None
        self.__player2 = None
        self.__turn = "X"
        self.__board = [[' ' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]

    @property
    def _available_moves(self):
        empty_cells = []
        for row in range(self.BOARD_SIZE):
            for column in range(self.BOARD_SIZE):
                if self.__board[row][column] == ' ':
                    empty_cells.append((row, column))
        return empty_cells

    def _check_winner(self, row, column):

        # check row
        if self.__board[row] == [self.__turn for _ in range(self.BOARD_SIZE)]:
            return True

        # check column
        if all(self.__board[r][column] == self.__turn for r in range(self.BOARD_SIZE)):
            return True

        # check left diagonal
        if row == column:
            return all(self.__board[r][r] == self.__turn for r in range(self.BOARD_SIZE))

        # check right diagonal
        if row + column == 2:
            return all(self.__board[r][2 - r] == self.__turn for r in range(self.BOARD_SIZE))

    def _switch_player(self):
        self.__turn = "X" if self.__turn == "O" else "O"

    def _is_full(self):
        return all(self.__board[i][j] != " " for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE))

    def _print_game_board(self):
        print("-------------")
        for row in self.__board:
            print("| ", end='')
            new_row = "".join(row)
            print(*new_row, sep=' | ', end='')
            print(' |')
        print("-------------")

    def _human_move(self):
        while True:
            try:
                row, column = [int(x) - 1 for x in input("Move: ").split()]
                if not (0 <= row < self.BOARD_SIZE) or not (0 <= column < self.BOARD_SIZE) or (
                        row, column) not in self._available_moves:
                    raise GameError((row, column))
            except (ValueError, GameError) as _:
                print("Invalid choice")
            else:
                break

        self.__board[row][column] = self.__turn
        return row, column

    def _reset(self):
        self.__board = [[' ' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.__turn = "X"

    def _play(self, player):
        if isinstance(player, AIPlayer):
            return player.make_move(self.__board)
        return self._human_move()

    def start(self):
        players_options = ["human", "AI Easy", "AI Medium", "AI Hard"]
        print("Welcome to Tic Tac Toe Game!")

        while True:
            try:
                game_choice = int(input("1-Start\n2-Quit\n"))
                if game_choice not in [1, 2]:
                    raise GameError(game_choice)
                if game_choice == 2:
                    end_game()

            except (ValueError, GameError) as _:
                print("invalid choice please choose between (1, 2)")
                continue

            while game_choice == 1:
                player_choices = [PlayerType.HUMAN, PlayerType.HUMAN]
                for i, option in enumerate(players_options):
                    print(f"{i + 1}- {option}")

                current_player_choice = 1
                while current_player_choice < 3:
                    try:
                        player_choices[current_player_choice - 1] = int(input(f"Player {current_player_choice}: "))
                        if not (1 <= player_choices[current_player_choice - 1] < 5):
                            raise GameError(player_choices[current_player_choice - 1])
                        current_player_choice += 1
                    except (ValueError, GameError) as _:
                        print("Invalid Choice please choose between (1 and 4)")
                        continue

                self.__player1 = create_player(player_choices[0], 'X')
                self.__player2 = create_player(player_choices[1], 'O')

                while True:
                    self._print_game_board()
                    row_move, column_move = self._play(self.__player1 if self.__turn == "X" else self.__player2)
                    if self._check_winner(row_move, column_move):
                        self._print_game_board()
                        print(f"Game Over! {self.__turn} wins!")
                        break

                    elif self._is_full():
                        self._print_game_board()
                        print(f"Game Over! Draw")
                        break
                    time.sleep(0.1)

                    self._switch_player()
                self._reset()
                game_choice = 0
