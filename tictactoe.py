import sys
import random
import copy

class MoveGrader():
    moves = {}

    @staticmethod
    def best_move():
        max = -1000
        best_moves = list()
        for key, value in MoveGrader.moves.items():
            if value == max:
                best_moves.append(key)
            if value > max:
                best_moves.clear()
                max = value
                best_moves.append(key)
        i = random.randint(0, len(best_moves) - 1)
        return best_moves[i]


class player():

    def pick_move(self, board):
        pass

    def is_cpu(self):
        pass


class human_player(player):
    turn = "X"

    def __init__(self, turn="X"):
        self.turn = turn

    def pick_move(self, board):
        pass

    def is_cpu(self):
        return False


class cpu_player(player):
    turn = "X"

    def __init__(self, diff="easy", turn="X"):
        self.diff = diff
        self.turn = turn

    def is_cpu(self):
        return True

    def pick_move(self, b):
        available_moves = self.find_available_moves(b)
        if self.diff == "easy":
            idx = random.randint(0, len(available_moves) - 1)
            return available_moves[idx]
        elif self.diff == "medium":
            return self.pick_medium_move(b)
        elif self.diff == "hard":
            MoveGrader.moves.clear()
            return self.pick_hard_move(copy.deepcopy(b))

    def pick_medium_move(self, b):
        available_moves = self.find_available_moves(b)
        otherturn = "O" if self.turn == "X" else "X"
        for move in available_moves:
            if self.evaluate_move_wins(b, move, self.turn):
                return move
            if self.evaluate_move_wins(b, move, otherturn):
                return move
        idx = random.randint(0, len(available_moves) - 1) #If no blocking or winning move, choose random
        return available_moves[idx]

    def pick_hard_move(self, b): #play out the game for each available spot and evaluate results
        available_moves = cpu_player.find_available_moves(b)
        if len(available_moves) == 9:
            idx = random.randint(0,8)
            return available_moves[idx]
        for move in available_moves:
            test_board = copy.deepcopy(b)
            y, x = move.split()
            test_board[int(y) - 1][int(x) - 1] = self.turn
            MoveGrader.moves[move] = self.minmax(False, self.turn, test_board, self.turn)
        return MoveGrader.best_move()

    def minmax(self, is_max_turn, maximizer_mark, b, turn):
        if cpu_player.evaluate_table(b) == maximizer_mark:
            return 1
        if cpu_player.evaluate_table(b) == "DRAW":
            return 0
        if cpu_player.evaluate_table(b) != "NOTDONE":
            return -1
        nextturn = "O" if turn == 'X' else "X"
        scores = []
        for move in cpu_player.find_available_moves(b):
            test_board = copy.deepcopy(b)
            y, x = move.split()
            test_board[int(y) - 1][int(x) - 1] = nextturn
            scores.append(self.minmax(not is_max_turn, maximizer_mark, test_board, nextturn))
        return max(scores) if is_max_turn else min(scores)

    @staticmethod
    def find_available_moves(b):
        available_moves = []
        for y in range(0, 3):
            for x in range(0, 3):
                if b[y][x] == " ":
                    available_moves.append(str(y+1) + " " + str(x+1))
        return available_moves

    @staticmethod
    def evaluate_table(nboard):
        otherturn = "O"
        main_diag = [nboard[0][0], nboard[1][1], nboard[2][2]]
        secondary_diag = [nboard[0][2], nboard[1][1], nboard[2][0]]
        if main_diag.count("X") == 3 or secondary_diag.count("X") == 3:
            return "X"
        if main_diag.count(otherturn) == 3 or secondary_diag.count(otherturn) == 3:
            return otherturn
        for i in range(0, 3):
            if nboard[i].count("X") == 3 or [nboard[0][i], nboard[1][i], nboard[2][i]].count("X") == 3:
                return "X"
            if nboard[i].count(otherturn) == 3 or [nboard[0][i], nboard[1][i], nboard[2][i]].count(otherturn) == 3:
                return otherturn
        if cpu_player.is_board_full(nboard):
            return "DRAW"
        return "NOTDONE"

    @staticmethod
    def is_board_full(b):
        for line in b:
            if " " in line:
                return False
        return True

    @staticmethod
    def evaluate_move_wins(b, move, turn):
        nboard = copy.deepcopy(b)
        y, x = move.split()
        nboard[int(y) - 1][int(x) - 1] = turn
        main_diag = [nboard[0][0], nboard[1][1], nboard[2][2]]
        secondary_diag = [nboard[0][2], nboard[1][1], nboard[2][0]]
        if main_diag.count(turn) == 3 or secondary_diag.count(turn) == 3:
            return True
        for i in range(0, 3):
            if nboard[i].count(turn) == 3 or [nboard[0][i], nboard[1][i], nboard[2][i]].count(turn) == 3:
                return True
        return False

