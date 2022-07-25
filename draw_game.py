# Catherine Mathews --> cmathews
import time

''' This file draws the entire game, including the backgrounds, buttons,
fruits, bombs, combos, blades, and slices. '''

''' MAIN BACKGROUND '''

# draws the homepage
def drawHomepage(app, canvas):
    if app.onHomepage == True:
        canvas.create_image(app.centerX - 10, app.centerY, image = app.menuBackground)

# draws the menu button on the homepage
def drawMenuButton(app, canvas):
    if app.inMenu == False:
        canvas.create_rectangle(10,10,175,80, fill = "black")
        canvas.create_text(90, 40, text = "MENU", font = app.menuFont1, fill = "silver")

# draws the game background
def drawBackground(app, canvas):
    if app.gameStarted == True or app.inMenu == True:
        canvas.create_image(app.centerX, app.centerY, image = app.gameBackground)
    
# draws the menu text
def drawMenuText(app, canvas):
    if app.inMenu == True:
        canvas.create_text(app.centerX, 90, text = "MENU", 
                           font = "Arial 40 bold", fill = "white", anchor = "n")
        canvas.create_text(100, 170, text = "Modes ", 
                           font = "Arial 30 bold", fill = "white", anchor = "n")
        canvas.create_text(100, 245, text = "Classic Mode: Slice all fruits appearing on the screen. Each missed fruit will result in a loss of a life.",
                           font = "Arial 14", fill = "white", anchor = "w")
        canvas.create_text(228, 270, text = "Levels of increasing difficulty will be introduced as the game is played", 
                           font = "Arial 14", fill = "white", anchor = "w")
        canvas.create_text(100, 325, text = "Zen Mode: Try to slice as many fruits as possible in 90 seconds. No bombs.",
                           font = "Arial 14", fill = "white", anchor = "w")
        canvas.create_text(100, 385, text = "Arcade Mode: Try to slice as many fruits as possible in 60 seconds without hitting any bombs.",
                           font = "Arial 14", fill = "white", anchor = "w")
        canvas.create_text(228, 410, text = "Bonus fruits are included. No bombs.", 
                           font = "Arial 14", fill = "white", anchor = "w")
        canvas.create_text(100, 430, text = "Other ", 
                           font = "Arial 30 bold", fill = "white", anchor = "n")
        canvas.create_text(100, 505, 
                           text = "Press h to return to homepage at anytime",
                           font = "Arial 14", anchor = "w", fill = "white")
        canvas.create_text(100, 540, 
                           text = "Press s to change blade color to silver",
                           font = "Arial 14", anchor = "w", fill = "white")
        canvas.create_text(100, 575, 
                           text = "Press t to change blade color to teal",
                           font = "Arial 14", anchor = "w", fill = "white")
        canvas.create_text(100, 610, 
                           text = "Press p to change blade color to pink",
                           font = "Arial 14", anchor = "w", fill = "white")

# draws the homepage button during the game
def drawHomepageButton(app, canvas):
    if app.gameStarted == True and app.onHomepage == False:
        canvas.create_rectangle(10,10,200,80, fill = "black")
        canvas.create_text(105, 40, text = "HOMEPAGE", font = app.menuFont2, fill = "silver")

''' FRUITS, BOMBS, SLICES DRAWING '''

# draws the fruits and bombs on the game 
def drawFruitsAndBombs(app, canvas):
    if app.onHomepage != True and app.arcadeGameOver == False and app.zenGameOver == False and app.classicGameOver == False:
        for fruit in app.fruits:
            canvas.create_oval(fruit.cx-fruit.r, fruit.cy-fruit.r,
                               fruit.cx+fruit.r, fruit.cy+fruit.r,
                               fill=fruit.col)
        for bomb in app.bombs:
            canvas.create_oval(bomb.cx - app.br, bomb.cy - app.br,
                               bomb.cx + app.br, bomb.cy + app.br,
                               fill = bomb.col)
        for sfruit in app.starfruits:
            canvas.create_oval(sfruit.cx - app.sr, sfruit.cy - app.sr,
                               sfruit.cx + app.sr, sfruit.cy + app.sr,
                               fill = sfruit.col, outline = "white",
                               width = 3)
        for cbomb in app.classicbombs:
            canvas.create_oval(cbomb.cx - cbomb.r, cbomb.cy - cbomb.r,
                               cbomb.cx + cbomb.r, cbomb.cy + cbomb.r,
                               fill = cbomb.col)
        for cfruit in app.combos:
            canvas.create_oval(cfruit.cx - cfruit.r, cfruit.cy - cfruit.r,
                               cfruit.cx + cfruit.r, cfruit.cy + cfruit.r,
                               fill = cfruit.col)

# draws the blade 
def drawBlade(app, canvas):
    if app.mousepress != None and app.mouserelease != None:
        canvas.create_line(app.mousepress[0], app.mousepress[1],
                           app.mouserelease[0], app.mouserelease[1],
                           fill = app.blade, width = 2)  

# draws the fruit slices 
def drawSlices(app, canvas):
    if app.onHomepage == False:
        for slices in app.slice1s:
            if slices.typ == "r":
                canvas.create_arc(slices.x0, slices.y0, slices.x1 - 3, slices.y1 - 3, style = "chord",
                                  start = slices.ang1, extent = slices.ang2, fill = slices.col)
            if slices.typ == "s":
                canvas.create_arc(slices.x0, slices.y0, slices.x1, slices.y1, style = "chord",
                                  start = slices.ang1, extent = slices.ang2, fill = slices.col,
                                  outline = "white", width = 3)
        for slices2 in app.slice2s:
            if slices2.typ == "r":
                canvas.create_arc(slices2.x0, slices2.y0, slices2.x1, slices2.y1, style = "chord",
                                  start = slices2.ang1, extent = slices2.ang2, fill = slices2.col)
            if slices2.typ == "s": 
                canvas.create_arc(slices2.x0, slices2.y0, slices2.x1, slices2.y1, style = "chord",
                                  start = slices2.ang1, extent = slices2.ang2, fill = slices2.col,
                                  outline = "white", width = 3)

