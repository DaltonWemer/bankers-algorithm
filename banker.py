# Dalton Wemer
# CSC 360 Operating Systems
# Bankers Algorithm Implementation
# March 10 2021
# Instructor: Dr. Siming Liu

# Get access to CLI parameters
import sys

# Grabs the first command line argument and sets it
# as a variable that we can access in our read function
filePath = sys.argv[1]

# Loops through the data file and splits each line 
# into a new element in array
with open(filePath, 'r') as file:
    data = file.read().splitlines()

# Initalize required variables 
alphabet = ['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M' 'N', "O"]
numOfProcess = int(data[0])
numOfResourceTypes = int(data[2])
allocationMatrix=[]
tempAllocationMatrix=[]
maxMatrix=[]
availableVector=[]
copyAvailableVector=[]
needMatrix = [ [0] * numOfResourceTypes for _ in range(numOfProcess)]         
processRequestingResource=2
listRequestVector=[]     
newAvailVector = [[0 for x in range(0)] for y in range(1)] 
availForPrinting = []

def main():
    for x in range(0, numOfProcess):
        # Get the string from the position in text file and
        # split each character up into it's own string
        allocTempRow = data[x+4]
        splitRow = allocTempRow.split()

        # Cast each string as an integer
        alloc_map_object = map(int, splitRow)
        alloc_list_of_integers = list(alloc_map_object)

        # Append the integer array to the matrix
        allocationMatrix.append(alloc_list_of_integers)
        

    # Appends each of the rows of the max matrix
    # to our max matrix array
    for x in range(0, numOfProcess):
        # Get the string from the position in text file and
        # split each character up into it's own string
        maxTempRow = data[5 + x + numOfProcess]
        maxTempRow.split()
        maxSplitRow = maxTempRow.split()

        # Cast each string as an integer
        max_map_object = map(int, maxSplitRow)
        max_list_of_integers = list(max_map_object)

        # Append the integer array to the matrix
        maxMatrix.append(max_list_of_integers)
    
    # Calculate the need matrix by using the formula
    # Need[i,j] = Max[i,j] - Allocation[i,j]
    for j in range(numOfResourceTypes):
        for i in range (numOfProcess):
            needMatrix[i][j] = maxMatrix[i][j] - allocationMatrix[i][j]
            

    # Read the available vector in and format it
    tempAvailableVector = data[(numOfProcess*2) + 6]
    splitTempAvailableVector = tempAvailableVector.split()
    mapAvailableVector = map(int, splitTempAvailableVector)
    listAvailableVector = list(mapAvailableVector)

    availableVector.append(listAvailableVector)

    # Used for final calculation, created a copy to avoid reference issues
    # when updating the available resources in the algorithm
    copyTempAvailableVector = data[(numOfProcess*2) + 6]
    copySplitTempAvailableVector = copyTempAvailableVector.split()
    copyMapAvailableVector = map(int, copySplitTempAvailableVector)
    copyListAvailableVector = list(copyMapAvailableVector)

    copyAvailableVector.append(copyListAvailableVector)

    # Get the request vector and split it into two parts
    # an int that represents the process that is requesting
    # the additional resource and the vector that represents
    # that actual vector that will be added to the process
    # we then map every element in the vector to an int
    tempRequestVector = data[(numOfProcess * 2 + 8)]
    splitTempRequestVector = tempRequestVector.split(':')
    processRequestingResource = splitTempRequestVector[0]
    
    spaceSplitTempRequest = splitTempRequestVector[1].split()
    mapRequstVector = map(int, spaceSplitTempRequest)
    listRequestVector = list(mapRequstVector)

    # Start displaying program in console 
    echoData(processRequestingResource, listRequestVector)
    print('\n')


# Used for each process in a system, evaluates a process
# and returns whether or not the need of a given process
# is highter than the available resoruces
def isProccessSafe(i, needMatrix, availableVector):
    for j in range(numOfResourceTypes):
        if(needMatrix[i][j]>availableVector[0][j]):
            return 0
    return 1
    

