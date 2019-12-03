# -*- coding: utf-8 -*-
"""

@author: gy19rgm, University of Leeds

Project Version 1

"""

# import libraries
import random

'''
Class Agent (sheep)
'''
class Agent ():
    
    '''
    @environment    environment from Model.py
    @agents         list of agents from Model.py
    @dogs           list of dogs from Model.py
    '''    
    def __init__(self, environment, agents, dogs):
        self.x = random.randint(0,299)
        self.y = random.randint(0,299)
        self.environment = environment
        self.agents = agents 
        self.dogs = dogs
        self.store = 0  # sets initial agent (sheep) store as zero
        
    def __str__(self): # defines how to return info about self
        return str(self.y) + " " + str(self.x)  
        
    '''
    Check field to return information about closest dog
    '''
    def check_field(self):
        
        closest_dog = [] # set up list called closest dog
        
        for i in range(len(self.dogs)): # for self calculate distance of all dogs
            distance = self.distance_between(self.dogs[i])
            closest_dog.append([distance, self.dogs[i].x, self.dogs[i].y],)
        closest_dog.sort() # sort so smallest distance first
        
        return closest_dog[0] # return information for the closest dog
    
    '''
    Move away from sheep dog or move randomly
    '''
    def move(self):
        
        close = self.check_field() # close = closest_dog from check_field
    
        if close[0] < 20: # if closest dog is within 20
            
            if self.x == close[1]: # if x values are the same then pass
                pass
            if self.x - close[1] < 0: # when dog x is greater than sheep
                self.x = self.x - 2 # move closer to value 0 to get away
            else:
                self.x = self.x + 2 # move away from value 0 to get away

            if self.y == close[2]: # if y values are the same then pass
                pass
            if self.y - close[2] < 0: # when dog y is greater than sheep
                self.y = self.y - 2 # move closer to value 0 to get away
            else:
                self.y = self.y + 2 # move away from value 0 to get away                

        else: # what to do if there is no dog within 20
            # add or minus 2 to current xy values based on random number
            if random.random() < 0.5: 
                self.y += 1
            else:
                self.y -= 1
                
            if random.random() < 0.5:
                self.x += 1
            else:
                self.x -= 1
            
        # Check if sheep will reach the environment boundary
        # If xy values become 0 or 299, remain at 0 and 299
        if self.y < 0: 
            self.y = 0 
        if self.x < 0: 
            self.x = 0 
        if self.y > 299: 
            self.y = 299 
        if self.x > 299: 
            self.x = 299 

    '''
    Eat grass and remove from environment
    '''                            
    def eat(self):
        if self.environment[self.y][self.x] > 10: # if grass has unit > 10
            self.environment[self.y][self.x] -= 10 # eat 10 units of grass
            self.store += 10 # give to personal store

    '''
    Returns distance between self and other sheep (agent)
    '''           
    def distance_between(self, agent): # calculate distance between self and other sheep
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5        
    
    '''
    Share grass from personal store with neighbour agent's store
    '''
    def share_with_neighbours(self, neighbourhood):
        self.neighbourhood = neighbourhood
        # Loop through the agents in self.agents
        for agent in self.agents:
            distance = self.distance_between(agent)
            # If distance is less than or equal to the neighbourhood
            if distance <= neighbourhood:
                # calculate combined store and share equally
                sum = self.store + agent.store
                average = sum / 2
                self.store = average
                agent.store = average
  

'''
Sheepdog class
'''
class Dog(Agent):
    
    '''
    @environment    environment from Model.py
    @agents         list of agents from Model.py
    @dogs           list of dogs from Model.py
    @y              y value from HTML file opened in Model.py
    @x              x value from HTML file opened in Model.py
    '''
    def __init__(self, environment, agents, dogs, y, x):
        super().__init__(environment, agents, dogs) # inherit from class Agent
        
        self.y = y # define y from y defined by HTML file in Model.py
        self.x = x # define x from x defined by HTML file in Model.py
        if y == None:# if no y value is found
            self.y = random.randint(0,299) # assign random value to y
        else:
            self.y = y # else use y
        if x == None: # if no x value is found
            self.x = random.randint(0,299) # assign random value to x
        else:
            self.x = x # else use x

    '''
    Check field to return information about closest sheep
    '''
    def check_vicinity(self):
       
        closest_sheep = [] # set up list called closest sheep
        
        for i in range(len(self.agents)): # for self calculate distance of all sheep
            distance = self.distance_between(self.agents[i])
            closest_sheep.append([distance, self.agents[i].x, self.agents[i].y],)
        closest_sheep.sort() # sort so smallest distance first
        
        return closest_sheep[0] # return information for closest dog

    '''
    Move towards sheep (via sprint then stalk motion) or move randomly
    '''
    def move(self):  
        
        closest = self.check_vicinity() # closest = sheep from check_vicinity
     
        if closest[0] < 30: # if sheep is within 30 
          
            self.x += (closest[1]-self.x)/2 # x value becomes half closer to sheep            
            self.y += (closest[2]-self.y)/2 # y value becomes half closer to sheep
        
        else: # what to do if there is no sheep within 30
            # add or minus 5 to current xy values based on random number
            if random.random() < 0.5:
                self.y += 5
            else:
                self.y -= 5
                
            if random.random() < 0.5:
                self.x += 5
            else:
                self.x -= 5

        # Check if dog will reach the environment boundary
        # If xy values become 0 or 299, remain at 0 and 299
        if self.y < 0:
            self.y = 0
        if self.x < 0:
            self.x = 0
        if self.y > 299:
            self.y = 299
        if self.x > 299:
            self.x = 299