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

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import * 

from constants import *
from utils import *
from core import *

### This function optimizes the given path and returns a new path
### source: the current position of the agent
### dest: the desired destination of the agent
### path: the path previously computed by the A* algorithm
### world: pointer to the world
def shortcutPath(source, dest, path, world, agent):
	### YOUR CODE GOES BELOW HERE ###
	wholePath = [source]
	wholePath.extend(path)
	wholePath.append(dest)
	for point in wholePath:
		current = point
		i = wholePath.index(current)
		iStart = wholePath.index(current)
		while i < len(wholePath) :
			if clearShot(current, wholePath[i], world.getLinesWithoutBorders(), world.getPoints(), agent):
				i += 1
			else:
				break
		i -= 1
		if i - iStart > 1:
			while i > iStart + 1:
				wholePath.remove(wholePath[i-1])
				i -=1
	wholePath.remove(wholePath[0])
	wholePath.remove(wholePath[len(wholePath) - 1])
	path = wholePath
	### YOUR CODE GOES BELOW HERE ###
	return path

def clearShot(p1, p2, worldLines, worldPoints, agent):
	### YOUR CODE GOES BELOW HERE ###
	point1 = tuple(p1)
	point2 = tuple(p2)
	obstacleLines = worldLines
	r = agent.getRadius()
	if point1 == point2:
		return True
	if rayTraceWorldNoEndPoints(point1,point2,worldLines) is not None:
		return False
	if not point2[0] - point1[0] == 0 and not point2[1] - point1[1] == 0:
		# print (point1, point2)
		if (point2[0] > point1[0] and point2[1] < point1[1]):
			#print "yes"
			phi = abs(math.atan((float(point2[1]) - float(point1[1])) / (float(point2[0]) - float(point1[0]))))
			theta = (math.pi / 2) - phi
			point3 = (point1[0] + math.ceil(r * math.cos(theta)), point1[1] + math.ceil(r * math.sin(theta)))
			point4 = (point1[0] - math.ceil(r * math.cos(theta)), point1[1] - math.ceil(r * math.sin(theta)))
			point5 = (point2[0] + math.ceil(r * math.cos(theta)), point2[1] + math.ceil(r * math.sin(theta)))
			point6 = (point2[0] - math.ceil(r * math.cos(theta)), point2[1] - math.ceil(r * math.sin(theta)))
			line1 = (point3, point5)
			line2 = (point4, point6)
			#drawPolygon(line1, agent.world.debug, (255,0,0), 1, False)
			#drawPolygon(line2, agent.world.debug, (255, 0, 0), 1, False)
			if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1],
																							 obstacleLines) is not None:
				return False
		elif (point2[0] > point1[0] and point2[1] > point1[1]):
			phi = abs(math.atan((float(point2[1]) - float(point1[1])) / (float(point2[0]) - float(point1[0]))))
			theta = (math.pi / 2) - phi
			point3 = (point1[0] + math.ceil(r * math.cos(theta)), point1[1] - math.ceil(r * math.sin(theta)))
			point4 = (point1[0] - math.ceil(r * math.cos(theta)), point1[1] + math.ceil(r * math.sin(theta)))
			point5 = (point2[0] + math.ceil(r * math.cos(theta)), point2[1] - math.ceil(r * math.sin(theta)))
			point6 = (point2[0] - math.ceil(r * math.cos(theta)), point2[1] + math.ceil(r * math.sin(theta)))
			line1 = (point3, point5)
			line2 = (point4, point6)
			#drawPolygon(line1, agent.world.debug, (255, 0, 0), 1, False)
			#drawPolygon(line2, agent.world.debug, (255, 0, 0), 1, False)
			if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1],
																							 obstacleLines) is not None:
				return False
		elif (point2[0] < point1[0] and point2[1] > point1[1]):
			phi = abs(math.atan((float(point2[0]) - float(point1[0])) / (float(point2[1]) - float(point1[1]))))
			theta = (math.pi / 2) - phi
			point3 = (point1[0] + math.ceil(r * math.sin(theta)), point1[1] + math.ceil(r * math.cos(theta)))
			point4 = (point1[0] - math.ceil(r * math.sin(theta)), point1[1] - math.ceil(r * math.cos(theta)))
			point5 = (point2[0] + math.ceil(r * math.sin(theta)), point2[1] + math.ceil(r * math.cos(theta)))
			point6 = (point2[0] - math.ceil(r * math.sin(theta)), point2[1] - math.ceil(r * math.cos(theta)))
			line1 = (point3, point5)
			line2 = (point4, point6)
			#drawPolygon(line1, agent.world.debug, (255, 0, 0), 1, False)
			#drawPolygon(line2, agent.world.debug, (255, 0, 0), 1, False)

			if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1],
																							 obstacleLines) is not None:
				return False
		elif (point2[0] < point1[0] and point2[1] < point1[1]):
			phi = abs(math.atan((float(point2[0]) - float(point1[0])) / (float(point2[1]) - float(point1[1]))))
			theta = (math.pi / 2) - phi
			point3 = (point1[0] + math.ceil(r * math.sin(theta)), point1[1] - math.ceil(r * math.cos(theta)))
			point4 = (point1[0] - math.ceil(r * math.sin(theta)), point1[1] + math.ceil(r * math.cos(theta)))
			point5 = (point2[0] + math.ceil(r * math.sin(theta)), point2[1] - math.ceil(r * math.cos(theta)))
			point6 = (point2[0] - math.ceil(r * math.sin(theta)), point2[1] + math.ceil(r * math.cos(theta)))
			line1 = (point3, point5)
			line2 = (point4, point6)
			#drawPolygon(line1, agent.world.debug, (255, 0, 0), 1, False)
			#drawPolygon(line2, agent.world.debug, (255, 0, 0), 1, False)
			if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1],
																							 obstacleLines) is not None:
				return False
	if (point2[0] - point1[0] == 0):
		line1 = ((point1[0] - r, point1[1]), (point2[0] - r, point2[1]))
		line2 = ((point1[0] + r, point1[1]), (point2[0] + r, point2[1]))
		#drawPolygon(line1, agent.world.debug, (255, 0, 0), 1, False)
		#drawPolygon(line2, agent.world.debug, (255, 0, 0), 1, False)
		if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1],
																						 obstacleLines) is not None:
			return False
	if (point2[1] - point1[1] == 0):
		line1 = ((point1[0], point1[1] - r), (point2[0], point2[1] - r))
		line2 = ((point1[0], point1[1] + r), (point2[0], point2[1] + r))
		#drawPolygon(line1, agent.world.debug, (255, 0, 0), 1, False)
		#drawPolygon(line2, agent.world.debug, (255, 0, 0), 1, False)
		if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1],
																						 obstacleLines) is not None:
			return False
	### YOUR CODE GOES ABOVE HERE ###
	return True

