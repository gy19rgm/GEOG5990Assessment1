# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:17:03 2019

@author: gy19rgm
"""
import random

class Agent ():

    def __init__(self, environment, agents, dogs): # this initialises agent + defines environ and other agents
        self.x = random.randint(0,299)
        self.y = random.randint(0,299)
        self.environment = environment
        self.agents = agents
        self.dogs = dogs
        self.store = 0  # initial store of agent's food
        
    def __str__(self): # how to return info about agent/self
        return str(self.y) + " " + str(self.x)  
        
    def check_field(self): # sheep check 
        
        closest_dog = []
        
        for i in range(len(self.dogs)):
            distance = self.distance_between(self.dogs[i])
            closest_dog.append([distance, self.dogs[i].x, self.dogs[i].y],)
        # sort on 0 value
        closest_dog.sort()
        
        return closest_dog[0]

    def move(self):     
        
        close = self.check_field()
    
        if close[0] < 20:
            
            if self.x == close[1]:
                pass
            if self.x - close[1] < 0:
                self.x = self.x - 2
            else:
                self.x = self.x + 2

            if self.y == close[2]:
                pass
            if self.y - close[2] < 0:
                self.y = self.y - 2
            else:
                self.y = self.y + 2                

        else:
            if random.random() < 0.5:
                self.y += 1
            else:
                self.y -= 1
                
            if random.random() < 0.5:
                self.x += 1
            else:
                self.x -= 1
            
        # Check if off edge and adjust.
        if self.y < 0:
#            print('bounce')
            self.y = 0
        if self.x < 0:
#            print('bounce')
            self.x = 0
        if self.y > 299:
#            print('bounce')
            self.y = 299
        if self.x > 299:
#            print('bounce')
            self.x = 299
                                
    def eat(self): # eat the 'grass' (environment)
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
            
    def distance_between(self, agent): # work out the distance between self and other agent
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5        
            
    def share_with_neighbours(self, neighbourhood):
        self.neighbourhood = neighbourhood
        # Loop through the agents in self.agents
        for agent in self.agents:
            # Calculate the distance between self and the current other agent
            distance = self.distance_between(agent)
            # If distance is less than or equal to the neighbourhood
            if distance <= neighbourhood:
                # Sum self.store and agent.store
                sum = self.store + agent.store
                # Divide sum by two to calculate average
                average = sum / 2
                self.store = average
                agent.store = average
  

class Dog(Agent):
    
    def __init__(self, environment, agents, dogs, y, x):
        super().__init__(environment, agents, dogs)
        
        self.y = y 
        self.x = x
        if (y == None):
            self.y = random.randint(0,299)
        else:
            self.y = y
        if (x == None):
            self.x = random.randint(0,299)
        else:
            self.x = x      

    def move(self):
        # check vicinity
        closest = self.check_vicinity()
        
        # if sheep in vicinity then herd
        if closest[0] < 30:     # where 30 is a dog's vision
            # Check Dog is able to identify closest sheep
            #print(str(closest))
            
            #print("Start sheepdog x", self.x)
            #print("start closest sheep", closest[0])
            self.x += (closest[1]-self.x)/2
            #print("End sheepdog x", self.x)
            #print("end closest sheep", closest[0])
            
            self.y += (closest[2]-self.y)/2
        
        # else random movement
        else:
            if random.random() < 0.5:
                self.y += 5
            else:
                self.y -= 5
                
            if random.random() < 0.5:
                self.x += 5
            else:
                self.x -= 5

        # Check if off edge and adjust - check bounce if reaches environ edge
        if self.y < 0:
#            print('bounce')
            self.y = 0
        if self.x < 0:
#            print('bounce')
            self.x = 0
        if self.y > 299:
#            print('bounce')
            self.y = 299
        if self.x > 299:
#            print('bounce')
            self.x = 299

    def check_vicinity(self):
        closest_sheep = []
        
        for i in range(len(self.agents)):
            distance = self.distance_between(self.agents[i])
            closest_sheep.append([distance, self.agents[i].x, self.agents[i].y],)
        # sort on 0 value
        closest_sheep.sort()
        
        return closest_sheep[0]
