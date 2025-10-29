"""
Tic-Tac-Toe (Project 2 Part C)

This program is a simple Tic-Tac-Toe game using classes and objects.
The user will play as X and the computer will play as O with a ML algorithm from a trained model from text file supplied.

Author: Andre Archer
Date: 10/29/2025
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # simple, works well

def train_tictactoe_model(filepath=None):

    """
    Function to train and output an ML model for tic-tac-toe best move prediction.
    The model is trained on a dataset where each row represents a board state (9 features) and the target is the best move index (0-8).

    Args:
        filepath: Path to the dataset file. If None, uses default path (shown below is case for my use).
    """

    #update this file path to where the data file is. I had to do the full filepath on my macbook for some reason
    if filepath is None:
        filepath = "/Users/andrearcher/Library/CloudStorage/OneDrive-UniversityofFlorida/Coursework/FA25/EGN5442 - Programming for Applied Data Science/project 2/project 2/tictac_single.txt"

    # Load dataset
    data = np.loadtxt(filepath)
    X = data[:, :-1]  #9 board positions
    y = data[:, -1]   #best move index

    #Split data to show performance (although this class isn't for that)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12)

    #Using random forest classifier because its easy to use
    model = RandomForestClassifier(n_estimators=100, random_state=12)
    model.fit(X_train, y_train)

    #Print the model score (accuracy)
    acc = model.score(X_test, y_test)
    print(f"Model trained. Test accuracy: {acc:.2f}")

    return model


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
        predict_move_with_model: Predicts the computer's move using the trained ML model.
        playGame: Runs the Tic-Tac-Toe game loop.
    """

    # the constructor
    def __init__(self, model = None):
        self.board = Board()
        self.turn = 'X'
        self.model = model

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
    
    # this method checks for a winner to end the game. A different method is used for checking every move for continuity
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
    
    def get_available_moves(self, board):
        moves = []
        for i in range(3):
            for j in range(3):
                if board.c[i][j] == " ":
                    moves.append((i, j))
        return moves

    #this part is sort of nice, since you can replace it with any decision method to get the same result
    def predict_move_with_model(self):
        # Convert current board to ML input format
        # I had to use AI to help me get this formatting correctly for prediction, but I thought that would be okay since this is not an ML course
        mapping = {'X': 1, 'O': -1, ' ': 0}
        flat_board = [mapping[self.board.c[i][j]] for i in range(3) for j in range(3)]
        X_input = np.array(flat_board).reshape(1, -1)

        # Predict best move index
        move_index = int(self.model.predict(X_input)[0])
        row, col = divmod(move_index, 3)

        # If predicted move is invalid (spot already filled), fall back to random valid move
        # This is important since it is not guaranteed the model will always predict a valid move
        if not self.validateEntry(row, col):
            valid_moves = self.get_available_moves(self.board)
            row, col = valid_moves[np.random.randint(len(valid_moves))]

        return (row, col)
    

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
                move = self.predict_move_with_model()
                entry = f"{move[0]},{move[1]}"
            row, col = map(int, entry.split(','))
            if self.validateEntry(row, col):
                self.board.c[row][col] = self.turn
                # check end condition immediately — do NOT switch if the game just ended
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
    #get model from training function
    model = train_tictactoe_model()

    #start game loop
    play_again = "y"
    while play_again[0].lower() == "y":
        game = Game(model=model)  # pass trained model into the game
        game.playGame()
        play_again = input("Do you want to play again? (y/n): ")

    print("Thank you for playing!")
    
# call to main() function
if __name__ == "__main__":
    main()
