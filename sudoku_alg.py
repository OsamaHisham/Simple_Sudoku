def print_board(board):
    '''Prints the board'''   # --- Printing strings using the triple single quotes ''' or triple double quotes """ to enclose the string.
    boardString = ""
    for i in range(9):   # --- for i (rows) in range up until 9
        for j in range(9):   # --- for j (col) in range up until 9
            boardString += str(board[i][j]) + " "   # --- adding the position of the square ( [i][j] ) that is placed in a string and adding " " at the end to space out the values in the grid
            if (j+1)%3 == 0 and j != 0 and (j+1) != 9:
                boardString += " | "

            if j == 8:
                boardString += "\n"

        if (i+1)%3 == 0 and (i+1) != 9:
            boardString += "- - - - - - - - - - - \n"
    print(boardString)

# looking for blank spaces
def find_empty (board):    # --- defining a new function to find the empty places in the board by giving it ( board )
    '''Finds an empty cell and returns its position as a tuple'''
    for i in range (9):   # --- for i (rows) in range up until 9
        for j in range (9):   # --- for j (col) in range up until 9
            if board[i][j] == 0:   # --- using an if statment inside the for loops to state the condition we want to find along the board.
                return i,j

def valid(board, pos, num):
    '''Whether a number is valid in that cell, returns a bool if Tue or False'''

    # We need to check for 3 main things in the board and make sure we don't have any matching numbers inside them:

    # --- Check column ---
    for i in range(9):   # --- using a for loop in the range of rows in on the grid (i).
        if board[i][pos[1]] == num and (i, pos[1]) != pos:  # --- using an if statment. comparing if the board position of row ( i ) and row position value [ pos[1] ] is equal to the number we entered. and to make sure that it's not the exact position that we just inserted something into.
            return False   # --- and if that is true it would return a false

    # --- Check row --- ( Horizontally )
    for j in range(9):   # --- using a for loop in the range of col in on the grid (j).
        if board[pos[0]][j] == num and (pos[0], j) != pos: # --- using an if statment.comparing if the board at the col position value of [ pos[o] ] col ( j ) is equal to the number we entered. and to make sure that it's not the exact position that we just inserted something into.
            return False    # --- and if that is true it would return a false

    # --- Check box --- ( By using an integer division method to pin point the one of the small 9 boxes we got first to apply the conditions on )
    box_x = pos[1] // 3  # --- for the boxes in the x axis we are going to integer divide our pos [ 1 ] which is our colomn position by 3
    box_y = pos[0] // 3  # --- for the boxes in the y axis we are going to integer divide our pos [ 0 ] which is our row position by 3

    # Making for loops to loop throught the elements in each of the 9 boxes and check that they don't have matching numbers in them
    for i in range(box_y*3, box_y*3 + 3):  # --- for loop for i. here we multiplied box y by 3 to get the index of each element inside the small box and for the second range we added 3 in order to move down the elements that we have inside the small box
        for j in range(box_x * 3, box_x*3 + 3): # --- for loop for i. here we multiplied box x by 3 to get the index of each element inside the small box and for the second range we added 3 in order to move to the left of the elements that we have inside the small box
            if board[i][j] == num and (i,j) != pos:  # --- and if stament which will check while looping in the box if any other element in the box is equal to the one that we just added and that we are not going to check the same position that we added in.
                return False  # --- and if that is true it would return a false

    return True  # --- if all of these check are okay then we are going to return true

def solve(board):
    '''Solves the Sudoku board via the backtracking algorithm'''

    # --- We are going to do this recursively ( calling the function from inside of itself )
    # --- this whole empty function purpouse is to use either true or false indicating whether we found the solution or not
    empty = find_empty(board)
    if not empty:   # --- no empty spots are left so the board is solved
        return True

    # --- the looping algorithm to loop from 1 to 9 and attempt to fill them in our solution
    for nums in range(9):   # --- for loop for range 9
        if valid(board, empty,nums+1):    # --- condition checked which is the valid function defined bellow and is used to check whether this value is actually valid or not
            board[empty[0]][empty[1]] = nums+1  # --- what we will do is that we are going to place it on the board if the value is valid

            # --- recursively calling the defined function itself
            if solve(board):   # --- calling the solve function itself again after adding the solution and keep on trying until we find all the solutions or until we have looped through till 9 and non of them are valid.
                return True
            board[empty[0]][empty[1]] = 0   # --- here we are resetting the value added and backtracking to the last position after the loop returns a ( False )
    return False

if __name__ == '__main__':
    board =  [
        [0, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 8, 0, 0, 0, 7, 0, 9, 0],
        [6, 0, 2, 0, 0, 0, 5, 0, 0],
        [0, 7, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 4, 0],
        [0, 0, 5, 0, 0, 0, 6, 0, 3],
        [0, 9, 0, 4, 0, 0, 0, 7, 0],
        [0, 0, 6, 0, 0, 0, 0, 0, 0]
    ]
    
    print_board(board)
    solve(board) 
    print_board(board)
