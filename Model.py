# -*- coding: utf-8 -*-
"""

Author: R Martin, University of Leeds, 201369797

Project Version 1

"""

# import libraries
import agentframework
import bs4
import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.animation
import matplotlib.pyplot
import requests
import tkinter


# obtain data from HTML file and allocate to xy variables
r = requests.get("https://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html", verify=False)
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')

td_ys = soup.find_all(attrs={"class": "y"})
td_xs = soup.find_all(attrs={"class": "x"})
#print(str(td_ys[1]))
#print(str(td_xs[1]))

# open the field/environment data from in.txt file
with open('in.txt', newline='') as f: # automatically closes due to indentation
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    
    environment = []
    
    for row in reader:
        rowlist = []
        for value in row:
            rowlist.append(value)
        environment.append(rowlist)

# set figure size and axes
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])

agents = [] # list of agents
dogs = [] # list of dogs
num_of_iterations = 100
num_of_agents = 10
num_of_dogs = 2
neighbourhood = 20 # distance sheep can see

def setup_agents():
    '''
    Function to set up Class Agent (sheep) and Class Dogs (sheepdogs) using values from GUI sliders
    Initalise sheep and sheepdogs into the agentframework
    
    Returns:
        if uncommented, prints number of sheep and number of wolves, as selected on GUI slider
    '''
    global num_of_agents # global variable defining number of sheep updated by value on GUI slider
    global num_of_dogs # global variable defining number of sheepdogs updated by value on GUI slider
    num_of_agents = slide1.get()
    num_of_dogs = slide2.get()
    print('Total number of Agents (sheep):', num_of_agents)
    print('Total number of sheepdogs:', num_of_dogs)
    
    # Make the sheep
    for i in range(num_of_agents):
        agents.append(agentframework.Agent(environment, agents, dogs))           
#        print('agents:', agents[i])
        
#    # check sheep can return info about a different sheep
#    print('Agent 6 from agent 1 point of view', agents[1].agents[6].x)

    # Make the sheep dogs
    for i in range(num_of_dogs):
        y = int(td_ys[i].text) # integer obtained from html file
        x = int(td_xs[i].text) # integer obtained from html file
        dogs.append(agentframework.Dog(environment, agents, dogs, y, x))    
#        print('dogs:', dogs[i])

carry_on = True

def update(frame_number):
    '''
    Function to determine what is done during each iteration.
    The function plots the environment, makes the grass environment grow and runs sheep and sheepdog behavious
    
    Params:
        frame_number - the number of iterations
    '''
    fig.clear()
    global carry_on # global boolean value which determines whether iterations continue
    matplotlib.pyplot.ylim(0, 300)
    matplotlib.pyplot.xlim(300, 0)
    matplotlib.pyplot.imshow(environment) # grid of numbers describing the field environment

    # make the environment ('grass') grow each iteration     
    for i in range(300):
        for j in range(300):
            environment[j][i] += 1
    
    #print(len(agents), num_of_agents)
    for i in range(num_of_agents): # for each of the total number of sheep
        # call methods from agentframework.py 
        agents[i].check_field()
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)
        
    for i in range(num_of_dogs): # for each of the total number of sheepdogs
        # call methods from agentframework.py 
        dogs[i].check_vicinity()
        dogs[i].move()
          
        # stop before num_of_iterations if agents' stores are all greater than a value
        if agents[i].store > 900:
            carry_on = False
#            print("stopping condition")
            
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y, c = "white")

    for i in range(num_of_dogs):
        matplotlib.pyplot.scatter(dogs[i].x,dogs[i].y, marker = "D", c = "black")

def gen_function():
    '''
    Check whether stopping condition has been met, and if so, terminate model
    Stopping conditions are either number of iterations or a sheep's store becomes full 
        
    Returns:
        Prints stopping iteration number
        If uncommented, prints the value of the store for all agents
    '''
    a = 0
    global carry_on # global boolean value which determines whether iterations continue
    while (a < num_of_iterations) & (carry_on): # total iterations defined at the start of the model
        yield a # Returns control and waits next call
        a = a + 1
    print("Stopping iteration number:", a)
#    # check final agent.store value
#    for a in agents:
#        print("store" [i] ':', a.store)

def run():
    '''
    Function to run the model in the form of an animation
    '''
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()

def close():
    '''
    Function to close the model
    '''
    root.destroy()
    
# Set up GUI
root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
menubar = tkinter.Menu(root)
root.config(menu=menubar)
model_menu = tkinter.Menu(menubar)
menubar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run, state="normal")
model_menu.add_command(label="Close model", command=close)

# Add sliders and buttons to GUI
slide1= tkinter.Scale(root, bd=5, from_=50, label= "1. Choose the number of sheep:", 
                      length=200, orient='horizontal', resolution=1, to=150)
slide1.pack(fill='x')

slide2= tkinter.Scale(root, bd=5, from_=5, label= "2. Choose the number of sheepdogs:",
                      length=200, orient='horizontal', resolution=1, to=10)
slide2.pack(fill='x')
                      
butt1=tkinter.Button(root, command= setup_agents, text= "3. Press here to set up the field")
butt1.pack(fill='x')

butt2=tkinter.Button(root, command=run, text="4. Watch the sheepdog herd the sheep!")
butt2.pack(fill='x')

butt3=tkinter.Button(root, command=close, text="Close the model")
butt3.pack(fill='x')

tkinter.mainloop()