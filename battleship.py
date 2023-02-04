import random
import time

#custom map
hitMarker = " X "
missMarker = " 0 "
oceanMarker = " ~ "
boatMarker = " S "


numRows = int(input("Number of rows for the grid? "))
numColumns = int(input("Number of columns for the grid? "))
numBoats = int(input("Number of boats for the grid? "))
minBoatSize = int(input("What should the smallest boat size be? "))
maxBoatSize = int(input("What should the largest boat size be? "))

#making the grid
grid = []

#database
storedTargets = []

#temp row
tempRow = []
# loops number of column amount of time to append individual characters into the list
for i in range(numColumns):
    tempRow.append(oceanMarker)
# loops number of row amount of time to append complete rows to the grid
for i in range(numRows):
    grid.append(tempRow.copy())

    


#formats the grid into something readable in terminal
def displayGrid(battleshipField):
    print("\n"*10)
    gridString = ""
    lenList = len(storedTargets)
    print("Total Tries: " + str((lenList)))
    print("    ", end="")
    for i in range(1,numColumns+1):
        if i < 10:
            print(str(i), end = "  ")
        else:
            print(str(i), end = " ")
    print("")
    counter = 1
    for row in battleshipField:
        if counter < 10:
            gridString += str(counter)+ "  " + ''.join(row)+ '\n'
            counter += 1
        else:
            gridString += str(counter)+ " " + ''.join(row)+ '\n'
            counter += 1
    print(gridString)
displayGrid(grid)

#checks if a boat point overlaps another boat point
def isOverlap(test):
    # checks if the test point is outside the grid
    if test[0] >numRows or test[0] < 1 or test[1] >numColumns or test[1] < 1:
        return True
    #loops through the boat list
    for boat in boatList:
        for point in boat:
            if test == point:
                return True
    return False

# checks if there is enough space between boats when generating and the edge of the map
# length is the length of the whole boat
def sequenceOverlap(row, col, dir, length):
    # checks if going south is possible depending on the length of the generated boat
    if dir == 0: # North
        for i in range(length):
            if isOverlap([row-i,col]):
                # returns true if there is an overlap with another point
                return True
    if dir == 1: # East
        for i in range(length):
            if isOverlap([row,col+i]):
                # returns true if there is an overlap with another point
                return True
    if dir == 2: # South
        for i in range(length):
            if isOverlap([row+i,col]):
                # returns true if there is an overlap with another point
                return True
    if dir == 3: # West
        for i in range(length):
            if isOverlap([row,col-i]):
                # returns true if there is an overlap with another point
                return True


# DONE: Multi-cell boats.
# generate a 2 cell boat on the grid and make it so you can sink the boat
# Boat coordinate starts at 1
boatList= []
def genBoats(length):
    boat1 = []
    # Generates a new point if the previously generated point is in the boat list
    newPoint = [random.randint(1,numRows),random.randint(1,numColumns)]
    while True:
        if isOverlap(newPoint):
            newPoint = [random.randint(1,numRows),random.randint(1,numColumns)]
        else:
            boat1.append(newPoint)
            break
    rowPosition = boat1[0][0]
    columnPosition = boat1[0][1]
    # North: 0 East: 1 South: 2 West: 3
    # Randomly generate a direction number
    # Check if the 2nd point is a valid direction
    # Valid: make new point in valid direction
    # Invalid: Loop back up and randomly generate number again
    counter = 0
    while True:
        counter+=1
        if counter >100:
            print("Grid Too Small!")
            exit()
        directionNum = random.randint(0,3)
        if directionNum == 0: #north
            if sequenceOverlap(rowPosition-1 ,columnPosition,0, length):
                continue
            else:
                for i in range(1,length):
                    boat1.append([rowPosition-i, columnPosition])
                break
        elif directionNum == 1: #east
            if sequenceOverlap(rowPosition ,columnPosition+1 ,1, length):
                continue
            else:
                for i in range(1,length):
                    boat1.append([rowPosition, columnPosition+i])
                break
        elif directionNum == 2: #south
            if sequenceOverlap(rowPosition+1 ,columnPosition,2, length):
                continue
            else:
                for i in range(1,length):
                    boat1.append([rowPosition+i, columnPosition])
                break
        elif directionNum == 3: #west
            if sequenceOverlap(rowPosition, columnPosition-1, 3, length):
                continue
            else:
                for i in range(1,length):
                    boat1.append([rowPosition, columnPosition-i])
                break
    return boat1

