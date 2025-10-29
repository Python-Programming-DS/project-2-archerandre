"""
Tic-Tac-Toe (Project 2 Part A)

This program is a simple Tic-Tac-Toe game using classes and objects.

Author: Andre Archer
Date: 10/29/2025
"""

# define Board class to building the Game Board:
class Board:
    """
    Class to represent the Tic-Tac-Toe board.
    methods:
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
        playGame: Runs the Tic-Tac-Toe game loop.
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
    
    # this method checks for a winner
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

    # this method runs the tic-tac-toe game
     # hint: you can call a class method using self.method_name() within another class method
    def playGame(self):
        while not self.checkEnd():
            self.board.printBoard()
            entry = input(f"Player {self.turn}, enter row and column separated by a comma (e.g., 0,1): ")
            row, col = map(int, entry.split(','))
            if self.validateEntry(row, col):
                self.board.c[row][col] = self.turn

                # check end condition immediately, do NOT switch if the game just ended
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

    #end game
    print("Thank you for playing!")
    
# call to main() function
if __name__ == "__main__":
    main()
