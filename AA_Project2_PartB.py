"""
Tic-Tac-Toe (Project 2 Part B)

This program is a simple Tic-Tac-Toe game using classes and objects.
The user will play as X and the computer will play as O using the minimax algorithm.

Author: Andre Archer
Date: 10/29/2025
"""

# define Board class to building the Game Board:
class Board:
    """
    Class to represent the Tic-Tac-Toe board.

    Methods:
        printBoard: Prints the current state of the board.
    """
    # this constructor initiates the board with empty cells
    def __init__(self):
        self.c = [[" "," "," "],
                  [" "," "," "],
                  [" "," "," "]]
      
    # this method prints the board. Recall that class methods are functions
    def printBoard(self):
        # it first prints the BOARD_HEADER constant
        # BOARD_HEADER constant
        BOARD_HEADER = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"
        print(BOARD_HEADER)

        # using a for-loop, it increments through the rows
        for i in range(3):
            print(f"| {i} |", end="")
            for j in range(3):
                print(f" {self.c[i][j]} |", end="")
            print("\n-----------------")

# define Game class to implement the Game Logic:
class Game:
    """
    Class to manage the Tic-Tac-Toe game logic.
    Methods:
        switchPlayer: Switches the current player.
        validateEntry: Validates the user's move entry.
        checkFull: Checks if the board is full.
        checkWin: Checks for a winner.
        checkEnd: Checks if the game has ended.
        is_winner: Helper to check if a player has won.
        get_available_moves: Returns a list of available moves.
        minimax: Implements the minimax algorithm for optimal move selection.*
        minimax_tictactoe: Wrapper for minimax to get the best move for the current player.*
        playGame: Runs the Tic-Tac-Toe game loop.

        *These two are very similar to the algorithm used from DeepML, but are implemented here using lists instead of np.arrays.
    """
    # the constructor
    def __init__(self):
        self.board = Board()
        self.turn = 'X'

    # this method switches players 
    def switchPlayer(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'
    
    # this method validates the user's entry
    def validateEntry(self, row, col):
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        if self.board.c[row][col] != " ":
            return False
        return True

    # this method checks if the board is full
    def checkFull(self):
        for i in range(3):
            for j in range(3):
                if self.board.c[i][j] == " ":
                    return False
        return True
    
    # this method checks for a winner to end the game
    def checkWin(self):
        # Check the rows and columns of the board
        for i in range(3):
            # Check if rows are the same, but not empty
            if self.board.c[i][0] == self.board.c[i][1] == self.board.c[i][2] != " ":
                return True
            # Check if columns are the same, but not empty
            if self.board.c[0][i] == self.board.c[1][i] == self.board.c[2][i] != " ":
                return True 
        # Check the diagonals of the board
        if self.board.c[0][0] == self.board.c[1][1] == self.board.c[2][2] != " ": # Bottom left to top right
            return True
        if self.board.c[0][2] == self.board.c[1][1] == self.board.c[2][0] != " ": # Top left to bottom right
            return True
        return False
        

    # this method checks if the game has met an end condition by calling checkFull() and checkWin()
    # hint: you can call a class method using self.method_name() within another class method, e.g., self.checkFull()
    def checkEnd(self):
        if self.checkFull() or self.checkWin():
            return True
        return False
    

    #setting up minimax algorithm for AI player
    #helper to check every move is there is a winner, this is used for game continuity, not to end the game
    def is_winner(self, board, player):
        # Check rows, columns, and diagonals for a win
        for i in range(3):
            if all(board.c[i][j] == player for j in range(3)):
                return True
            if all(board.c[j][i] == player for j in range(3)):
                return True
        if all(board.c[i][i] == player for i in range(3)):
            return True
        if all(board.c[i][2 - i] == player for i in range(3)):
            return True
        return False
    
    #helper to get available moves
    def get_available_moves(self, board):
        moves = []
        for i in range(3):
            for j in range(3):
                if board.c[i][j] == " ":
                    moves.append((i, j))
        return moves

    #minimax algorithm implementation
    def minimax(self, board, player, maximizing):  # define minimax method on the Game class; takes board, current player, and whether we're maximizing
        if self.is_winner(board, 'X'): return 1, None  
        if self.is_winner(board, 'O'): return -1, None  
        if self.checkFull(): return 0, None  
        moves = self.get_available_moves(board) 

        if maximizing:  # maximizing mode (trying to maximize score)
            best_score, best_move = -float('inf'), None  # initialize best score to negative infinity and no best move yet
            for i, j in moves:  # iterate over each available move (row i, column j)
                board.c[i][j] = 'X'  
                score, _ = self.minimax(board, 'O', False)  # recursively call minimax for the opponent ('O') as minimizing
                board.c[i][j] = ' '  #undo the move (reset the cell to empty)
                if score > best_score: 
                    best_score, best_move = score, (i, j) 
            return best_score, best_move  # after exploring moves, return the best score and corresponding move
        
        else:  # minimizing node (trying to minimize score)
            best_score, best_move = float('inf'), None  # initialize best score to positive infinity and no best move yet
            for i, j in moves:          #iterate over each available move (row i, column j)
                board.c[i][j] = 'O'
                score, _ = self.minimax(board, 'X', True)  # recursively call minimax for the opponent ('X') as maximizing
                board.c[i][j] = ' '  #undo the move (reset the cell to empty)
                if score < best_score:
                    best_score, best_move = score, (i, j)
            return best_score, best_move # after exploring moves, return the best score and corresponding move

    #get best move for current player using minimax
    def minimax_tictactoe(self, board, player):
        maximizing = (player == 'X')
        _, move = self.minimax(board, player, maximizing)
        return move


    # this method runs the tic-tac-toe game
     # hint: you can call a class method using self.method_name() within another class method
    def playGame(self):

        while not self.checkEnd():
            self.board.printBoard()
            # need to set up game where user is X and computer is O.
            # player starts, then computer makes move using minimax
            if self.turn == 'X':
                entry = input(f"Player {self.turn}, enter row and column separated by a comma (e.g., 0,1): ")
            else:
                print(f"Computer {self.turn} is making a move...")
                move = self.minimax_tictactoe(self.board, self.turn)
                entry = f"{move[0]},{move[1]}"
            row, col = map(int, entry.split(','))
            if self.validateEntry(row, col):
                self.board.c[row][col] = self.turn
                #check end condition — do NOT switch if the game just ended
                if self.checkWin() or self.checkFull():
                    break
                self.switchPlayer()
            else:
                print("Invalid entry. Try again.")
        self.board.printBoard()
        if self.checkWin():
            print(f"Player {self.turn} wins!")
        else:
            print("It's a tie!")


# main function
def main():
    # first initializes a variable to repeat the game
    play_again = "y"
    while play_again[0].lower() == "y":

    # using while-loop that runs until the user says no for another game
        game = Game()  # create a new Game object
        game.playGame()  # call the playGame method to start the game
        play_again = input("Do you want to play again? (y/n): ")  # ask if the user wants to play again

    # goodbye message 
    print("Thank you for playing!")
    
# call to main() function
if __name__ == "__main__":
    main()
