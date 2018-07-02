import numpy as np



def getAdjacencyMat(arrival, destination, noOfDestinations):
    adjMat = np.zeros((noOfDestinations, noOfDestinations))
    for i in range(0,len(arrival)):
        adjMat[arrival[i],destination[i]] = adjMat[arrival[i],destination[i]] + 1
    return adjMat                

def findPath(adjMatWeek, route, length, end):   #first value of route should be starting vertex and route should be cast as list e.g. [0]
    currentPath = adjMatWeek[len(route)-1,:,:]
    for e,i in enumerate(currentPath[route[-1],:]):
        if i != 0:
            route.append(e)
            if route[-1] == end and len(route) == length:
            	return route,1

            elif len(route) == length:
                    route.pop()
                    continue
                   
            else:
                    route,solved = findPath(adjMatWeek, route, length, end)
                    if solved ==1:
                        return route,1
    route.pop()
    return route,0 


if __name__ == "__main__":
    arrival = [0,0,2,2,1,1,0]
    destination = [2,1,3,1,2,3,1]
    noOfDestinations = max(max([arrival,destination])) + 1
    noOfDays = 7
    adjMatWeek = np.zeros((noOfDays,noOfDestinations,noOfDestinations))
    for i in range(0,noOfDays):
        adjMatWeek[i,:, :] =getAdjacencyMat(arrival,destination, noOfDestinations)

    print(adjMatWeek)
    route = findPath(adjMatWeek,[0],3,3 )[0] #actual number of days is route length -1
    print(route)
    
    #remove path
    for e,i in enumerate(route[:-1]):
        adjMatWeek[e,route[e], route[e+1]] =  adjMatWeek[e,route[e], route[e+1]] - 1
    print(adjMatWeek)
    #noq run again
