#!/usr/bin/env python3

import os
import time
import pandas as pd
import random
import wx
from psychopy import event, visual, monitors, core
import datetime
import sys
import numpy as np
import subprocess
# from statemachine import StateMachine, State
import csv
from datetime import datetime
import json
import ndjson
from nico.main import startup, setmode, shutdown
from nico.speak import speak

participant = sys.argv[1]
country = sys.argv[2]
condition = sys.argv[3]

startup()

input("Press Enter to continue...")

code_path = "C:/Experiment/Drawing/"
images_dir = code_path + "Images/"
experiment_dir = images_dir + "Experiments_raw/"
script_path = code_path + "drawing.py"
script_path_trial = code_path + "drawing_trial.py"

if os.path.isdir(images_dir):
    print("folder already exist")
else:
    os.mkdir(images_dir)
    os.mkdir(experiment_dir)

####### CHANGE THE PATH
now = datetime.now()
date_hour = now.strftime("_%d-%m-%Y_%H-%M-%S")
participant_dir = participant + str(date_hour)
path_folder_participant = images_dir + participant_dir
os.mkdir(path_folder_participant)

seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # 0 is sheep, 1 is duck, 2 is computer
random.shuffle(seq)
categories = ['Sheep', 'Bus', 'Bee',
              'Face', 'Computer', 'Duck',
              'Mosquito', 'Map', 'Sea Turtle',
              'Pizza', 'Teddy Bear', 'Pig']

global win

####### CHANGE THE PATH

drawing_enjoyment = 0.0
drawing_frequency = 0.0
drawing_percentage = 0.0

difficulty_ranking = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
enjoyment_ranking = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
likeability_ranking = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

latency_time = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
total_drawing_time = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
number_of_strokes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


def save_rankings(n):


    path_var = images_dir + "/" + str(categories[n]) + "_quantitative_data.ndjson"

    ranking_data = {
        'Participant_ID': participant,
        'Country': country,
        'Condition': condition,
        'Latency_time': round(latency_time[n], 2),
        'Total_time': round(total_drawing_time[n], 2),
        'Number_of_Strokes': number_of_strokes[n],
        'Enjoyment_ranking': enjoyment_ranking[n],
        'Difficulty_ranking': difficulty_ranking[n],
        'Likeability_ranking': likeability_ranking[n]
    }

    if os.path.isfile(path_var):
        with open(path_var) as f:
            data = []
            reader = ndjson.reader(f)
            for i in reader:
                data.append(i)
        data.append(ranking_data)

    # Writing items to a ndjson file
        with open(path_var, 'w') as f:
            writer = ndjson.writer(f, ensure_ascii=False)
            for d in data:
                writer.writerow(d)

    else:
        open(path_var, "x")
        with open(path_var, "w") as file:
            json.dump(ranking_data, file)

    return


