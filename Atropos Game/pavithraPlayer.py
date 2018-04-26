#Atropos Game Player: pavithraPlayer
#Author: Pavithra Raghavan

#================================================================================================
#Importing Packages
#================================================================================================
import numpy as np
import sys
import re
import copy as cp
import math
import random


#================================================================================================
#Utility Functions
#================================================================================================


#This function parses the input string and returns a matrix
#inputs:-
#   new_words: Vectorized form of input sys.argsv[1]
#                   example input: ['13', '332', '1133', '33102', '131123', '3111122', '11111123', '311212122', '12121212', 'LastPlay:(1,3,4,2)']
#output:-
#   board: An int matrix with the colors as values. Left Justified. With zero padding in the unoccupied triangle
def parseInput(new_words):
    tokens = list(new_words)                                            #Converting the input into a list of tokens: each element like: '3111122'
    tokens_list = [list([int(x) for x in a]) for a in tokens[0:-1]]     #Splitting each element into a list of integers. above element converted to:  [3, 1, 1, 1, 1, 2, 2]
    length = len(sorted(tokens_list,key=len, reverse=True)[0])          #finding the maximum length  --> this will be the length of the board matrix
    board =np.array([xi+[0]*(length-len(xi)) for xi in tokens_list])    #initialize board matrix with values of the input string to the matrix. Left Justified.
    for a in range(len(board)-2,-1,-1):                                 #Move the contents of the last row to the right
        board[-1][a+1] = board[-1][a] 
    board[-1][0] = 0                                                    #The first element of the bottom row made zero
    #print(tokens)
    return(board)                                                       #return board matrix


#This function returns true if the circle is not colored
#input:-
#   circle: An integer
#output:-
#   True if input is zero, False otherwise
def isUncolored(circle):
    if circle == 0:         #if input is zero, circle is not colored. Return True.
        return(True)
    else:                   #False otherwise
        return(False)


#This function returns true if the circle is inside the board, i.e. if it is a valid playable location on the board
#Inputs:-
#   x,y,z,size: int
#output:-
#   True if the input satisfies the board rule: x+y+z=size+2
def isInside(x,y,z,size):
    if x<0 or y<0 or z<0:   #outside the triangle
        return False
    elif x+y+z == size+2:    #inside the board with valid x,y,z
        return True
    else:                    #invalid x,y,z
        return False


#This function returns true if the color forms 3-colored-triangle:
#Inputs:-
#   one, two, color: int
#output:-
#   True if they are of 3 different colors (1=Red, 2=Blue, 3=Green)
def deathTriangle(one, two, color):
    triangleColorSum = 6        #sum of colors of a 3-colored-triangle
    if one!=two and one + two + color == triangleColorSum:
        return True
    else:
        return False


#This function returns all the adjacent colors of a given input
#input:-
#   board: matrix
#   x,y,z: int representing the coordinates of the given input
#output:-
#   Returns the following adjacent elements in the same order
#       (topLeft, topRight, bottomLeft, bottomRight, Left, Right)
def adjacentCircleColors(board, x,y,z):
    topLeft = -1                #initialize the colors with -1
    topRight = -1
    bottomLeft = -1
    bottomRight = -1
    Left = -1
    Right = -1
    
    #Get the color of topLeft, topRight, bottomLeft, bottomRight, Left, Right:
    if isInside(x+1,y-1,z, size = x+y+z-2):     #check if the coordinates of top-left circle lies inside the (playable) board
        topLeft = board[x+1][y-1]               #Assign the color of the top-left circle
    if isInside(x+1,y,z-1, size = x+y+z-2):
        topRight = board[x+1][y]
    if isInside(x-1,y,z+1, size = x+y+z-2):
        bottomLeft = board[x-1][y]
    if isInside(x-1,y+1,z, size = x+y+z-2):
        bottomRight = board[x-1][y+1]
    if isInside(x,y-1,z+1, size = x+y+z-2):
        Left = board[x][y-1]
    if isInside(x,y+1,z-1, size = x+y+z-2):
        Right = board[x][y+1]
    
    return(topLeft, topRight, bottomLeft, bottomRight, Left, Right)


