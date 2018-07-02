import numpy as np
from train import getAdjacencyMat, findPath
from dataparser import matrixgeneration,dayoftheweek


#specify from date (num), to date (num), fromlocation, tolocation, output route
def graphoutput(fromdate, todate):
	arrival = []
	destination = []
	route = []
	noOfDestinations = 4
	noOfDays = np.abs(todate - fromdate)
	adjMatWeek = np.zeros((noOfDays,noOfDestinations,noOfDestinations))
	arrivaltemp, destinationtemp = matrixgeneration(dayoftheweek(fromdate))
	print(arrivaltemp)
	print(destinationtemp)
	arrival.append(arrivaltemp)
	destination.append(destinationtemp)
	adjMatWeek[0,:, :] = getAdjacencyMat(arrival[0],destination[0], noOfDestinations)
	return adjMatWeek

graph = graphoutput(6,0)
print(graph)