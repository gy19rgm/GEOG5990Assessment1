# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: gy19rgm
"""

# Import packages
import matplotlib
matplotlib.use('TkAgg')
import tkinter
import matplotlib.pyplot
import agentframework
import csv
import random
import matplotlib.animation
import requests
import bs4

# Obtain data from HTML file and allocate to y, x, variables
r = requests.get("https://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html", verify=False)
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')

td_ys = soup.find_all(attrs={"class": "y"})
td_xs = soup.find_all(attrs={"class": "x"})
#print(td_ys)
#print(td_xs)

# Check the agentframework is being called successfully 
#a = agentframework.Agent()
#print("Agent (y,x):", a.y, a.x)

# Open the environment .txt file
with open('in.txt', newline='') as f:   # everything indented is instruction, automatically closes
#    f = open('in.txt', newline='') 
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    
    # Lines here happen before any data is processed
    environment = []
    
    for row in reader:				# A list of rows
        # Lines here happen before each row is processed
        rowlist = []
        for value in row:
            # do something with values.
            rowlist.append(value)
        # Lines here happen before after row is processed
        environment.append(rowlist)

''' match figure size to computer screen!'''
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

dogs = []
agents = []
num_of_iterations = 650
num_of_agents = 10
num_of_dogs = 2
neighbourhood = 20      # distance sheep can see

# Set up sheep and sheepdogs using values from sliders
def setup_agents():
    global num_of_agents
    global num_of_dogs
    num_of_agents = slide1.get()
    num_of_dogs = slide2.get()
    print('Total agents:', num_of_agents)
    print('Total dogs:', num_of_dogs)
    
    # Make the sheep
    for i in range(num_of_agents):
 
        agents.append(agentframework.Agent(environment, agents, dogs))           
#        print('agents:', agents[i])
        
    # Check sheep can return info about a different sheep
    #print(agents[1].agents[6].x)

    # Make the dogs
    for i in range(num_of_dogs):
        y = int(td_ys[i].text)
        x = int(td_xs[i].text)
        dogs.append(agentframework.Dog(environment, agents, dogs, y, x))    
#        print('dogs:', dogs[i])

carry_on = True

def update(frame_number):
    fig.clear()
    global carry_on
    matplotlib.pyplot.ylim(0, 300)
    matplotlib.pyplot.xlim(300, 0)
    matplotlib.pyplot.imshow(environment)

    # Make the environment ('grass') grow each iteration     
    for i in range(300):
        for j in range(300):
            environment[j][i] += 5
    
#    print(len(agents), num_of_agents)
    for i in range(num_of_agents):
        # Call methods from agentframework.py 
        agents[i].check_field()
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
        
    for i in range(num_of_dogs):
        dogs[i].check_vicinity()
        dogs[i].move()
        
        # This can stop iterations before total expected iterations are met     
    #    if random.random() < 0.01:
    #        carry_on = False
    #        print("stopping condition")
    
        # Stop before num_of_ iterations if agents' stores are all greater than a value
        if agents[i].store > 600:
            carry_on = False
            print("stopping condition")

    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y, c = "white")

    for i in range(num_of_dogs):
        matplotlib.pyplot.scatter(dogs[i].x,dogs[i].y, marker = "D", c = "black")

        

def gen_function(b = [0]):
    a = 0
    global carry_on # Not actually needed as we're not assigning, but clearer
    while (a < num_of_iterations) & (carry_on) :
        yield a # Returns control and waits next call
        a = a + 1
    print("stopping iteration number:", a)
#    # Check final agent.store value
#    for a in agents:
#        print("store:", a.store)

# Run model
def run():
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()

# Close model
def close():
    root.destroy()
   
# Set up GUI
root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
menubar = tkinter.Menu(root)
root.config(menu=menubar)
model_menu = tkinter.Menu(menubar)
menubar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run, state="normal")
model_menu.add_command(label="Close model", command=close)

# Add a slider for user to choose the number of sheep
slide1= tkinter.Scale(root, bd=5, from_=50, label= "1. Choose the number of sheep:", 
                      length=200, orient='horizontal', resolution=1, to=150)
slide1.pack()

# Add a slider for user to choose the number of dogs
slide2= tkinter.Scale(root, bd=5, from_=5, label= "2. Choose the number of sheepdogs:",
                      length=200, orient='horizontal', resolution=1, to=10)
slide2.pack()
                      
# Add button get values of sheep and dogs from slider
butt1=tkinter.Button(root, command= setup_agents, text= "3. Press here to set up the field")
butt1.pack()

# Add button to run model
butt2=tkinter.Button(root, command=run, text="4. Watch the sheepdog herd the sheep!")
butt2.pack()

# Add button to close model
butt3=tkinter.Button(root, command=close, text="Close the model")
butt3.pack()

tkinter.mainloop()