#This function returns true if a color is safe in a location
#inputs:-
#   board: matrix
#   color: color of the given circle
#   x,y,z: int coordinates of the given circle
#output:-
#   True if coloring the given circle with 'color' doesn't form a 3-colored-triangle
def isSafe(board, color, x,y,z):
    topLeft, topRight, bottomLeft, bottomRight, Left, Right = adjacentCircleColors(board, x,y,z)       #get the adjacent circle colors
    
    #check if 'color' is safe for the location x,y,z by checking if a 3-colored-triangle is formed with adjacent circle:
    if deathTriangle(topRight, Right, color) or deathTriangle(Right, bottomRight, color) or deathTriangle(bottomRight, bottomLeft, color) or deathTriangle(bottomLeft, Left, color) or deathTriangle(Left, topLeft, color) or deathTriangle(topLeft, topRight, color):
        return(False)
    else:
        return(True)


#This function returns True if there are no adjacent (uncolored) circles for a given location
#inputs:-
#   board: matrix
#   x,y,z: int coordinates of the given circle
#output:-
#   True if there are no adjacent circles which are unclored
def terminateGame(board, x,y,z):
    a = adjacentCircleColors(board, x,y,z)
    if 0 in a:                 #if there is at least one uncolored adjacent circle, return false
        return(False)
    else:
        return(True)



#================================================================================================
#Functions for Search Algorithm
#================================================================================================

#This function is the static evaluator for the algorithm
#   stores the number of safe moves as the score
#inputs:-
#   board: matrix
#   x,y,z: int coordinates of the given circle
#output:-
#   returns the number of possible safe moves after this coordinate is colored (either 1 or 2 or 3)
def evaluator(board, x,y,z):
    score = 0
    topLeft, topRight, bottomLeft, bottomRight, Left, Right = adjacentCircleColors(board, x,y,z)
    
    for color in range(1,4):                                            #for every possible color
        if(isUncolored(topLeft) and isSafe(board, color, x+1,y-1,z)):   #check if it is a safe move
            score = score+1                                             #increment the score if it is a safe move
        if(isUncolored(topRight) and isSafe(board, color, x+1,y,z-1)):
            score = score+1
        if(isUncolored(bottomLeft) and isSafe(board, color, x-1,y,z+1)):
            score = score+1
        if(isUncolored(bottomRight) and isSafe(board, color, x-1,y+1,z)):
            score = score+1
        if(isUncolored(Left) and isSafe(board, color, x,y-1,z+1)):
            score = score+1
        if(isUncolored(Right) and isSafe(board, color, x,y+1,z-1)):
            score = score+1
    
    return(score)


