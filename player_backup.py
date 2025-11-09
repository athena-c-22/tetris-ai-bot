from board import Direction, Rotation, Action
from random import Random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)
                

            

    def choose_action(self, board):
        self.print_board(board)
        time.sleep(0.5)
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])

class GoodPlayer(Player):
    def move_to_target(self, board, t_pos, t_rot):
        if board.falling is None:
            return []
    
        moves = []
        rotation = 0
        while rotation < t_rot and board.falling is not None:
            board.rotate(Rotation.Clockwise)
            moves.append(Rotation.Clockwise)
            rotation += 1
            if board.falling is None:
                return moves
        while board.falling is not None and min(board.falling.cells)[0] < t_pos:
            board.move(Direction.Right)
            moves.append(Direction.Right)
        while board.falling is not None and min(board.falling.cells)[0] > t_pos:
            board.move(Direction.Left)
            moves.append(Direction.Left)
        if board.falling is not None:
            board.move(Direction.Drop)
            moves.append(Direction.Drop)
        return moves
    
    def count_holes(self, board):
        holes = 0
        for y in range(board.height):
            for x in range(board.width):
                if (x, y) not in board.cells and (x, y - 1) in board.cells:
                    holes += 1
        return holes

    def calculate_greatest_height(self, board):
        greatest_height = 0
        for y in range(board.height):
            for x in range(board.width):
                if (x, y) in board.cells:
                    height = board.height - y
                    greatest_height = max(greatest_height, height)
        return greatest_height

    def get_column_heights(self, board):
        heights = [0] * board.width

        for (x, y) in board.cells:
            column_height = board.height - y
            heights[x] = max(column_height, heights[x])

        return heights

    def calculate_bumpiness(self, board):
        bumpiness = 0
        heights = self.get_column_heights(board)
        for x in range(board.width - 1):
            bumpiness += abs(heights[x] - heights[x + 1])
        return bumpiness

    def calculate_lines_cleared(self, board):
        lines_cleared = 0
        for y in range(board.height):
            if board.line_full(y):
                lines_cleared += 1
        return lines_cleared

    def calculate_well_penalty(self, board):
        heights = self.get_column_heights(board)
        tolerance = 4 # After testing with different values, I found this value gives the best score.
        for x in range(board.width - 1):
            difference = abs(heights[x] - heights[x + 1])
            if difference > tolerance:
                return 1
        return 0

    def calculate_tetris_potential(self, board):
        score = 0
        for y in range(board.height):
            row = [x for x in range(board.width) if (x, y) not in board.cells]
            if len(row) == 1:
                score += 10
        return score

    def count_empty_pillars(self, board):
        empty_pillars = 0
        for x in range(board.width):
            column = [y for y in range(board.height) if (x, y) not in board.cells]
            if len(column) == board.height:
                empty_pillars += 1
        return empty_pillars

    def six_three_stack(self, board):
        six_three_penalty = 0
        for y in range(board.height):
            if (6, y) in board.cells:
                if not board.line_full(y):
                    six_three_penalty += 1
                else:
                    six_three_penalty -= 1
        return six_three_penalty

    def score_board(self, board):
        holes = self.count_holes(board)
        greatest_height = self.calculate_greatest_height(board)
        bumpiness = self.calculate_bumpiness(board)
        lines_cleared = self.calculate_lines_cleared(board)
        well_penalty = self.calculate_well_penalty(board)
        tetris_potential = self.calculate_tetris_potential(board) # Tetris is a move that completes four lines simultaneously with the use of the I-shaped tetromino.
        #empty_pillars = self.count_empty_pillars(board)
        #six_three_penalty = self.six_three_stack(board)
        score = 1000 - 20 * holes - len(board.cells) - greatest_height - 0.1 * bumpiness + 4 * lines_cleared - 100 * well_penalty + tetris_potential # The weights are chosen by myself based on my observations and through trial-and-error over the course of this coursework. For example, I noticed that despite the block structure having a smooth profile, if there are holes, it is hard to clear lines. So, I increased the relative weight of 'holes' to bumpiness.
        return score

    def choose_action(self, board):
        if board.falling is None:
            return None
        
        if board.falling is not None:
            highest_score = 0
            for x in range(board.width):
                for r in range(4):
                    if board.falling is None:
                        break
                    
                    sandbox = board.clone()
                    move = self.move_to_target(sandbox, x, r)
                    
                    sandbox.next = board.next
                    if sandbox.next is not None:
                        for next_x in range(sandbox.width):
                            for next_r in range(4):
                                next_sandbox = sandbox.clone()
                                next_move = self.move_to_target(next_sandbox, next_x, next_r)

                                score = self.score_board(next_sandbox)
                                if score > highest_score:
                                    highest_score = score
                                    best_move = move
            return best_move
        
    

    
    Action.Discard, # if next is much better than current?
    Action.Bomb,

    Direction.Left,
    Direction.Right,
    Direction.Down,
    Rotation.Anticlockwise,
    Rotation.Clockwise,


SelectedPlayer = GoodPlayer