class TicTacToe():
    game_over = False
    board = [[" ", " ", " "], [" ", " ", " ",], [" ", " ", " "]]
    player1 = None
    player2 = None

    def __init__(self):
        pass

    def count_X(self):
        return board[0].count("X") + board[1].count("X") + board[2].count("X")

    def count_O(self):
        return board[0].count("O") + board[1].count("O") + board[2].count("O")

    def print_table(self):
        print("---------\n|", *board[0], "|\n|", *board[1], "|\n|", *board[2], "|\n---------", sep=" ")

    def player_move(self, player):
        if player.is_cpu():
            print(f'Making move level "{player.diff}"')
            move = player.pick_move(board)
            y, x = move.split()
            board[int(y) - 1][int(x) - 1] = player.turn
            self.print_table()
            self.evaluate_game()
            return
        while True:
            coords = input("Enter the coordinates: ").split()
            try:
                y = int(coords[0])
                x = int(coords[1])
                if x < 1 or x > 3 or y < 1 or y > 3:
                    raise IndexError
                if board[y - 1][x - 1] != " ":
                    print("This cell is occupied! Choose another one!")
                    continue
            except IndexError:
                print("Coordinates should be from 1 to 3!")
                continue
            except ValueError:
                print("You should enter numbers!")
                continue
            board[y - 1][x - 1] = player.turn
            self.print_table()
            break
        self.evaluate_game()

    def is_board_full(self):
        for line in board:
            if " " in line:
                return False
        return True

    def evaluate_game(self):
        global game_over
        main_diag = [board[0][0], board[1][1], board[2][2]]
        secondary_diag = [board[0][2], board[1][1], board[2][0]]
        if main_diag.count("X") == 3 or main_diag.count("O") == 3 or\
            secondary_diag.count("X") == 3 or secondary_diag.count("O") == 3:
            print(f"{board[1][1]} wins")
            game_over = True
        for i in range(0, 3):
            if board[i].count("X") == 3 or board[i].count("O") == 3:
                print(f"{board[i][0]} wins")
                game_over = True
            if [board[0][i], board[1][i], board[2][i]].count("X") == 3 or [board[0][i], board[1][i], board[2][i]].count("O") == 3:
                print(f"{board[0][i]} wins")
                game_over = True
        if self.is_board_full() and game_over == False:
            print("Draw")
            game_over = True

    def start_turns(self):
        while not game_over:
            if not game_over:
                self.player_move(player1)
            if not game_over:
                self.player_move(player2)
        self.start_game()

    def start_game(self):
        global board, player1, player2, game_over
        game_over = False
        board = [[" ", " ", " "], [" ", " ", " ",], [" ", " ", " "]]
        options = ["easy", "user", "medium", "hard"]
        while True:
            choice = input("Input command: ").split()
            if choice[0] == "exit":
                sys.exit()
            elif choice[0] != "start":
                print("Bad parameters!")
                continue
            else:
                if len(choice) != 3:
                    print("Bad parameters!")
                    continue
                if choice[1] not in options or choice[2] not in options:
                    print("Bad parameters!")
                    continue
            break
        player1 = human_player(turn="X") if choice[1] == "user" else cpu_player(turn="X", diff=choice[1])
        player2 = human_player(turn="O") if choice[2] == "user" else cpu_player(turn="O", diff=choice[2])
        self.print_table()
        self.start_turns()

TicTacToe().start_game()
