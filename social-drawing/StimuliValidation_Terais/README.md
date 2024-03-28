# StimuliValidation_Terais
Repository with the code to perform the Stimuli Validation experiment for the Shared Drawing project.

## Brief description of the repository and the architecture
Inside the repository you can find the following files:
* *stimuli.py*: main script to launch in the condition "no robot";
* *stimuli_nico.py*: main script to launch in the condition "robot";
* *drawing.py*: script to handle the drawing part and the storage of the images and coordinates of the strokes;
* *drawing_trial.py*: script to handle the trial part in which the user will draw a category not between the important ones.

### Architecture
The architecture is very basic: the `stimuli.py`/`stimuli_nico.py` scripts contain all the graphic windows (created via the psychopy library) for the interaction with the user and launch both the `drawing_trial.py` and `drawing.py` scripts (as subprocesses), waiting for them to finish before going on with the questions.
In the drawing scripts a tkinter canva is configured so the participants can draw freely with their finger.

## Folder and files created during the experiment
At the first launch of the code, you will notice that a folder `Images` has been created, in which there will be created other folders for storage of the drawings created by the participants. The drawings will be saved as .png files. Inside these personal folders, other two .csv files will be created (these are technical .csv files to store the coordinates of each stroke for every category and the personal answer to the questionnaire).

## How to run the code
First of all, clone this repository wherever you prefer with the following commands:
```
cd the/chosen/folder
git clone https://github.com/LorenzoMorocutti/StimuliValidation_Terais.git
```
Then, go to the stimuli.py script and change the paths at the beginning of the file (to match the location in which you cloned the repository).
Do the same for the drawing.py script.
At this point you should go to the settings --> Appearance --> turn on the 'Auto-hide the dock' to hide the lateral bar during the running of the application, so that the participant can draw freely on the entire screen.
Now you are ready to run the code with the following command:
```
python3 stimuli.py 'name_of_the_participant'
```
and you are done!