''' CLASSIC MODE DRAWING '''

# draws classic mode of the game
def drawClassicMode(app, canvas):
    if app.mode == "Classic" and app.inMenu == False and app.onHomepage == False:
        if app.openClassic == True:
            canvas.create_rectangle(0, app.centerY - 50, app.width, app.centerY + 50, fill = "black")
            canvas.create_text(app.centerX, app.centerY - 15, text = f'Level: {app.level}',
                               font = "Arial 30 bold", fill = "white", anchor = "c")
            canvas.create_text(app.centerX, app.centerY + 25, text = "Press anywhere to begin",
                               font = "Arial 16 bold", fill = "white", anchor = "c")
        canvas.create_text(app.width - 10, 10, text = f"Score: {app.score}", 
                           anchor = "ne", font = "Arial 34 bold", fill = "white")
        canvas.create_text(app.width - 12, 60, text = f"Lives: {app.lives}",
                           anchor = "ne", font = "Arial 30 bold", fill = "white")
        if app.classicGameOver == True:
            canvas.create_rectangle(0, app.centerY - 50, app.width, app.centerY + 50, fill = "black")
            canvas.create_text(app.centerX, app.centerY, text = f"Game Over! Score: {app.score} ",
                               font = "Arial 30 bold", fill = "white", anchor = "c")
        if app.showClassicLevel == True:
            canvas.create_rectangle(0, app.centerY - 50, app.width, app.centerY + 50, fill = "black")
            canvas.create_text(app.centerX, app.centerY - 15, text = f'Level Up! Level: {app.level}',
                               font = "Arial 30 bold", fill = "white", anchor = "c")
            canvas.create_text(app.centerX, app.centerY + 25, text = "Press anywhere to continue playing",
                               font = "Arial 16 bold", fill = "white", anchor = "c")

''' ARCADE MODE DRAWING '''

# draws arcade mode of the game
def drawArcadeMode(app, canvas):
    if app.mode == "Arcade" and app.inMenu == False and app.onHomepage == False:
        if app.openArcade == True:
            canvas.create_rectangle(0, app.centerY - 50, app.width, app.centerY + 50, fill = "black")
            canvas.create_text(app.centerX, app.centerY - 15, text = "60 seconds!",
                               font = "Arial 30 bold", fill = "white", anchor = "c")
            canvas.create_text(app.centerX, app.centerY + 25, text = "Press anywhere to begin",
                               font = "Arial 16 bold", fill = "white", anchor = "c")
        if app.openArcade == False and app.arcadeGameOver == False:
            canvas.create_text(app.width - 10, 10, text = f"Time: {round((60 - (time.time() - app.openArcadeTime)))}s", 
                               anchor = "ne", font = "Arial 34 bold", fill = "white")
            canvas.create_text(app.centerX, 10, text = f"Score: {app.score}",
                               anchor = "n", font = "Arial 34 bold", fill = "white")
    if app.mode == "Arcade" and app.arcadeGameOver == True:
        canvas.create_rectangle(0, app.centerY - 50, app.width, app.centerY + 50, fill = "black")
        canvas.create_text(app.centerX, app.centerY, text = f"Game Over! Score: {app.score} ",
                           font = "Arial 30 bold", fill = "white", anchor = "c")

''' ZEN MODE DRAWING '''

# draws zen mode of the game
def drawZenMode(app, canvas):
    if app.mode == "Zen" and app.inMenu == False and app.onHomepage == False:
        if app.openZen == True:
            canvas.create_rectangle(0, app.centerY - 50, app.width, app.centerY + 50, fill = "black")
            canvas.create_text(app.centerX, app.centerY - 15, text = "90 seconds!",
                               font = "Arial 30 bold", fill = "white", anchor = "c")
            canvas.create_text(app.centerX, app.centerY + 25, text = "Press anywhere to begin",
                               font = "Arial 16 bold", fill = "white", anchor = "c")
        if app.openZen == False and app.zenGameOver == False:
            canvas.create_text(app.width - 10, 10, text = f"Time: {round((90 - (time.time() - app.openZenTime)))}s", 
                               anchor = "ne", font = "Arial 34 bold", fill = "white")
            canvas.create_text(app.centerX, 10, text = f"Score: {app.score}",
                               anchor = "n", font = "Arial 34 bold", fill = "white")
    if app.mode == "Zen" and app.zenGameOver == True:
            canvas.create_rectangle(0, app.centerY - 50, app.width, app.centerY + 50, fill = "black")
            canvas.create_text(app.centerX, app.centerY, text = f"Game Over! Score: {app.score} ",
                               font = "Arial 30 bold", fill = "white", anchor = "c")

# draws the fruit in zen mode
def drawZenFruit(app, canvas):
    if app.mode == "Zen" and app.openZen == False:
        canvas.create_oval(app.xPosition - app.r, app.yPosition - app.r,
                           app.xPosition + app.r, app.yPosition + app.r,
                           fill = app.color)

# calls all of the draw functions to draw the game
def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawHomepage(app, canvas)
    drawMenuButton(app, canvas)
    drawMenuText(app, canvas)
    drawHomepageButton(app, canvas)
    drawFruitsAndBombs(app, canvas)
    drawSlices(app, canvas)
    drawBlade(app, canvas)
    drawClassicMode(app, canvas)
    drawArcadeMode(app, canvas)
    drawZenMode(app, canvas)