def drawing_questions(n):
    text = visual.TextStim(win, text="How difficult it was to draw the " + categories[n] + "? \n"
                            "(1 - not difficult, 7 - extremely difficult)", color=(1, 1, 1),
                           pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center",
                           wrapWidth=400)
    text.draw()

    button_continue = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                                        fillColor=[-0.3, -0.3, -0.3], pos=[0, -350], size=(400, 150), units='pix')
    # button_continue.draw()

    slider = visual.Slider(win, ticks=(0, 100), labels=(0, 100), granularity=0.1, pos=(0, -100), size=(1000, 50),
                           units='pix')

    slider.setMarkerPos(200)
    slider.getMouseResponses()
    slider.setReadOnly(False, log=None)
    slider.draw()
    win.flip()

    touch = False
    print(slider.markerPos)

    while touch == False:
        if slider.getMouseResponses():
            rating = slider.getRating()
            slider.setMarkerPos(rating)
            button_continue.draw()
            text.draw()
            slider.draw()
            win.flip()

        if myMouse.isPressedIn(button_continue):
            difficulty_ranking[n] = rating
            touch = True

    blue_window()

    text = visual.TextStim(win, text="How much did you enjoy drawing the " + categories[n] + "? \n"
                            "(1 - not enjoyed, 7 - extremely enjoyed)", color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center",
                           wrapWidth=400)
    text.draw()

    button_continue = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                                        fillColor=[-0.3, -0.3, -0.3], pos=[0, -350], size=(400, 150), units='pix')
    # button_continue.draw()

    slider = visual.Slider(win, ticks=(0, 7), labels=(0, 7), granularity=0.1, pos=(0, -100), size=(1000, 50),
                           units='pix')

    slider.setMarkerPos(200)
    slider.getMouseResponses()
    slider.setReadOnly(False, log=None)
    slider.draw()
    win.flip()

    touch = False
    print(slider.markerPos)

    while touch == False:
        if slider.getMouseResponses():
            rating = slider.getRating()
            slider.setMarkerPos(rating)
            button_continue.draw()
            text.draw()
            slider.draw()
            win.flip()

        if myMouse.isPressedIn(button_continue):
            enjoyment_ranking[n] = rating
            touch = True

    blue_window()

    text = visual.TextStim(win, text="How much do you like your drawing of the " + categories[n] + "? \n"
                           "(1 - not liked, 7 - liked a lot)", color=(1, 1, 1), pos=(0.0, 15.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center",
                           wrapWidth=400)
    text.draw()

    image = visual.ImageStim(win, image=path_folder_participant + "/" + categories[n] + ".png", size=(600, 337),
                             units='pix', pos=(0.0, -5.0))
    image.draw()

    button_continue = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                                        fillColor=[-0.3, -0.3, -0.3], pos=[0, -450], size=(400, 150), units='pix')
    # button_continue.draw()

    slider = visual.Slider(win, ticks=(0, 7), labels=(0, 7), granularity=0.1, pos=(0, -250), size=(1000, 50),
                           units='pix')

    slider.setMarkerPos(200)
    slider.getMouseResponses()
    slider.setReadOnly(False, log=None)
    slider.draw()
    win.flip()

    touch = False
    print(slider.markerPos)

    while touch == False:
        if slider.getMouseResponses():
            rating = slider.getRating()
            slider.setMarkerPos(rating)
            button_continue.draw()
            text.draw()
            image.draw()
            slider.draw()
            win.flip()

        if myMouse.isPressedIn(button_continue):
            likeability_ranking[n] = rating
            touch = True

    blue_window()
    save_rankings(n)

    return


def drawing_activity(i):

    win.close()
    print("window closed, ready to open drawing")

    p = subprocess.Popen(
        ["C:/Experiment/Drawing/drawing_venv/Scripts/python", script_path, categories[i], path_folder_participant,
         condition, country, experiment_dir], stdout=subprocess.PIPE)
    p.wait()

    output = []
    output = p.stdout.read()

    array = np.fromstring(output.decode(), dtype=float, sep=',')

    print(categories[i])

    speak("Ok")

    latency_time[i] = array[0]
    total_drawing_time[i] = array[1]
    number_of_strokes[i] = array[2]

    # time.sleep(0.7)

    setmode(3)

    configure()

    text = visual.TextStim(win, text="Now please answer to some questions.", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    button = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3], pos=[0, -250], size=(400, 150), units='pix')
    button.draw()

    win.flip()

    touch = False

    while touch == False:
        if myMouse.isPressedIn(button):
            touch = True

    drawing_questions(i)

    return


def drawing_task(n):

    time.sleep(1.5)

    text = visual.TextStim(win, text="Are you ready to draw?", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    button = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3], pos=[0, -250], size=(400, 150), units='pix')
    button.draw()

    win.flip()

    touch = False

    while touch == False:
        if myMouse.isPressedIn(button):
            touch = True

    time.sleep(0.2)
    buttons = myMouse.getPressed()
    myMouse.clickReset(buttons)

    setmode(0)

    text = visual.TextStim(win, text="Please draw with your finger the...\n", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)

    text2 = visual.TextStim(win, text=categories[n], color=(1, -0.7, -0.7), pos=(0.0, -1.0),
                            colorSpace='rgb', bold=True, height=4.5, anchorHoriz="center", wrapWidth=400)

    text.draw()
    text2.draw()

    win.flip()

    time.sleep(4)

    drawing_activity(n)

    return