# Loops though every process until every process has been completed or cannot be,
# while keeping track of every process that gets completed. Once a process gets completed,
# we add the resources it was taking up to the available vector. Once concluded, If the amount of processes
# that got completed is equal to the amount of processes in our system we know the system is currently
# in a safe state
def isSystemSafe(needMatrix, allocationMatrix, availableVector):
    finish = [0] * numOfProcess    
    count = 0
    tempAvailableVector = availableVector
    tempAllocationMatrix = allocationMatrix    
    while(count < numOfProcess):
        temp = 0
        for i in range(numOfProcess):
            if(finish[i] == 0):
                if(isProccessSafe(i, needMatrix, tempAvailableVector)):
                    finish[i]=1
                    count+=1
                    temp=1
                    for j in range(numOfResourceTypes):
                        tempAvailableVector[0][j] += tempAllocationMatrix[i][j] 
        if(temp == 0):
            break
                
    if(count < numOfProcess):
        return False
    else:
        return True
        

# Adds request vector to the process requesting additonal resources 
# and then runs the algorithm again to check if the request can be granted
def request(process,vector):
    processRequesting = int(process)
    for i in range(numOfResourceTypes):
        allocationMatrix[processRequesting][i] += vector[i]
        newAvailVector[0].append(copyAvailableVector[0][i] - vector[i])
        availForPrinting.append(copyAvailableVector[0][i] - vector[i])

    if(isSystemSafe(newNeed(), allocationMatrix, newAvailVector)):
        return True
    else:
        return False


# Calculate new need after request
def newNeed():
    newNeedMatrix = [ [0] * numOfResourceTypes for _ in range(numOfProcess)]         

    for j in range(numOfResourceTypes):
        for i in range (numOfProcess):
            newNeedMatrix[i][j] = maxMatrix[i][j] - allocationMatrix[i][j]

    return newNeedMatrix


# Prints all of the data in the format specified
def echoData(processRequestingResource, listRequestVector):
    print("\n")
    print("There are " + str(numOfProcess) + " processes in the system" + "\n")
    print("There are " + str(numOfResourceTypes) + " resource types" "\n")

    # Print the Allocation Matrix
    print("The Allocation Matrix is...")
    i=0
    print("  ", end=" ")
    for x in range(numOfResourceTypes):
        print(alphabet[x], end =" ")

    print(" ")
    for row in allocationMatrix: 
        print(str(i) + ":", *row)
        i += 1
    
    print("\n")

    # Print the Max Matrix
    print("The Max Matrix is...")
    i=0
    print("  ", end=" ")
    for x in range(numOfResourceTypes):
        print(alphabet[x], end =" ")

    print(" ")
    for row in maxMatrix: 
        print(str(i) + ":", *row)
        i += 1

    print("\n")

    # Print the need matrix
    print("The Need Matrix is...")
    i=0
    print("  ", end=" ")
    for x in range(numOfResourceTypes):
        print(alphabet[x], end =" ")

    print(" ")
    for row in needMatrix: 
        print(str(i) + ":", *row)
        i += 1

    print("\n")

    # Print the Available Vector
    print("The Available Vector is...")
    
    for x in range(len(availableVector[0])):
        print(alphabet[x], end =" ")

    print(" ")    
    print(*availableVector[0])

    print("\n")
    # Print the safe state status
    if(isSystemSafe(needMatrix, allocationMatrix, availableVector)):
         print("THE SYSTEM IS IN A SAFE STATE!")
    else:
         print("THE SYSTEM IS NOT IN A SAFE STATE!")

    print("\n")
    # Print the request vector
    print("The Request Vector is...")

    print("  ", end=" ")
    for x in range(len(listRequestVector)):
        print(alphabet[x], end =" ")

    print(" ")
    print(processRequestingResource + ":", *listRequestVector)    

    print("\n")
    # Print the safe state status
    if(request(processRequestingResource, listRequestVector)):
         print("THE REQUEST CAN BE GRANTED!")
    else:
         print("THE REQUEST CAN NOT BE GRANTED!")

    print("\n")
    # Print the request vector
    print("The Available Vector is...")

    # Print the Available Vector
    for x in range(len(availableVector[0])):
        print(alphabet[x], end =" ")

    print(" ")    
    print(*availForPrinting)

if __name__ == "__main__":
    main()