#This is the max function
#inputs:-
#   depth: look-ahead depth
#   board: matrix
#   x,y,z: int coordinates of the given circle
#output:-
#   maxColor: color for the return circle
#   maxPostition: position with respect to the given coordinates
#   maxValue: value of the score from evaluator
def maxValue(depth, board, x,y,z):
    #Base case
    if terminateGame(board, x,y,z):                                             #if there is no uncolored adjacent circles, return
        return (None, None, None)

    if depth == 1:                                                              #if look-ahead depth is 1, evaltuate the board
        return (None, None, evaluator(board, x,y,z))
    
    topLeft, topRight, bottomLeft, bottomRight, Left, Right = adjacentCircleColors(board, x,y,z)    #get the adjacent circle colors
    scores = -1*np.ones((3,6))                                                  #initialize the scores matrix to -1.
    
    for color in range(1,4):                                                    #for each color, find the score which is what the minimizer would choose
        if isUncolored(topLeft) and isSafe(board, color, x+1,y-1,z):            #check if top-left circle is safe
            new_board = cp.deepcopy(board)                                      #create a copy of the board and incorporate this pseudo-move and send to minimizer
            new_board[x+1][y-1] = color
            temp1, temp2, score1 = minValue(depth-1, new_board, x+1, y-1,z)
            if score1==None:                                                    #if game was terminated by minimizer, send to evaluator
                scores[color - 1][0] = evaluator(board, x+1,y-1,z)
            else:                                                               #else, store the scores given by minimizer
                scores[color - 1][0] = score1
                
        if isUncolored(topRight) and isSafe(board, color, x+1,y,z-1):
            new_board = cp.deepcopy(board)
            new_board[x+1][y] = color
            temp1, temp2, score1 = minValue(depth-1, new_board, x+1, y, z-1)
            if score1==None:
                scores[color - 1][1] = evaluator(new_board, x+1,y,z-1)
            else:
                scores[color - 1][1] = score1
                
        if isUncolored(bottomLeft) and isSafe(board, color, x-1,y,z+1):
            new_board = cp.deepcopy(board)
            new_board[x-1][y] = color
            temp1, temp2, score1 = minValue(depth-1, new_board, x-1,y,z+1)
            if score1==None:
                scores[color - 1][2] = evaluator(new_board, x-1,y,z+1)
            else:
                scores[color - 1][2] = score1
                
        if isUncolored(bottomRight) and isSafe(board, color, x-1,y+1,z):
            new_board = cp.deepcopy(board)
            new_board[x-1][y+1] = color
            temp1, temp2, score1 = minValue(depth-1, new_board, x-1,y+1,z)
            if score1==None:
                scores[color - 1][3] = evaluator(new_board, x-1,y+1,z)
            else:
                scores[color - 1][3] = score1
                
        if isUncolored(Left) and isSafe(board, color, x,y-1,z+1):
            new_board = cp.deepcopy(board)
            new_board[x][y-1] = color
            temp1, temp2, score1 = minValue(depth-1, new_board, x,y-1,z+1)
            if score1==None:
                scores[color - 1][4] = evaluator(new_board, x,y-1,z+1)
            else:
                scores[color - 1][4] = score1
                
        if isUncolored(Right) and isSafe(board, color, x,y+1,z-1):
            new_board = cp.deepcopy(board)
            new_board[x][y+1] = color
            temp1, temp2, score1 = minValue(depth-1, new_board, x,y+1,z-1)
            if score1==None:
                scores[color - 1][5] = evaluator(new_board, x,y+1,z-1)
            else:
                scores[color - 1][5] = score1
    maxValue = scores.max()
    if(maxValue!=-1):                                                   #if there us at least one safe neighbor
        temp = np.argmax(scores)
        maxColor = math.floor(temp/6)
        maxPostition = temp%6                                              #order: (topLeft, topRight, bottomLeft, bottomRight, Left, Right)
    else:                                                               #if all uncolored neighbors are unsafe, choose to lose
        if(isUncolored(topLeft)):
            maxPostition = 0
        elif(isUncolored(topRight)):
            maxPostition = 1
        elif(isUncolored(bottomLeft)):
            maxPostition = 2
        elif(isUncolored(bottomRight)):
            maxPostition = 3
        elif(isUncolored(Left)):
            maxPostition = 4
        elif(isUncolored(Right)):
            maxPostition = 5
        else:
            maxPostition = -1
        maxColor = random.randint(1,4)
        maxValue = 0
    return(maxColor, maxPostition, maxValue)



