import chess

class MinimaxAI():
    def __init__(self, depth, color=chess.BLACK):
        self.color = color
        self.max_depth = depth
        self.nodes_visited = 0
        self.visited = {}

    # Returns the move with the maximum expected value via minimax algorithm
    def choose_move(self, board):

        final_best_move = None

        for i in range(1, self.max_depth+1):
            best_val, best_move = self.max_val(board, 0, i, True)
            print("At depth " + str(i) + ", Minimax recommends move " + str(best_move))
            print("Visited " + str(self.nodes_visited) + " nodes to produce move with value " + str(best_val))
            self.visited.clear()

        self.nodes_visited = 0
        final_best_move = best_move

        return final_best_move


    #Returns whether or not minimax should continue searching this branch
    def cutoff_test(self, board, depth, depth_lim):
        return (depth >= depth_lim or board.is_game_over())


    # Returns maximum expected value of possible values from given state
    def max_val(self, board, curr_depth, depth_lim, return_move=False):
        if self.cutoff_test(board, curr_depth, depth_lim):
            return self.get_val(board)

        max_val = float("-inf")
        best_move = None
        for move in board.legal_moves:
            board.push(move)

            #Checks hash
            if board.fen() not in self.visited:
                val = self.min_val(board, curr_depth + 1, depth_lim)
                self.visited[board.fen()] = val
            else:
                val = self.visited[board.fen()]
            if val > max_val:
                max_val = val
                best_move = move
            self.nodes_visited += 1
            board.pop()
        if return_move:
            return max_val, best_move
        else:
            return max_val


    # Returns minimum expected value of possible values from given state
    def min_val(self, board, curr_depth, depth_lim):
        if self.cutoff_test(board, curr_depth, depth_lim):
            return self.get_val(board)

        min_val = float("inf")

        for move in board.legal_moves:
            board.push(move)
            if board.fen() not in self.visited:
                val = self.max_val(board, curr_depth + 1, depth_lim)
                self.visited[board.fen()] = val
            else:
                val = self.visited[board.fen()]

            if val < min_val:
                min_val = val
            self.nodes_visited += 1
            board.pop()
        return min_val

    # Returns the value of the current board position (1000 for win, 0 for draw,
    # -1000 for loss, and material_heuristic(board) for incomplete game)
    def get_val(self, board):
        res = board.result()
        if res == "*":
            return self.material_heuristic(board)
        if res == "1-0":
            if self.color == chess.BLACK:
                return -1000
            else:
                return 1000
        if res == "0-1":
            if self.color == chess.BLACK:
                return 1000
            else:
                return -1000
        if res == "1/2-1/2":
            return 0

    # Returns a modified heuristic value of the board based on material values
    def material_heuristic(self, board):
        val = 0

        val += self.get_material_value(board, self.color)
        val -= self.get_material_value(board, not self.color)

        if board.is_check():
            if board.turn == self.color:
                val -= 1
            else:
                val += 1
        return val

    # Returns the total material value of a given color
    def get_material_value(self, board, color):
        p_val = 1
        k_val = 3
        b_val = 3
        r_val = 5
        q_val = 9

        # Arbitrary point at which to increase bishop value since it is the endgame
        if self.count_pieces(board, color) < 6:
            b_val += 1

        val = 0

        val += p_val * len(board.pieces(chess.PAWN, color))
        val += k_val * len(board.pieces(chess.KNIGHT, color))
        val += b_val * len(board.pieces(chess.BISHOP, color))
        val += r_val * len(board.pieces(chess.ROOK, color))
        val += q_val * len(board.pieces(chess.QUEEN, color))
        #print("Calculated value of " + str(val) + " for color " + str(color))
        return val

    # Returns the number of pieces of a given color left on the board
    def count_pieces(self, board, color):
        pieces = frozenset([chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN])
        count = 0

        for piece in pieces:
            count += len(board.pieces(piece, color))

        return count
