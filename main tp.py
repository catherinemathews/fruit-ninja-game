# Catherine Mathews --> cmathews

''' This file initializes the variables of the overall game and each mode,
sets the backgrounds for each screen, and controls the key and mouse presses '''

from cmu_112_graphics import *
import tkinter as tk
from tkinter import Tk, font
from tkinter.font import Font
from PIL import ImageTk, Image
from timer_fired import *
from draw_game import  *
import os

'''MAIN FRAMEWORK'''

#initializes the app variables
def appStarted(app):
    app.centerX = app.width/2
    app.centerY = app.height/2
    app.menuFont1, app.menuFont2 = menuText(app)
    app.menuBackground = menuBackground(app)
    app.gameBackground = gameBackground(app)
    app.time0 = time.time()
    gameVariables(app)
    classicVariables(app)
    arcadeVariables(app)
    zenVariables(app)
    app.r = 25
    app.br = 40
    app.sr = 30
    app.timerDelay = 100
    app.timecalls = 0
    createFruit(app)

# initializes game variables 
def gameVariables(app):
    app.mode = None
    app.inMenu = False
    app.gameStarted = False
    app.onHomepage = True
    app.score = 0
    app.fruits = [ ]
    app.bombs = [ ]
    app.classicfruits = [ ]
    app.classicbombs = [ ]
    app.starfruits = [ ]
    app.combos = []
    app.mousepress = None
    app.mouserelease = None
    app.blade = "silver"
    app.slice1s = []
    app.slice2s = []

# initializes the arcade variables
def arcadeVariables(app):
    app.openArcade = False
    app.openArcadeTime = 0
    app.lives = 3
    app.arcadeGameOver = False

# initializes the zen variables
def zenVariables(app):
    app.openZen = False
    app.openZenTime = 0 
    app.zenGameOver = False
    app.sfFreq = random.randint(300, 600)
    app.fFreq = random.randint(20, 35)

# initializes the classic variables
def classicVariables(app):
    app.openClassic = False
    app.classicGameOver = False
    app.level = 1
    app.showClassicLevel = False
    app.openClassicTime = 0

# sets the menu text and font
def menuText(app):
    family = "Copperplate Gothic Bold"
    size1 = 30
    size2 = 20
    return Font(family = family, size = size1), Font(family = family, size = size2)

# sets the menu background; image inspired by old fruit ninja homepage
# code inspired by: https://www.geeksforgeeks.org/python-os-path-dirname-method/
def menuBackground(app):
    folderPath = os.path.dirname(os.path.realpath("term project"))
    pathName = folderPath + "/fruit ninja home.jpg"
    image = Image.open(pathName)
    return ImageTk.PhotoImage(image)

# sets the game background, from: https://wallpapersafari.com/w/hny8mG
# code inspired by: https://www.geeksforgeeks.org/python-os-path-dirname-method/
def gameBackground(app):
    folderPath = os.path.dirname(os.path.realpath("term project"))
    pathName = folderPath + "/game background.jpg"
    image = Image.open(pathName)
    return ImageTk.PhotoImage(image)

# returns to homepage if 'h' is clicked and changes blade color depending on key press
def keyPressed(app, event):
    if event.key == "h":
        app.gameStarted = False
        app.onHomepage = True
        app.inMenu = False
        app.mode = ""
    if event.key == "s":
        app.blade = "silver"
    if event.key == "p":
        app.blade = "pink"
    if event.key == "t":
        app.blade = "teal"

# sets variables based on mouse presses
def mousePressed(app, event):
    classicMousePressed(app, event)
    if app.onHomepage == True:
        app.mode = None
        app.gameStarted = False
        app.timerDelay = 100
        app.score = 0
        app.fruits = []
        app.bombs = []
        app.slices = []
        arcadeVariables(app)
        classicVariables(app)
        zenVariables(app)
    if app.gameStarted == True:
        gameStartedConditions(app, event)
        app.mousepress = None
        app.mouserelease = None
        if app.openZen == False or app.openClassic == False:
            app.mousepress = (event.x, event.y)
    else:
        if app.gameStarted == False:
            gameNotStartedConditions(app, event)

# removes classic level screen after mouse is pressed
def classicMousePressed(app, event):
    if app.showClassicLevel == True:
        app.showClassicLevel = False

# saves mouse release position 
def mouseReleased(app, event):
    if app.gameStarted == True and app.openZen == False:
        app.mouserelease = (event.x, event.y)

# sets the conditions when the game is started
def gameStartedConditions(app, event):
    if event.x >= 10 and event.x <= 200 and event.y >= 10 and event.y <= 80:
        app.onHomepage = True
        appStarted(app)
        app.mode = None
    if app.mode == "Arcade":
        app.openArcade = False
    if app.mode == "Zen":
        app.openZen = False
    if app.mode == "Classic":
        app.openClassic = False
        if app.showClassicLevel == True:
            app.showClassicLevel == False
    if app.mode != None:
        if event.x >= 10 and event.x <= 175 and event.y >= 10 and event.y <= 80:
            app.onHomepage = True
            app.mode = None
            app.gameStarted = False

# sets the conditions when the game is not started
def gameNotStartedConditions(app, event):
    if event.x >= 14 and event.x <= 237 and event.y >= 431 and event.y <= 651:
        app.mode = "Arcade"
        app.openArcade = True
        app.onHomepage = False
        app.openArcadeTime = time.time()
        app.gameStarted = True
    elif event.x >= 394 and event.x <= 604 and event.y >= 434 and event.y <= 649:
        app.mode = "Classic"
        app.openClassic = True
        app.openClassicTime = time.time()
        app.onHomepage = False
        app.gameStarted = True
    elif event.x >= 750 and event.x <= 980 and event.y >= 425 and event.y <= 646:
        app.mode = "Zen"
        app.onHomepage = False
        app.openZen = True
        app.gameStarted = True
    if app.inMenu == False: 
        if event.x >= 10 and event.x <= 175 and event.y >= 10 and event.y <= 80:
            app.inMenu = True
            app.onHomepage = False

runApp(width = 1000, height = 775)