#This is the min function:
#inputs:-
#   depth: look-ahead depth
#   board: matrix
#   x,y,z: int coordinates of the given circle
#output:-
#   minColor: color for the return circle
#   minPostition: position with respect to the given coordinates
#   minValue: value of the score from evaluator
def minValue(depth, board, x,y,z):
    #Base case
    if terminateGame(board, x,y,z):                                             #if there is no uncolored adjacent circles, return
        return (None, None, None)
    
    if depth == 1:                                                              #if look-ahead depth is 1, evaltuate the board
        return (None, None, evaluator(board, x,y,z))
    
    topLeft, topRight, bottomLeft, bottomRight, Left, Right = adjacentCircleColors(board, x,y,z)    #get the adjacent circle colors
    scores = 100*np.ones((3,6))                                                 #initialize the scores matrix to 100
    for color in range(1,4):                                                    #for each color, find the score which is what the minimizer would choose
        if isUncolored(topLeft) and isSafe(board, color, x+1,y-1,z):            #check if top-left circle is safe
            new_board = cp.deepcopy(board)                                      #create a copy of the board and incorporate this pseudo-move and send to minimizer
            new_board[x+1][y-1] = color
            temp1, temp2, score1 = maxValue(depth-1, new_board, x+1,y-1,z)
            if score1==None:                                                    #if game was terminated by maximizer, send to evaluator
                scores[color - 1][0] = evaluator(new_board, x+1,y-1,z)
            else:                                                               #else, store the scores given by maximizer
                scores[color - 1][0] = score1
                
        if isUncolored(topRight) and isSafe(board, color, x+1,y,z-1):
            new_board = cp.deepcopy(board)
            new_board[x+1][y] = color
            temp1, temp2, score1 = maxValue(depth-1, new_board, x+1,y,z-1)
            if score1==None:
                scores[color - 1][1] = evaluator(new_board, x+1,y,z-1)
            else:
                scores[color - 1][1] = score1
                
        if isUncolored(bottomLeft) and isSafe(board, color, x-1,y,z+1):
            new_board = cp.deepcopy(board)
            new_board[x-1][y] = color
            temp1, temp2, score1 = maxValue(depth-1, new_board, x-1,y,z+1)
            if score1==None:
                scores[color - 1][2] = evaluator(new_board, x-1,y,z+1)
            else:
                scores[color - 1][2] = score1
                
        if isUncolored(bottomRight) and isSafe(board, color, x-1,y+1,z):
            new_board = cp.deepcopy(board)
            new_board[x-1][y+1] = color
            temp1, temp2, score1 = maxValue(depth-1, new_board, x-1,y+1,z)
            if score1==None:
                scores[color - 1][3] = evaluator(new_board, x-1,y+1,z)
            else:
                scores[color - 1][3] = score1
                
        if isUncolored(Left) and isSafe(board, color, x,y-1,z+1):
            new_board = cp.deepcopy(board)
            new_board[x][y-1] = color
            temp1, temp2, score1 = maxValue(depth-1, new_board, x,y-1,z+1)
            if score1==None:
                scores[color - 1][4] = evaluator(new_board, x,y-1,z+1)
            else:
                scores[color - 1][4] = score1
                
        if isUncolored(Right) and isSafe(board, color, x,y+1,z-1):
            new_board = cp.deepcopy(board)
            new_board[x][y+1] = color
            temp1, temp2, score1 = maxValue(depth-1, new_board, x,y+1,z-1)
            if score1==None:
                scores[color - 1][5] = evaluator(new_board, x,y+1,z-1)
            else:
                scores[color - 1][5] = score1
    temp = np.argmin(scores)
    minColor = math.floor(temp/6)
    minPostition = temp%6                                                           #order: (topLeft, topRight, bottomLeft, bottomRight, Left, Right)
    minValue = scores.min()
    if minValue == -1:
        minValue=0
    return(minColor, minPostition, minValue)



#================================================================================================
#Output Utility Functions
#================================================================================================

#This function chooses a random available circle and returns coordinates with safe color
#inputs:-
#   board: matrix
#   prevMove: vector representing the lastPlay
#outputs:-
#   color and coordinates for the next move
def chooseRandomCircle(board, prevMove):
    oldX = prevMove[1]              #get the x from laastPlay
    oldY = prevMove[2]              #get the y from laastPlay
    size = oldX + oldY + prevMove[3]    #get size of the game board + 2
    for i in range(0, len(board)-1):
        for j in range(0,len(board[i])-1):
            for col in range(1,4):
                if isInside(i,j,size - i - j, size-2) and isUncolored(board[i][j]) and isSafe(board, col, i,j,size - i - j):   #check if there is a safe uncolored circle in the board
                    return (col, i, j, size - i - j)

    for i in range(0, len(board)-1):
        for j in range(0,len(board[i])-1):
            for col in range(1,4):
                if isInside(i,j,size - i - j, size-2) and isUncolored(board[i][j]):   #Lose: return even if it is not safe
                    return (col, i, j, size - i - j)