### This function changes the move target of the agent if there is an opportunity to walk a shorter path.
### This function should call nav.agent.moveToTarget() if an opportunity exists and may also need to modify nav.path.
### nav: the navigator object
### This function returns True if the moveTarget and/or path is modified and False otherwise
def mySmooth(nav):
	### YOUR CODE GOES BELOW HERE ###
	if nav.destination is not None:
		if clearShot(nav.agent.position, nav.destination, nav.world.getLinesWithoutBorders(), nav.world.getPoints(), nav.agent):
			nav.agent.moveToTarget(nav.destination)
			return True
		else:
			if nav.path is not None:
				index = len(nav.path) - 1
				while index >= 0:
					if clearShot(nav.agent.position, nav.path[index], nav.world.getLinesWithoutBorders(), nav.world.getPoints(), nav.agent):
						nav.agent.moveToTarget(nav.path[index])
						return True
					index -= 1
	if isinstance(nav.agent, Gatherer):
		if not nav.agent.targets == []:
			sortedTargets = sortTargets(nav.agent.position, nav.agent.targets)
			if not nav.destination == sortedTargets[0]:
				nav.agent.targets = sortedTargets
				nav.computePath(nav.agent.position, nav.agent.targets[0])
				return True
	### YOUR CODE GOES ABOVE HERE ###
	return False

def sortTargets(location, targets):
	# Get the closest
	start = None
	dist = INFINITY
	for t in targets:
		d = distance(location, t)
		if d < dist:
			start = t
			dist = d
	# ASSERT: start has the closest node
	remaining = [] + targets
	sorted = [start]
	remaining.remove(start)
	current = start
	while len(remaining) > 0:
		closest = None
		dist = INFINITY
		for t in remaining:
			d = distance(current, t)
			if d < dist:
				closest = t
				dist = d
		sorted.append(closest)
		remaining.remove(closest)
		current = closest
	return sorted