def artistic_questions():
    global drawing_enjoyment, drawing_frequency, drawing_percentage


    text = visual.TextStim(win,
                           text="How much do you enjoy free-hand drawing? \n "
                                "(click on the slider and then drag the marker) \n"
                                "(1 - extremely little, 7 - extremely much)",
                           color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    button_continue = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                                        fillColor=[-0.3, -0.3, -0.3], pos=[0, -350], size=(400, 150), units='pix')
    # button_continue.draw()

    slider = visual.Slider(win, ticks=(0, 7), labels=(0, 7), granularity=0.1, pos=(0, -100), size=(1000, 50),
                           units='pix')

    slider.setMarkerPos(200)
    slider.getMouseResponses()
    slider.setReadOnly(False, log=None)
    slider.draw()
    win.flip()

    touch = False
    print(slider.markerPos)

    while touch == False:
        if slider.getMouseResponses():
            rating = slider.getRating()
            slider.setMarkerPos(rating)
            button_continue.draw()
            text.draw()
            slider.draw()
            win.flip()

        if myMouse.isPressedIn(button_continue):
            drawing_enjoyment = rating
            touch = True

    blue_window()

    text = visual.TextStim(win, text="How often do you draw sketches? \n (1 - extremely little, 7 - extremely much)",
                           color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    button_continue = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                                        fillColor=[-0.3, -0.3, -0.3], pos=[0, -350], size=(400, 150), units='pix')
    # button_continue.draw()

    slider = visual.Slider(win, ticks=(0, 7), labels=(0, 7), granularity=0.1, pos=(0, -100), size=(1000, 50),
                           units='pix')

    slider.setMarkerPos(200)
    slider.getMouseResponses()
    slider.setReadOnly(False, log=None)
    slider.draw()
    win.flip()

    touch = False
    print(slider.markerPos)

    while touch == False:
        if slider.getMouseResponses():
            rating = slider.getRating()
            slider.setMarkerPos(rating)
            button_continue.draw()
            text.draw()
            slider.draw()
            win.flip()

        if myMouse.isPressedIn(button_continue):
            drawing_frequency = rating
            touch = True

    blue_window()

    text = visual.TextStim(win, text="Imagine other 100 people drawing the same sketches as yours: \n"
                            " how many of them do you think will draw better than you?",
                           color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center",
                           wrapWidth=400)
    text.draw()

    button_continue = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                                        fillColor=[-0.3, -0.3, -0.3], pos=[0, -350], size=(400, 150), units='pix')
    # button_continue.draw()

    slider = visual.Slider(win, ticks=(0, 100), labels=(0, 100), granularity=0.1, pos=(0, -100), size=(1000, 50),
                           units='pix')

    slider.setMarkerPos(200)
    slider.getMouseResponses()
    slider.setReadOnly(False, log=None)
    slider.draw()
    win.flip()

    touch = False
    print(slider.markerPos)

    while touch == False:
        if slider.getMouseResponses():
            rating = slider.getRating()
            slider.setMarkerPos(rating)
            button_continue.draw()
            text.draw()
            slider.draw()
            win.flip()

        if myMouse.isPressedIn(button_continue):
            drawing_percentage = rating
            touch = True

    return


def blue_window():
    blue_poly = visual.Polygon(win, edges=4, fillColor=[-0.4, -0.4, 1], colorSpace='rgb', pos=[0, 0], size=[4000, 4000],
                               units='pix', ori=0)


    blue_poly.draw()
    win.flip()  # show the stim
    time.sleep(0.1)

    return


# function to wait for the touch of the mouse
def wait_touch():
    myMouse.clickReset()


    buttons = myMouse.getPressed()
    print(buttons)
    while buttons[0] == False | buttons[1] == False | buttons[2] == False:
        buttons = myMouse.getPressed()

    print(buttons)
    print("click")
    time.sleep(1)

    return


def configure():
    global win, widthPix, heightPix, monitorWidth, viewdist, monitorname, scrn, mon, myMouse, myKey


    widthPix = 1920
    heightPix = 1080
    monitorWidth = 47.7
    # monitorWidth = 30.9
    viewdist = 25.4
    monitorname = 'testMonitor'
    scrn = 1

    mon = monitors.Monitor(monitorname, width=monitorWidth, distance=viewdist)
    mon.setSizePix((widthPix, heightPix))

    win = visual.Window(
        monitor=mon,
        size=(widthPix, heightPix),
        color=(-0.4, -0.4, 1),
        colorSpace='rgb',
        units='deg',
        screen=scrn,
        allowGUI=True,
        fullscr=True
    )

    myMouse = event.Mouse(win)
    # myMouse.setPos(newPos=(300, 300))

    return