#This function parses the output from maximizer and returns coordinates with color
#inputs:-
#   color: int representing the color of the given circle
#   prevMove: vector representing the lastPlay
#   nextPosition: integer representing location w.r.t lastPlay. Order: (topLeft, topRight, bottomLeft, bottomRight, Left, Right)
#   board: matrix
#outputs:-
#   color and coordinates for the next move
def parseNextMove(color, prevMove, nextPosition, board) :
    oldX = prevMove[1]              #get the x from laastPlay
    oldY = prevMove[2]              #get the y from laastPlay
    size = oldX + oldY + prevMove[3]    #get size of the game board + 2
    
    if nextPosition == 0:       #topLeft
        newX = oldX+1           #get the coordinates w.r.t lastPlay
        newY = oldY-1
        newZ = size - newX - newY
    elif nextPosition == 1:  #topRight
        newX = oldX+1
        newY = oldY
        newZ = size - newX - newY
    elif nextPosition == 2:  #bottomLeft
        newX = oldX-1
        newY = oldY
        newZ = size - newX - newY
    elif nextPosition == 3:  #bottomRight
        newX = oldX-1
        newY = oldY+1
        newZ = size - newX - newY
    elif nextPosition == 4:  #Left
        newX = oldX
        newY = oldY-1
        newZ = size - newX - newY
    elif nextPosition == 5:  #Right
        newX = oldX
        newY = oldY+1
        newZ = size - newX - newY
    else:                           #if there is no safe adjacent uncolored circle
        chooseRandomCircle(board, prevMove)
    return(color, newX, newY, newZ)



#This function gets next move and returns it
#inputs:-
#   board: matrix
#   lastPlay: lastPlay from the input
#   depth: look-ahead depth
#output:
#   color and coordinates for the next move
def nextMove(board, lastPlay, depth):
    c = lastPlay[0]             #get the color and coordinates of the lastPlay
    x = lastPlay[1]
    y = lastPlay[2]
    z = lastPlay[3]
    if terminateGame(board, x,y,z):                                             #if there is no uncolored adjacent circles, return
        return chooseRandomCircle(board, lastPlay)
    else:
        color, position, value = maxValue(depth, board, x,y,z)          #get the result from the search algorithm    for look-ahead-depth=depth
        return parseNextMove(color+1, lastPlay, position, board)



#================================================================================================
#Main
#================================================================================================

#msg = "Given board: " + sys.argv[1] + "\n";
#sys.stderr.write(msg);
#sys_argv = "[13][302][1003][30002][100003][3000002][10000003][300000002][12121212]LastPlay:null"


#=====Split the input argument into words
words = sys.argv[1].split("]")                #split the input args based on "]" and store in a list: words
new_words = [s.strip('[') for s in words]  #remove "[" from list (words)
old_board = parseInput(new_words)          #get an integer matrix with the positions of circles in input
board = old_board[::-1]                    #reverse the board, so that height starts from top
board[0][0] = -1

#=====Decide the next move based on last play


#look-ahead-depth
depth = 5

if new_words[-1] == "LastPlay:null":       #if this is the first play, return random output
    col=0
    size = len(board) -2
    x = math.floor((size )/2)
    y = 1
    topLeft, topRight, bottomLeft, bottomRight, Left, Right = adjacentCircleColors(board, x,y,size-x-y+2)
    #print(topLeft, topRight, bottomLeft, bottomRight, Left, Right)
    for color in range(1,4):
        if isSafe(board, color, x,y,size-x-y+2):
            col = color
            break
    z=size-x-y+2
    str1 = "(" + str(int(col)) + "," + str(int(x)) + "," + str(int(y)) + "," + str(int(z)) + ")"
    #=====Print the next move
    sys.stdout.write(str1)


else:                                      #if this is not the first play, parse the last play and decide next move
    lastPlay = [int(a) for a in list(re.sub(',', '', new_words[-1].split("(")[-1].strip(")")))] #parse last play
    color, x, y, z = nextMove(board, lastPlay, depth)
    str1 = "(" + str(int(color)) + "," + str(int(x)) + "," + str(int(y)) + "," + str(int(z)) + ")"
    #=====Print the next move
    sys.stdout.write(str1)



