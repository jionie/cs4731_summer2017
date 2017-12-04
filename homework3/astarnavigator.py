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

import sys, pygame, math, numpy, random, time, copy, Queue
from pygame.locals import * 

from constants import *
from utils import *
from core import *
from mycreatepathnetwork import *
from mynavigatorhelpers import *


###############################
### AStarNavigator
###
### Creates a path node network and implements the A* algorithm to create a path to the given destination.

class AStarNavigator(NavMeshNavigator):

	def __init__(self):
		NavMeshNavigator.__init__(self)


	### Create the path node network.
	### self: the navigator object
	### world: the world object
	def createPathNetwork(self, world):
		self.pathnodes, self.pathnetwork, self.navmesh = myCreatePathNetwork(world, self.agent)
		return None

	### Finds the shortest path from the source to the destination using A*.
	### self: the navigator object
	### source: the place the agent is starting from (i.e., its current location)
	### dest: the place the agent is told to go to
	def computePath(self, source, dest):
		self.setPath(None)
		### Make sure the next and dist matrices exist
		if self.agent != None and self.world != None:
			self.source = source
			self.destination = dest
			### Step 1: If the agent has a clear path from the source to dest, then go straight there.
			###   Determine if there are no obstacles between source and destination (hint: cast rays against world.getLines(), check for clearance).
			###   Tell the agent to move to dest
			### Step 2: If there is an obstacle, create the path that will move around the obstacles.
			###   Find the path nodes closest to source and destination.
			###   Create the path by traversing the self.next matrix until the path node closest to the destination is reached
			###   Store the path by calling self.setPath()
			###   Tell the agent to move to the first node in the path (and pop the first node off the path)
			if clearShot(source, dest, self.world.getLines(), self.world.getPoints(), self.agent):
				self.agent.moveToTarget(dest)
			else:
				start = findClosestUnobstructed(source, self.pathnodes, self.world.getLinesWithoutBorders())
				end = findClosestUnobstructed(dest, self.pathnodes, self.world.getLinesWithoutBorders())
				if start != None and end != None:
					# print len(self.pathnetwork)
					newnetwork = unobstructedNetwork(self.pathnetwork, self.world.getGates())
					# print len(newnetwork)
					closedlist = []
					path, closedlist = astar(start, end, newnetwork)
					if path is not None and len(path) > 0:
						path = shortcutPath(source, dest, path, self.world, self.agent)
						self.setPath(path)
						if self.path is not None and len(self.path) > 0:
							first = self.path.pop(0)
							self.agent.moveToTarget(first)
		return None

	### Called when the agent gets to a node in the path.
	### self: the navigator object
	def checkpoint(self):
		myCheckpoint(self)
		return None

	### This function gets called by the agent to figure out if some shortcuts can be taken when traversing the path.
	### This function should update the path and return True if the path was updated.
	def smooth(self):
		return mySmooth(self)

	def update(self, delta):
		myUpdate(self, delta)


def unobstructedNetwork(network, worldLines):
	newnetwork = []
	for l in network:
		hit = rayTraceWorld(l[0], l[1], worldLines)
		if hit == None:
			newnetwork.append(l)
	return newnetwork




def astar(init, goal, network):
	path = []
	open = []
	closed = []
	### YOUR CODE GOES BELOW HERE ###
	open = Queue.PriorityQueue()
	openSet = set([])
	closed = set([])
	current = (distance(init,goal), init)
	open.put(current)
	openSet.add(current[1])
	parentDict = {}
	while not open.empty():
		current = open.get()
		openSet.remove(current[1])
		if current[1] == goal:
			break
		closed.add(current[1])
		neighbors = []
		for edge in network:
			if edge[0] == current[1]:
				neighbors.append(edge[1])
			elif edge[1] == current[1]:
				neighbors.append(edge[0])
		for neighbor in neighbors:
			if neighbor not in closed:
				gScore = current[0] + distance(current[1], neighbor)
				fScore = gScore + distance(neighbor,goal)
				if neighbor not in openSet:
					open.put((fScore, neighbor))
					openSet.add(neighbor)
					parentDict[neighbor] = current[1]
				else:
					for node in open.queue:
						if neighbor == node[1]:
							oldgScore = node[0]
					if gScore < oldgScore:
						for node in open.queue:
							if neighbor == node[1]:
								open.queue.remove(node)
								open.queue.append((fScore, node[1]))
								parentDict[neighbor] = current[1]
								break
	index = goal
	while index is not init:
		path.append(index)
		if index not in parentDict:
			path = None
			break
		else:
			index = parentDict[index]
	if path is not None:
		path.append(init)
		path.reverse()
	closed = list(closed)
	### YOUR CODE GOES ABOVE HERE ###
	return path, closed