def main():


    # subprocess.run(["xrandr", "--output", "eDP", "--off"])

    configure()

    setmode(1)
    # speak("hello")

    text = visual.TextStim(win, text="Welcome!\nThis is a first trial to help\n"
                            "you understand how the drawing activity will work.", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    button = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3], pos=[0, -250], size=(400, 150), units='pix')
    button.draw()

    win.flip()

    touch = False

    while touch == False:
    # print(myMouse.isPressedIn(button))

        if myMouse.isPressedIn(button):
            print(myMouse.isPressedIn(button))
            touch = True

    text = visual.TextStim(win, text="When you are ready, press the button and\n"
                                "a subject to be drawn will appear on the screen."
                           , color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    button = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3], pos=[0, -250], size=(400, 150), units='pix')
    button.draw()

    win.flip()

    touch = False

    while touch == False:
        if myMouse.isPressedIn(button):
            touch = True

    setmode(0)

    text = visual.TextStim(win, text="Please draw with your finger the...\n", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)

    text2 = visual.TextStim(win, text="Tree", color=(1, -0.7, -0.7), pos=(0.0, -1.0),
                            colorSpace='rgb', bold=True, height=4.5, anchorHoriz="center", wrapWidth=400)

    text.draw()
    text2.draw()

    win.flip()

    time.sleep(4)

    win.close()

    p = subprocess.Popen(["C:/Experiment/Drawing/drawing_venv/Scripts/python", script_path_trial])
    p.wait()

    speak("Ok")

    # time.sleep(0.7)

    setmode(1)

    configure()

    text = visual.TextStim(win, text="Great!\n Is everything clear? Then you can\n"
                            "proceed with the actual experiment.", color=(1, 1, 1), pos=(0.0, 11.0), colorSpace='rgb',
                           bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    button = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3], pos=[0, -250], size=(400, 150), units='pix')
    button.draw()

    win.flip()

    touch = False

    while touch == False:
        if myMouse.isPressedIn(button):
            touch = True

    text = visual.TextStim(win, text="Welcome!\nWe will ask you to draw several pictures\n"
                                     "and then answer some simple questions.\n"
                                     "Are you ready? ", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()

    button = visual.ButtonStim(win, text="Click to continue", color=[1, 1, 1], colorSpace='rgb',
                               fillColor=[-0.3, -0.3, -0.3], pos=[0, -250], size=(400, 150), units='pix')
    button.draw()

    win.flip()

    touch = False

    while touch == False:
        if myMouse.isPressedIn(button):
            touch = True

    setmode(3)

    artistic_questions()

    for i in seq:
        drawing_task(i)


    path_var = code_path + "/artistic_skills.ndjson"

    artistic_data = {
        'Participant_ID': participant,
        'Country': country,
        'Condition': condition,
        'Artistic_enjoyment': drawing_enjoyment,
        'Artistic_frequency': drawing_frequency,
        'Artistic_percentage': drawing_percentage,
        'Average_latency_time': round(np.mean(latency_time), 2),
        'Average_total_time': round(np.mean(total_drawing_time), 2),
        'Average_number_strokes': round(np.mean(number_of_strokes), 2),
        'Average_enjoyment_ranking': round(np.mean(enjoyment_ranking), 2),
        'Average_difficulty_ranking': round(np.mean(difficulty_ranking), 2),
        'Average_likeability_ranking': round(np.mean(likeability_ranking), 2)
    }

    if os.path.isfile(path_var):
        with open(path_var) as f:
            data = []
            reader = ndjson.reader(f)
            for i in reader:
                data.append(i)
        data.append(artistic_data)

        # Writing items to a ndjson file
        with open(path_var, 'w') as f:
            writer = ndjson.writer(f, ensure_ascii=False)
            for d in data:
                writer.writerow(d)

    else:
        open(path_var, "x")
        with open(path_var, "w") as file:
            json.dump(artistic_data, file)

    setmode(1)

    text = visual.TextStim(win, text="Thank you very much!", color=(1, 1, 1), pos=(0.0, 11.0),
                           colorSpace='rgb', bold=False, height=2.5, anchorHoriz="center", wrapWidth=400)
    text.draw()
    win.flip()

    wait_touch()

    # subprocess.run(["xrandr", "--output", "eDP", "--mode", "1920x1080", "--panning", "1920x1080", "--pos", "1920x0", "--primary"])

if __name__ == '__main__':
    main()

    sys.exit()