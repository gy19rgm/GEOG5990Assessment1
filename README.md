## GEOG5990Assessment1
#### Repository of GEOG5990 Assessment 1 material

This is an Agent Based Model in which sheep and sheepdogs interact within a 300 by 300 field environment, eating, sharing resources and running as they go.


## Getting Started
This model was created in Spyder (Anaconda3). The version of python is version is 3.7.

### Repository Contents:
1. **LICENSE**: GNU General Public License v3.0
2. **Model.py:** Main agent-based model code
3. **agentframework.py**: code containing Agents (sheep) and Dogs class
4. **in.txt:** text file containing values used in setting up the environment
5. **README.md:** this file is the README.md file - it explains the contents of the GEOG5990Assessment1 folder

### Prerequisites
Download the relevant files from this repository into your personal folder
* Model.py - main model which initiates the agent-based model animation using numbers obtained from the GUI
* agentframework.py - agent framework which sets up the agents (sheep) and sheepdogs and their relevant behaviours
* in.txt - text file containint integers used to set up the values of the field environment 

If using Spyder, the backend may need to be changed in order for matplotlib to render graphics succesfully. This can be set in Spyder by selecting 'Tools' > 'Preferences' > IPython console > 'Graphics' > adjust the backend drop-down list to read TkInter > OK > Restart Spyder


## Running the model
The model can be run from the command prompt by navigating to the current working directory and typing 'python Model.py'.

Alternatively, the model can be run from within a programming software, such as Spyder.

Once the GUI is visible, follow the instructions on the sliders and buttons to 1. choose the number of agents (sheep), 2. choose the number of sheepdogs, 3. Set the animals up within the field environment and, 4. run the model.

### Expectations
Upon opening the model, a blank GUI will appear. From here, the number of sheep and sheepdogs can be selected by adjusting the sliders. Button "3. Press here to set up the field" must be pressed in order for the model to retrieve the desired number of sheep and sheepdogs. Once button three has been pressed, the model can be run from either 'Run model' in the drop down menu or button "4. Watch the sheepdog herd the sheep!". 

Once running, sheep will move randomly, eating 10 units of grass each iteration. Every move sheep will check whether they have  are other sheep nearby

The animation will end when either a. total number of iterations are reached or, b. all sheep's personal stores reach a pre-determined capacity.

## Closing the model
To close the model, the user can choose 'Close model' in the drop down menu or click the "Close the model" button. This must also be done to re-run the model, and then the model must be re-opened.


## Author
* R Martin, gy19rgm, University of Leeds


## License
This project is licensed under the GNU General Public License v3.0 - see the [License.md](https://github.com/gy19rgm/GEOG5990Assessment1/blob/master/LICENSE) file for further details