import numpy as np
from train import getAdjacencyMat, findPath
from dataparser import matrixgeneration,dayoftheweek


#specify from date (num), to date (num), fromlocation, tolocation, output route
def routeoptimizer(fromdate, todate, fromlocation, tolocation,numtrains):
	arrival = []
	destination = []
	route = []
	noOfDestinations = 4
	noOfDays = np.abs(todate - fromdate)
	adjMatWeek = np.zeros((noOfDays,noOfDestinations,noOfDestinations))
	for i in range(noOfDays):
		arrivaltemp, destinationtemp = matrixgeneration(dayoftheweek(fromdate+i))
		print(arrivaltemp)
		print(destinationtemp)
		arrival.append(arrivaltemp)
		destination.append(destinationtemp)
		adjMatWeek[i,:, :] = getAdjacencyMat(arrival[i],destination[i], noOfDestinations)
	#print(adjMatWeek)
	#for non trivial solutions
	# for k in range(4):
	# 	adjMatWeek[:,k,k] = 0
	# print(adjMatWeek)
	adjMatWeek[:,]
	#find first path
	for j in range(numtrains):
		routetemp = findPath(adjMatWeek,[fromlocation], noOfDays + 1, tolocation)[0] #actual number of days is route length -1
	    #remove path
		for e,i in enumerate(routetemp[:-1]):
			adjMatWeek[e,routetemp[e], routetemp[e+1]] =  adjMatWeek[e,routetemp[e], routetemp[e+1]] - 1
		print(adjMatWeek)
		route.append(routetemp)

	return route
# arrival = []
# destination = []
# arrivaltemp, destinationtemp = matrixgeneration(dayoftheweek(0))
# arrival.append(arrivaltemp)
# destination.append(destinationtemp)
# print(arrival[0])

route = routeoptimizer(3,6,1,0,4)
print(route)