def myUpdate(nav, delta):
	### YOUR CODE GOES BELOW HERE ###
	if nav.getDestination() is not None and not clearShot(nav.agent.getLocation(), nav.agent.getMoveTarget(), nav.world.getLinesWithoutBorders(), nav.world.getPoints(),
					 nav.agent):
		nav.agent.stopMoving()
		nav.agent.navigateTo(nav.getDestination())
		newPath = nav.getPath()
		if newPath is not None:
			nav.agent.start()
	### YOUR CODE GOES ABOVE HERE ###
	return None



def myCheckpoint(nav):
	### YOUR CODE GOES BELOW HERE ###
	wholePath = [nav.agent.getLocation(), nav.agent.getMoveTarget()]
	wholePath.extend(nav.getPath())
	wholePath.append(nav.getDestination())
	i = 0
	while i + 1 < len(wholePath):
		if not clearShot(wholePath[i], wholePath[i+1],nav.world.getLinesWithoutBorders(),nav.world.getPoints(),nav.agent):
			nav.agent.navigateTo(nav.getDestination())
			newPath = nav.getPath()
			if newPath is None:
				nav.agent.stopMoving()
		i = i + 1
	### YOUR CODE GOES ABOVE HERE ###
	return None


### Returns true if the agent can get from p1 to p2 directly without running into an obstacle.
### p1: the current location of the agent
### p2: the destination of the agent
### worldLines: all the lines in the world
### agent: the Agent object
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
			phi = abs(math.atan((float(point2[1]) - float(point1[1])) / (float(point2[0]) - float(point1[0]))))
			theta = (math.pi / 2) - phi
			point3 = (point1[0] + math.ceil(r * math.cos(theta)), point1[1] + math.ceil(r * math.sin(theta)))
			point4 = (point1[0] - math.ceil(r * math.cos(theta)), point1[1] - math.ceil(r * math.sin(theta)))
			point5 = (point2[0] + math.ceil(r * math.cos(theta)), point2[1] + math.ceil(r * math.sin(theta)))
			point6 = (point2[0] - math.ceil(r * math.cos(theta)), point2[1] - math.ceil(r * math.sin(theta)))
			line1 = (point3, point5)
			line2 = (point4, point6)
			#drawPolygon(line1, agent.world.debug,0,1,False)
			#drawPolygon(line2, agent.world.debug,0,1,False)
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
			#drawPolygon(line1, agent.world.debug,0,1,False)
			#drawPolygon(line2, agent.world.debug,0,1,False)
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
			#drawPolygon(line1, agent.world.debug,0,1,False)
			#drawPolygon(line2, agent.world.debug,0,1,False)
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
			#drawPolygon(line1, agent.world.debug,0,1,False)
			#drawPolygon(line2, agent.world.debug,0,1,False)
			if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1],
																							 obstacleLines) is not None:
				return False
	if (point2[0] - point1[0] == 0):
		line1 = ((point1[0] - r, point1[1]), (point2[0] - r, point2[1]))
		line2 = ((point1[0] + r, point1[1]), (point2[0] + r, point2[1]))
		#drawPolygon(line1, agent.world.debug, 0, 1, False)
		#drawPolygon(line2, agent.world.debug, 0, 1, False)
		if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1],
																						 obstacleLines) is not None:
			return False
	if (point2[1] - point1[1] == 0):
		line1 = ((point1[0], point1[1] - r), (point2[0], point2[1] - r))
		line2 = ((point1[0], point1[1] + r), (point2[0], point2[1] + r))
		#drawPolygon(line1, agent.world.debug, 0, 1, False)
		#drawPolygon(line2, agent.world.debug, 0, 1, False)
		if rayTraceWorld(line1[0], line1[1], obstacleLines) is not None or rayTraceWorld(line2[0], line2[1],
																						 obstacleLines) is not None:
			return False
	### YOUR CODE GOES ABOVE HERE ###
	return True

