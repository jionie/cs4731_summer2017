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
from moba import *

class MyMinion(Minion):
	
	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
		self.states = [Idle]
		### Add your states to self.states (but don't remove Idle)
		### YOUR CODE GOES BELOW HERE ###
		self.states.append(Move)
		self.states.append(Attack)
		self.states.append(MovingAttack)
		### YOUR CODE GOES ABOVE HERE ###

	def start(self):
		Minion.start(self)
		self.changeState(Idle)

############################
### Idle
###
### This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):
	
	def enter(self, oldstate):
		State.enter(self, oldstate)
		# stop moving
		self.agent.stopMoving()
	
	def execute(self, delta = 0):
		State.execute(self, delta)
		### YOUR CODE GOES BELOW HERE ###
		self.agent.changeState(Move)
		### YOUR CODE GOES ABOVE HERE ###
		return None

##############################
### Taunt
###
### This is a state given as an example of how to pass arbitrary parameters into a State.
### To taunt someome, Agent.changeState(Taunt, enemyagent)

class Taunt(State):

	def parseArgs(self, args):
		self.victim = args[0]

	def execute(self, delta = 0):
		if self.victim is not None:
			print "Hey " + str(self.victim) + ", I don't like you!"
		self.agent.changeState(Idle)

##############################
### YOUR STATES GO HERE:

def closestTarget(agent, targets):
	agentLocation = agent.getLocation()
	returnTarget = None
	targetDist = INFINITY
	for target in targets:
		if distance(agentLocation, target.getLocation()) < targetDist:
			returnTarget = target
			targetDist = distance(agentLocation, target.getLocation())
	return returnTarget

def shootTarget(agent, target):
	agent.turnToFace(target.getLocation())
	agent.shoot()

class Move(State):

	def enter(self, oldstate):
		State.enter(self, oldstate)
		towers = self.agent.world.getEnemyTowers(self.agent.getTeam())
		bases = self.agent.world.getEnemyBases(self.agent.getTeam())
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		if len(towers) > 0:
			self.agent.navigateTo(closestTarget(self.agent, towers).getLocation())
		elif len(bases) > 0:
			self.agent.navigateTo(closestTarget(self.agent, bases).getLocation())
		elif len(enemies) > 0:
			self.agent.navigateTo(closestTarget(self.agent, enemies).getLocation())

	def execute(self, delta = 0):
		towers = self.agent.world.getEnemyTowers(self.agent.getTeam())
		bases = self.agent.world.getEnemyBases(self.agent.getTeam())
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		if not self.agent.isMoving():
			self.agent.changeState(Move)
		if len(towers) > 0:
			destinationTower = closestTarget(self.agent, towers)
			#self.agent.navigateTo(destinationTower.getLocation())
		elif len(bases) > 0:
			destinationBase = closestTarget(self.agent, bases)
			#self.agent.navigateTo(destinationBase.getLocation())
		elif len(enemies) > 0:
			destinationEnemy = closestTarget(self.agent, enemies)
			#self.agent.navigateTo(destinationEnemy.getLocation())
		if len(towers) > 0 and distance(self.agent.getLocation(),
			destinationTower.getLocation()) < 150 and rayTraceWorld(
			self.agent.getLocation(), destinationTower.getLocation(),
			self.agent.world.getLinesWithoutBorders()) is None:
			self.agent.changeState(Attack, destinationTower)
		if len(bases) > 0 and len(towers) == 0 and distance(self.agent.getLocation(),
			destinationBase.getLocation()) < 150 and rayTraceWorld(
			self.agent.getLocation(), destinationBase.getLocation(),
			self.agent.world.getLinesWithoutBorders()) is None:
			self.agent.changeState(Attack, destinationBase)
		if len(enemies) > 0 and len(bases) == 0 and len(towers) == 0 and distance(self.agent.getLocation(),
			destinationEnemy.getLocation()) < 150 and rayTraceWorld(
			self.agent.getLocation(), destinationEnemy.getLocation(),
			self.agent.world.getLinesWithoutBorders()) is None:
				if destinationEnemy.isMoving():
					self.agent.changeState(MovingAttack, destinationEnemy)
				else:
					self.agent.changeState(Attack, destinationEnemy)

class Attack(State):

	def parseArgs(self, args):
		self.target = args[0]

	def enter(self, oldstate):
		State.enter(self, oldstate)
		if isinstance(self.target, MOBAAgent):
			if self.target.isMoving():
				self.agent.changeState(MovingAttack, self.target)
		self.agent.stopMoving()
		towers = self.agent.world.getEnemyTowers(self.agent.getTeam())
		bases = self.agent.world.getEnemyBases(self.agent.getTeam())
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		allPossiblePoints = self.agent.getPossibleDestinations()
		self.targetPoints = []
		for point in allPossiblePoints:
			if distance(point, self.target.getLocation()) < 150 and distance(point, self.target.getLocation()) > 50:
				self.targetPoints.append(point)
		if self.target in set(towers) or self.target in set(bases) or self.target in set(enemies):
			shootTarget(self.agent, self.target)
		else: self.agent.changeState(Move)

	def execute(self, delta = 0):
		if isinstance(self.target, MOBAAgent):
			if self.target.isMoving():
				self.agent.changeState(MovingAttack, self.target)
		towers = self.agent.world.getEnemyTowers(self.agent.getTeam())
		bases = self.agent.world.getEnemyBases(self.agent.getTeam())
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		if not self.agent.isMoving():
			self.agent.navigateTo(random.choice(self.targetPoints))
		if self.target in set(towers) or self.target in set(bases) or self.target in set(enemies):
			shootTarget(self.agent, self.target)
		else:
			self.agent.changeState(Move)

class MovingAttack(State):

	def parseArgs(self, args):
		self.target = args[0]

	def enter(self, oldstate):
		State.enter(self, oldstate)
		if not self.target.isMoving():
			self.agent.changeState(Attack, self.target)
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		if self.target in set(enemies):
			self.agent.navigateTo(self.target.getLocation())
			shootTarget(self.agent, self.target)
		else: self.agent.changeState(Move)

	def execute(self, delta = 0):
		if not self.target.isMoving():
			self.agent.changeState(Attack, self.target)
		enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
		if self.target in set(enemies):
			self.agent.navigateTo(self.target.getLocation())
			shootTarget(self.agent, self.target)
		else: self.agent.changeState(Move)