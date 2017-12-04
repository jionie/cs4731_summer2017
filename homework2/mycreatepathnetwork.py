'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates a path node network that connects the midpoints of each nav mesh together
def myCreatePathNetwork(world, agent = None):
	nodes = []
	edges = []
	polys = []
	### YOUR CODE GOES BELOW HERE ###
	allPoints = world.getPoints()
	random.shuffle(allPoints)
	corners = allPoints[0:4]
	maxBound = max(corners)
	obstacles = world.getObstacles()
	obstacleLines = []
	for obstacle in obstacles:
		obstacleLines.extend(obstacle.getLines())
	allLines = world.getLinesWithoutBorders()
	for a in allPoints:
		for b in allPoints:
			for c in allPoints:
				if not a==b and not a==c and not b==c:
					currentPoly = [a,b,c]
					inPolys = False
					for shape in polys:
						if set(currentPoly) == set(shape):
							inPolys = True
					if not inPolys and isConvex(currentPoly):
						obstacleInside = False
						if any([rayTraceWorldNoEndPoints(a, b, allLines) is not None and (a,b) not in allLines and (b,a) not in allLines,
						 		rayTraceWorldNoEndPoints(c, b, allLines) is not None and (c,b) not in allLines and (b,c) not in allLines,
						 		rayTraceWorldNoEndPoints(a, c, allLines) is not None and (a,c) not in allLines and (c,a) not in allLines]):
							obstacleInside = True
						distanceAB = (b[0]-a[0],b[1]-a[1])
						distanceBC = (c[0]-b[0],c[1]-b[1])
						distanceCA = (a[0]-c[0],a[1]-c[1])
						for obstacle in obstacles:
							x = [p[0] for p in currentPoly]
							y = [p[1] for p in currentPoly]
							centroid = (sum(x) / len(currentPoly), sum(y) / len(currentPoly))

							if obstacle.pointInside(centroid):
								obstacleInside = True
							elif any([obstacle.pointInside((a[0] + (distanceAB[0] / 8), a[1] + (distanceAB[1] / 8))) and a not in obstacle.getPoints(),
									obstacle.pointInside((a[0] + (2*distanceAB[0] / 8), a[1] + (2*distanceAB[1] / 8))) and a not in obstacle.getPoints(),
									obstacle.pointInside((a[0] + (3*distanceAB[0] / 8), a[1] + (3*distanceAB[1] / 8))) and a not in obstacle.getPoints(),
									obstacle.pointInside((a[0] + (4*distanceAB[0] / 8), a[1] + (4*distanceAB[1] / 8))) and a not in obstacle.getPoints(),
									obstacle.pointInside((a[0] + (5*distanceAB[0] / 8), a[1] + (5*distanceAB[1] / 8))) and a not in obstacle.getPoints(),
									obstacle.pointInside((a[0] + (6*distanceAB[0] / 8), a[1] + (6*distanceAB[1] / 8))) and a not in obstacle.getPoints(),
									obstacle.pointInside((a[0] + (7*distanceAB[0] / 8), a[1] + (7*distanceAB[1] / 8))) and a not in obstacle.getPoints()]):
								obstacleInside = True
							elif any([obstacle.pointInside((b[0] + (distanceBC[0] / 8), b[1] + (distanceBC[1] / 8))),
									obstacle.pointInside((b[0] + (2*distanceBC[0] / 8), b[1] + (2*distanceBC[1] / 8))) and b not in obstacle.getPoints(),
									obstacle.pointInside((b[0] + (3*distanceBC[0] / 8), b[1] + (3*distanceBC[1] / 8))) and b not in obstacle.getPoints(),
									obstacle.pointInside((b[0] + (4*distanceBC[0] / 8), b[1] + (4*distanceBC[1] / 8))) and b not in obstacle.getPoints(),
									obstacle.pointInside((b[0] + (5*distanceBC[0] / 8), b[1] + (5*distanceBC[1] / 8))) and b not in obstacle.getPoints(),
									obstacle.pointInside((b[0] + (6*distanceBC[0] / 8), b[1] + (6*distanceBC[1] / 8))) and b not in obstacle.getPoints(),
									obstacle.pointInside((b[0] + (7*distanceBC[0] / 8), b[1] + (7*distanceBC[1] / 8))) and b not in obstacle.getPoints()]):
								obstacleInside = True
							elif any([obstacle.pointInside((c[0] + (distanceCA[0] / 8), c[1] + (distanceCA[1] / 8))) and c not in obstacle.getPoints(),
									obstacle.pointInside((c[0] + (2*distanceCA[0] / 8), c[1] + (2*distanceCA[1] / 8))) and c not in obstacle.getPoints(),
									obstacle.pointInside((c[0] + (3*distanceCA[0] / 8), c[1] + (3*distanceCA[1] / 8))) and c not in obstacle.getPoints(),
									obstacle.pointInside((c[0] + (4*distanceCA[0] / 8), c[1] + (4*distanceCA[1] / 8))) and c not in obstacle.getPoints(),
									obstacle.pointInside((c[0] + (5*distanceCA[0] / 8), c[1] + (5*distanceCA[1] / 8))) and c not in obstacle.getPoints(),
									obstacle.pointInside((c[0] + (6*distanceCA[0] / 8), c[1] + (6*distanceCA[1] / 8))) and c not in obstacle.getPoints(),
									obstacle.pointInside((c[0] + (7*distanceCA[0] / 8), c[1] + (7*distanceCA[1] / 8))) and c not in obstacle.getPoints()]):
								obstacleInside = True
							for point in obstacle.getPoints():
								if pointInsidePolygonPoints(point, currentPoly) and point not in currentPoly:
									obstacleInside = True
						if not obstacleInside:
							polys.append(currentPoly)
							allLines.append((a, b))
							allLines.append((b, c))
							allLines.append((c, a))

	polygonsMerged = False
	while not polygonsMerged:
		polygonsMerged = True
		for polygon1 in polys:
			for polygon2 in polys:
				if not polygon1 == polygon2:
					if polygonsAdjacent(polygon1, polygon2):
						newPolygon = []
						for point1 in polygon1:
							newPolygon.append(point1)
						for point2 in polygon2:
							if point2 not in newPolygon:
								newPolygon.append(point2)
						x = [point[0] for point in newPolygon]
						y = [point[1] for point in newPolygon]
						centroid = (sum(x) / len(newPolygon), sum(y) / len(newPolygon))
						newPolygon.sort(key = lambda point: math.atan2(point[1] - centroid[1], point[0] - centroid[0]))
						if isConvex(newPolygon):
							if polygon1 in polys:
								polys.remove(polygon1)
							if polygon2 in polys:
								polys.remove(polygon2)
							polys.append(newPolygon)
							polygonsMerged = False
				if not polygonsMerged: break

	polygonNodesAll = []
	polygonNodes = []
	for polygon in polys:
		if polygonNodes:
			polygonNodesAll.append(polygonNodes)
		polygonNodes = []
		for i in xrange(len(polygon)):
			edge1 = polygon[i]
			if i == len(polygon) - 1:
				edge2 = polygon[0]
			else:
				edge2 = polygon[i+1]
			xDist = edge2[0] - edge1[0]
			yDist = edge2[1] - edge1[1]
			midpoint = (int(edge1[0] + (xDist/2)),int(edge1[1] + (yDist/2)))
			collision = False
			for obstacle in obstacles:
				if obstacle.pointInside(midpoint):
					collision = True
				elif obstacle.pointInside((midpoint[0],midpoint[1] + 1)):
					collision = True
				elif obstacle.pointInside((midpoint[0],midpoint[1] - 1)):
					collision = True
				elif obstacle.pointInside((midpoint[0] + 1 ,midpoint[1])):
					collision = True
				elif obstacle.pointInside((midpoint[0] - 1,midpoint[1])):
					collision = True
				elif midpoint[0] == 0 or midpoint[1] == 0 or midpoint[0] == maxBound[0] or midpoint[1] == maxBound[1]:
					collision = True
			if not collision:
				polygonNodes.append(midpoint)
				if midpoint not in set(nodes):
					nodes.append(midpoint)
	if polygonNodes:
		polygonNodesAll.append(polygonNodes)

	for polygonNode in polygonNodesAll:
		for point1 in polygonNode:
			for point2 in polygonNode:
				if not point1 == point2:
					if (point1,point2) not in set(edges) and (point2,point1) not in set(edges) and rayTraceWorldNoEndPoints(point1,point2, edges) is None:
						collision = False
						r = agent.getRadius()
						if not point2[0] - point1[0] == 0 and not point2[1] - point1[1] == 0:
							#print (point1, point2)
							if (point2[0] > point1[0] and point2[1] < point1[1]):
								phi = abs(math.atan((float(point2[1])-float(point1[1]))/(float(point2[0])-float(point1[0]))))
								theta = (math.pi/2) - phi
								point3 = (point1[0] + math.ceil(r * math.cos(theta)), point1[1] + math.ceil(r * math.sin(theta)))
								point4 = (point1[0] - math.ceil(r * math.cos(theta)), point1[1] - math.ceil(r * math.sin(theta)))
								point5 = (point2[0] + math.ceil(r * math.cos(theta)), point2[1] + math.ceil(r * math.sin(theta)))
								point6 = (point2[0] - math.ceil(r * math.cos(theta)), point2[1] - math.ceil(r * math.sin(theta)))
								line1 = (point3, point5)
								line2 = (point4, point6)
								#drawPolygon(line1, world.debug,0,1,False)
								#drawPolygon(line2, world.debug,0,1,False)
								if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1], obstacleLines) is not None:
									collision = True
							elif (point2[0] > point1[0] and point2[1] > point1[1]):
								phi = abs(math.atan((float(point2[1]) - float(point1[1])) / (float(point2[0]) - float(point1[0]))))
								theta = (math.pi/2) - phi
								point3 = (point1[0] + math.ceil(r * math.cos(theta)), point1[1] - math.ceil(r * math.sin(theta)))
								point4 = (point1[0] - math.ceil(r * math.cos(theta)), point1[1] + math.ceil(r * math.sin(theta)))
								point5 = (point2[0] + math.ceil(r * math.cos(theta)), point2[1] -  math.ceil(r * math.sin(theta)))
								point6 = (point2[0] - math.ceil(r * math.cos(theta)), point2[1] + math.ceil(r * math.sin(theta)))
								line1 = (point3, point5)
								line2 = (point4, point6)
								#drawPolygon(line1, world.debug,0,1,False)
								#drawPolygon(line2, world.debug,0,1,False)
								if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1], obstacleLines) is not None:
									collision = True
							elif (point2[0] < point1[0] and point2[1] > point1[1]):
								phi = abs(math.atan((float(point2[0]) - float(point1[0])) / (float(point2[1]) - float(point1[1]))))
								theta = (math.pi/2) - phi
								point3 = (point1[0] + math.ceil(r * math.sin(theta)), point1[1] + math.ceil(r * math.cos(theta)))
								point4 = (point1[0] - math.ceil(r * math.sin(theta)), point1[1] - math.ceil(r * math.cos(theta)))
								point5 = (point2[0] + math.ceil(r * math.sin(theta)), point2[1] + math.ceil(r * math.cos(theta)))
								point6 = (point2[0] - math.ceil(r * math.sin(theta)), point2[1] - math.ceil(r * math.cos(theta)))
								line1 = (point3, point5)
								line2 = (point4, point6)
								#drawPolygon(line1, world.debug,0,1,False)
								#drawPolygon(line2, world.debug,0,1,False)
								if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1], obstacleLines) is not None:
									collision = True
							elif (point2[0] < point1[0] and point2[1] < point1[1]):
								phi = abs(math.atan((float(point2[0]) - float(point1[0])) / (float(point2[1]) - float(point1[1]))))
								theta = (math.pi/2) - phi
								point3 = (point1[0] + math.ceil(r * math.sin(theta)), point1[1] - math.ceil(r * math.cos(theta)))
								point4 = (point1[0] - math.ceil(r * math.sin(theta)), point1[1] + math.ceil(r * math.cos(theta)))
								point5 = (point2[0] + math.ceil(r * math.sin(theta)), point2[1] - math.ceil(r * math.cos(theta)))
								point6 = (point2[0] - math.ceil(r * math.sin(theta)), point2[1] + math.ceil(r * math.cos(theta)))
								line1 = (point3, point5)
								line2 = (point4, point6)
								#drawPolygon(line1, world.debug,0,1,False)
								#drawPolygon(line2, world.debug,0,1,False)
								if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1], obstacleLines) is not None:
									collision = True
						if (point2[0] - point1[0] == 0):
							line1 = ((point1[0] - r, point1[1]),(point2[0] - r, point2[1]))
							line2 = ((point1[0] + r, point1[1]),(point2[0] + r, point2[1]))
							#drawPolygon(line1, world.debug, 0, 1, False)
							#drawPolygon(line2, world.debug, 0, 1, False)
							if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0],line2[1], obstacleLines) is not None:
								collision = True
						if (point2[1] - point1[1] == 0):
							line1 = ((point1[0], point1[1] - r),(point2[0], point2[1] - r))
							line2 = ((point1[0], point1[1] + r),(point2[0], point2[1] + r))
							#drawPolygon(line1, world.debug, 0, 1, False)
							#drawPolygon(line2, world.debug, 0, 1, False)
							if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1],obstacleLines) is not None:
								collision = True
						if not collision:
							edges.append((point1,point2))
	# for node in nodes:
	# 	drawCross(world.debug, node, (0,0,255), 4, 4)
	# for polygon in polys:
	# 	x = [p[0] for p in polygon]
	# 	y = [p[1] for p in polygon]
	# 	centroid = (sum(x) / len(polygon), sum(y) / len(polygon))
	# 	drawCross(world.debug, centroid,255,5,5)

	### YOUR CODE GOES ABOVE HERE ###
	return nodes, edges, polys

	
