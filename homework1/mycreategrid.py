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

# Creates a grid as a 2D array of True/False values (True = traversable). Also returns the dimensions of the grid as a (columns, rows) list.
def myCreateGrid(world, cellsize):
	grid = None
	dimensions = (0, 0)
	### YOUR CODE GOES BELOW HERE ###
	maxEdgePoints = max(world.getPoints()[0:3])
	columnPoints = maxEdgePoints[0]
	rowPoints = maxEdgePoints[1]
	gridColumns = int(columnPoints/cellsize)
	gridRows = int(rowPoints/cellsize)
	dimensions = (gridColumns,gridRows)
	grid = [[] for i in range(gridColumns)]
	for i in range(0, gridColumns):
		for j in range(0, gridRows):
			ulCorner = (int(i*cellsize),int(j*cellsize))
			urCorner = (int(i*cellsize + cellsize), int(j*cellsize))
			llCorner = (int(i*cellsize), int(j*cellsize + cellsize))
			lrCorner = (int(i*cellsize + cellsize), int(j*cellsize + cellsize))
			midpoint = (int(i*cellsize + (cellsize/2)), int(j*cellsize + (cellsize/2)))
			if any([rayTraceWorld(ulCorner, urCorner, world.getLinesWithoutBorders()) is not None,
					rayTraceWorld(urCorner, lrCorner, world.getLinesWithoutBorders()) is not None,
					rayTraceWorld(lrCorner, llCorner, world.getLinesWithoutBorders()) is not None,
					rayTraceWorld(llCorner, ulCorner, world.getLinesWithoutBorders()) is not None,
					rayTraceWorld(ulCorner, lrCorner, world.getLinesWithoutBorders()) is not None,
					rayTraceWorld(urCorner, llCorner, world.getLinesWithoutBorders()) is not None]):
				grid[i].append(False)
			elif any([pointInsidePolygonLines(ulCorner, world.getLinesWithoutBorders()),
						pointInsidePolygonLines(urCorner, world.getLinesWithoutBorders()),
						pointInsidePolygonLines(lrCorner, world.getLinesWithoutBorders()),
						pointInsidePolygonLines(llCorner, world.getLinesWithoutBorders()),
						pointInsidePolygonLines(midpoint, world.getLinesWithoutBorders())]):
				grid[i].append(False)
			else:
				grid[i].append(True)
	### YOUR CODE GOES ABOVE HERE ###
	return grid, dimensions

