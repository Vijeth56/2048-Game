import random


SIZE = 4
WINNING_TILE = 2048
MAX_DEPTH = 5

# Directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Heuristic weights
EMPTY_WEIGHT = 100
MONOTONICITY_WEIGHT = 1
SMOOTHNESS_WEIGHT = 1

# Board class
class Board:
    def _init_(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0

    def place_random_tile(self):
        empty_cells = [(i, j) for i in range(SIZE) for j in range(SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.grid[row][col] = random.choice([2, 4])

    def move(self, direction):
        if direction == UP:
            self.grid = self.transpose(self.grid)
            self.move_left()
            self.grid = self.transpose(self.grid)
        elif direction == DOWN:
            self.grid = self.transpose(self.grid)
            self.reverse_rows()
            self.move_left()
            self.reverse_rows()
            self.grid = self.transpose(self.grid)
        elif direction == LEFT:
            self.move_left()
        elif direction == RIGHT:
            self.reverse_rows()
            self.move_left()
            self.reverse_rows()

    def move_left(self):
        for i in range(SIZE):
            merged = [False] * SIZE
            for j in range(1, SIZE):
                if self.grid[i][j] != 0:
                    k = j
                    while k > 0 and self.grid[i][k - 1] == 0:
                        self.grid[i][k - 1] = self.grid[i][k]
                        self.grid[i][k] = 0
                        k -= 1
                    if k > 0 and self.grid[i][k - 1] == self.grid[i][k] and not merged[k - 1]:
                        self.grid[i][k - 1] *= 2
                        self.score += self.grid[i][k - 1]
                        self.grid[i][k] = 0
                        merged[k - 1] = True

    def reverse_rows(self):
        for i in range(SIZE):
            self.grid[i] = list(reversed(self.grid[i]))

    def transpose(self, grid):
        return [list(row) for row in zip(*grid)]

    def get_empty_cells(self):
        return [(i, j) for i in range(SIZE) for j in range(SIZE) if self.grid[i][j] == 0]

    def is_game_over(self):
        if self.get_empty_cells():
            return False

        for i in range(SIZE):
            for j in range(SIZE):
                if self.can_tile_merge(i, j):
                    return False

        return True

    def can_tile_merge(self, row, col):
        tile_value = self.grid[row][col]
        if col < SIZE - 1 and self.grid[row][col + 1] == tile_value:
            return True
        if row < SIZE - 1 and self.grid[row + 1][col] == tile_value:
            return True
        return False

    def get_score(self):
        return self.score

    def get_best_move(self):
        best_move = -1
        best_score = -float('inf')
        for move in range(4):
            if self.can_move(move):
                new_board = Board()
                new_board.grid = [row[:] for row in self.grid]
                new_board.score = self.score
                new_board.move(move)
                score = new_board.minimax(MAX_DEPTH, -float('inf'), float('inf'), False)
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_move

    def minimax(self, depth, alpha, beta, is_maximizing):
        if depth == 0 or self.is_game_over():
            return self.evaluate()

        if is_maximizing:
            max_score = -float('inf')
            for move in range(4):
                if self.can_move(move):
                    new_board = Board()
                    new_board.grid = [row[:] for row in self.grid]
                    new_board.score = self.score
                    new_board.move(move)
                    score = new_board.minimax(depth - 1, alpha, beta, False)
                    max_score = max(max_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return max_score
        else:
            min_score = float('inf')
            empty_cells = self.get_empty_cells()
            for cell in empty_cells:
                row, col = cell
                for value in [2, 4]:
                    self.grid[row][col] = value
                    score = self.minimax(depth - 1, alpha, beta, True)
                    min_score = min(min_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        self.grid[row][col] = 0
                        break
                    self.grid[row][col] = 0
            return min_score

    def evaluate(self):
        empty_cells = len(self.get_empty_cells())
        monotonicity = self.calculate_monotonicity()
        smoothness = self.calculate_smoothness()
        return (empty_cells * EMPTY_WEIGHT) + (monotonicity * MONOTONICITY_WEIGHT) + (smoothness * SMOOTHNESS_WEIGHT)

    def calculate_monotonicity(self):
        # Calculate the sum of the differences between adjacent tiles in each row and column
        row_differences = sum(abs(self.grid[i][j] - self.grid[i][j + 1]) for i in range(SIZE) for j in range(SIZE - 1))
        column_differences = sum(abs(self.grid[i][j] - self.grid[i + 1][j]) for i in range(SIZE - 1) for j in range(SIZE))
        return row_differences + column_differences

    def calculate_smoothness(self):
        # Calculate the sum of squared differences between adjacent tiles in each row and column
        row_differences = sum((self.grid[i][j] - self.grid[i][j + 1]) ** 2 for i in range(SIZE) for j in range(SIZE - 1))
        column_differences = sum((self.grid[i][j] - self.grid[i + 1][j]) ** 2 for i in range(SIZE - 1) for j in range(SIZE))
        return row_differences + column_differences

    def can_move(self, direction):
        temp_board = Board()
        temp_board.grid = [row[:] for row in self.grid]
        temp_board.move(direction)
        return temp_board.grid != self.grid


# Game class
class Game:
    def _init_(self):
        self.board = Board()
        self.play_game()

    def play_game(self):
        while not self.board.is_game_over():
            move = self.board.get_best_move()
            self.board.move(move)
            self.board.place_random_tile()
            self.print_board()

    def print_board(self):
        print("Score:", self.board.get_score())
        for row in self.board.grid:
            print(row)
        print()

# Main function
def main():
    game = Game()

if _name_ == "_main_":
    main()