# Generating Boats
for i in range(numBoats):
    boatList.append(genBoats(random.randint(minBoatSize,maxBoatSize)))





#TODO: attacklocation fix loop marking hits as misses for other boats.
def attackLocation(target):
    #loops through the boat list
    for boat in boatList:
        for point in boat:
            # if the boat placement equals the users input
            if point == target:
                # grid[r-1][c-1]
                boat.remove(target)
                grid[target[0]-1][target[1]-1] = hitMarker
                displayGrid(grid)
                print("Hit!")
                #if the boat list is empty (the boat is sunk)
                if len(boat) == 0:
                    print("Boat Sunk!")
                    boatList.remove(boat)
                    #exit()
                    if len(boatList) == 0:
                        print("You won!")
                        exit()
                return(0)
            #if the input is incorrect (miss)
    grid[target[0]-1][target[1]-1] = missMarker
    displayGrid(grid)
    print("Miss!")


def cheat():
    cheatGrid = []
    #temp row
    tempRow = []
    # loops number of column amount of time to append individual characters into the list
    for i in range(numColumns):
        tempRow.append(oceanMarker)
    # loops number of row amount of time to append complete rows to the grid
    for i in range(numRows):
        cheatGrid.append(tempRow.copy())
    
    for boat in boatList:
        for point in boat:
            cheatGrid[point[0]-1][point[1]-1] = boatMarker
    displayGrid(cheatGrid)

def getTarget():
    # attack loop (indentify target square)
    while True:
        targetRow = (input("Row Coordinate: "))
        if targetRow == "cheat":
            cheat()
            continue
        targetCol = (input("Column Coordinate: "))
        try:
            targetRow = int(targetRow)
            targetCol = int(targetCol)
        except:
            displayGrid(grid)
            print("Invalid Input Type")
            continue
    # checks  if the input value is in the correct range
        maxNum = len(grid)
        if targetRow <= maxNum and targetCol <= maxNum and targetRow>0 and targetCol>0:
            target = [targetRow,targetCol]
            # checks if the target was previously guessed
            if target not in storedTargets:
                storedTargets.append(target)
                return target
            else:
                displayGrid(grid)
                print("Coordinate Previously Guessed")

        else:
            displayGrid(grid)
            print("Coordinate outside the grid")



#The Game
while True:
    currentTarget = getTarget()
    attackLocation(currentTarget)


#hit/miss markers 


# Done: validate user input(entering the right type of input),(if it is a number it has to be in the grid).
# Done: Make sure user doesn't reinput an existing hit/miss value.
# DONE: finish automated generation  
# DONE: Possible bigger grid 10x10.
# DONE: Fix Index Out of Range bug
# DONE: Multi-cell boats.
# DONE: Randomize boat sizes, and boat amounts.
# DONE: Fix Full column being marked as hit (not the function display grid)
# DONE: Try to make boat add on position more fair (avoid defaulting to the right)
# DONE: Next Week: More multi cell boats (Helper function)
# DONE: Issue: After one 2 cell boat is sunk, the game quits.
# DONE: Fix overlapping issue (rewring genbBoat function using the overlap function to check and regenerate points)
# DONE: If the loop takes 30 or more tries to find a possible generation for the boat, just quit and delete first point, think of ideas
# DONE: Update gen boat function with our new sequentialOverlap function.