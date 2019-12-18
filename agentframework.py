# -*- coding: utf-8 -*-
"""

Author: R Martin, gy19rgm, University of Leeds

Project Version 1

"""

# import libraries
import random

# define behaviour for class agents (sheep)
class Agent():
       
    def __init__(self, environment, agents, dogs):
        '''
        Function to initiate class Agent (sheep) and set up behaviours
        This includes defining xy values, the environment and the store and giving
        sheep the ability to know about the location of other sheep and all sheepdogs
        
        Params:
            environment - environment from Model.py
            agents - list of agents from Model.py
            dogs - list of dogs from Model.py
        ''' 
        self.x = random.randint(0,299) # randomly generated variable
        self.y = random.randint(0,299) # randomly generated variable
        self.environment = environment
        self.agents = agents 
        self.dogs = dogs
        self.store = 0 # variable representing the food storage capacity of the sheep, initialised as zero
        
    def __str__(self):
        '''
        Function that defines own values in string format
        
        Returns:
            Values in string format
        '''
        return str(self.y) + " " + str(self.x)  

    def check_field(self):
        '''
        Function to check the field environment and return information about the closest sheepdog
           
        Returns:
            Distance, x and y variables for the closest dog
        '''        
        closest_dog = [] # empty list to be filled with values of all dogs
        
        for i in range(len(self.dogs)): # for self calculate distance of all dogs
            distance = self.distance_between(self.dogs[i]) # distance between sheep and a dog, calculated and added to the closest_dog list
            closest_dog.append([distance, self.dogs[i].x, self.dogs[i].y],)
        closest_dog.sort() # sort so smallest distance first
        
        return closest_dog[0]

    def move(self):
        '''
        Function to move away from a sheepdog or to move randomly
        If a sheepdog is within sight then move away from it, else move randomly
        '''        
        close = self.check_field() # value returned from the check_field function
    
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
                         
    def eat(self):
        '''
        Function to 'eat' grass, removing it from the field environment and adding it to personal store
        '''   
        if self.environment[self.y][self.x] > 10: # if grass has unit > 10
            self.environment[self.y][self.x] -= 10 # eat 10 units of grass
            self.store += 10 # give 10 units of grass to personal store
         
    def distance_between(self, agent):
        '''
        Function to return distance between self and another sheep
        
        Params:
           agent - list of sheep and information about each one
        
        Returns:
            Distance between self and another sheep
        '''
        return (((self.x - agent.x)**2) + ((self.y - agent.y)**2))**0.5        
    
    def share_with_neighbours(self, neighbourhood):
        '''
        Function to share grass from personal store with neighbouring sheep's store
        
        Params:
            neighbourhood - neighbourhood variable defined in Model.py
        
        Returns:
            Updated values for each sheep's stores
        '''
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
  

# define behaviour for class dog (sheepdogs)
class Dog(Agent):
    
    def __init__(self, environment, agents, dogs, y, x):
        '''
        Function to initiate class Dog (sheepdog) and set up behaviours
        Environement, agents and dogs are inherited from class Agent
    
        Params:      
            environment - environment from Model.py, inherited from Agent
            agents - list of agents from Model.py, inherited from Agent
            dogs - list of dogs from Model.py, inherited from Agent
            y - y value from HTML file opened in Model.py, if no value is found one is assigned randomly
            x - x value from HTML file opened in Model.py, if no value is found one is assigned randomly
        '''
        super().__init__(environment, agents, dogs) # inherit environment, agents and dogs from class Agent
        
        self.y = y 
        self.x = x
        if y == None:
            self.y = random.randint(0,299)
        else:
            self.y = y # else use y from html
        if x == None:
            self.x = random.randint(0,299)
        else:
            self.x = x # else use x from html

    def check_vicinity(self):
        '''
        Function to check the field environment and return information about the closest sheep

        Returns:
            Distance, x and y variables for the closest sheep
        '''
        closest_sheep = [] # empty list to be filled with values of all sheep
        
        for i in range(len(self.agents)): # for self calculate distance of all sheep
            distance = self.distance_between(self.agents[i]) # distance between dog and a sheep, calculated and added to the closest_sheep list
            closest_sheep.append([distance, self.agents[i].x, self.agents[i].y],)
        closest_sheep.sort() # sort so smallest distance first
        
        return closest_sheep[0]

    def move(self):          
        '''
        Function to move towards a sheep or to move randomly
        If a sheep is within sight then move towards it, else move randomly
        '''
        closest = self.check_vicinity() # value returned from the check_vicinity function
     
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