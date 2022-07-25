# Catherine Mathews --> cmathews
import random
import time
import math
from dataclasses import make_dataclass

''' This file includes the specific timer fired function for each mode and also
randomly generates the characteristics of the fruits, bombs, combos, starfruits, 
and slices. '''

''' DATA CLASSES '''

Fruit = make_dataclass('Fruit', ['x0', 'y0', 'cx', 'cy', 'v', 'vx', 'vy', 'ax', 'ay', 'col', 'r'])
ClassicFruit = make_dataclass('ClassicFruit', ['x0', 'y0', 'cx', 'cy', 'v', 'vx', 'vy', 'ax', 'ay', 'col', 'r'])
Combo = make_dataclass('Combo', ['x0', 'y0', 'cx', 'cy', 'v', 'vx', 'vy', 'ax', 'ay', 'col', 'r'])
Bomb = make_dataclass('Bomb', ['x0', 'y0', 'cx', 'cy', 'v', 'vx', 'vy', 'ax', 'ay', 'col'])
ClassicBomb = make_dataclass('ClassicBomb', ['x0', 'y0', 'cx', 'cy', 'v', 'vx', 'vy', 'ax', 'ay', 'col', 'r'])
StarFruit = make_dataclass('StarFruit', ['x0', 'y0', 'cx', 'cy', 'v', 'vx', 'vy', 'ax', 'ay', 'col', 'r'])
Slice1 = make_dataclass('Slice1', ['inity0', 'inity1', 'x0', 'y0', 'x1', 'y1', 'v', 'vx', 'vy', 'ax', 'ay', 'col', 'ang1', 'ang2', 'typ', 'r'])
Slice2 = make_dataclass('Slice2', ['inity0', 'inity1','x0', 'y0', 'x1', 'y1', 'v', 'vx', 'vy', 'ax', 'ay', 'col', 'ang1','ang2', 'typ', 'r'])

''' TIMER FIRED '''

# timer fired for general game 
def timerFired(app):
    if app.onHomepage == True: 
        app.mode = ""
        app.zenGameOver = False
        app.mousepress = None
        app.mouserelease = None
        app.timecalls = 0
        app.fruits = []
        app.bombs = []
        app.starfruits = []
    if app.arcadeGameOver == True or app.zenGameOver == True or app.classicGameOver == True:
        app.mousepress = None
        app.mouserelease = None
        app.timecalls = 0
        app.fruits = []
        app.bombs = []
        app.starfruits = []
    classicTimerFired(app)
    zenTimerFired(app)
    arcadeTimerFired(app)

# timer fired for classic mode 
def classicTimerFired(app):
    if app.mode == "Classic":
        if app.level < 9:
            app.timerDelay = 100 - (10 * app.level)
        if app.level > 9:
            app.timerDelay -= (1/app.level)
        app.timecalls += 1
        if app.timecalls % 200 == 0 and app.timecalls != 0 and app.lives > 0 and app.timecalls > 200:
            app.level += 1
            app.fruits = []
            app.classicbombs = []
            app.openClassicTime = time.time()
            app.showClassicLevel = True
        if app.showClassicLevel == False:
            if app.timecalls % (25 - (app.level)) == 0:
                createFruit(app)
            if app.timecalls % (52 - (app.level * 1.25)) == 0 and app.timecalls != 0:
                createClassicBomb(app)
            if app.timecalls % (240 + (10 * (app.level - 1))) == 0 and app.level > 1:
                createFruitCombo(app)
            if app.classicGameOver == False and app.showClassicLevel == False:
                updateFruit(app)
                updateFruitCombo(app)
                updateBomb(app)
                createSlices(app)
                updateSlices(app)
            for fruit in app.fruits:
                if fruit.cy >= app.height and fruit.vy > 0:
                    app.fruits.remove(fruit)
                    app.lives -= 1
            if app.lives <= 0:
                app.classicGameOver = True
            if app.classicGameOver:
                app.fruits = []
                app.combos = []
                app.starfruits = []
                app.bombs = []

# timer fired for arcade mode 
def arcadeTimerFired(app):
    i = 0
    if app.openArcade == True and i == 0:
        app.openArcadeTime = time.time()
        app.openArcade == False
        i += 1
    if app.mode == "Arcade" and app.openArcade == False:
            app.timecalls += 1
            if (time.time() - app.openArcadeTime) > 60:
                app.arcadeGameOver = True
            else:
                if app.timecalls % app.fFreq == 0:
                    createFruit(app)
                if app.timecalls % 51 == 0:
                    createBomb(app)
                if app.timecalls % app.sfFreq == 0:
                    createStarFruit(app)
                if app.arcadeGameOver == False:
                    updateFruit(app)
                    updateBomb(app)
                    updateStarFruit(app)
                    createSlices(app)
                    updateSlices(app)
                if app.arcadeGameOver == True:
                    app.fruits = []
                    app.combos = []
                    app.starfruits = []
                    app.bombs = []

# timer fired for zen mode
def zenTimerFired(app):
    j = 0
    if app.openZen == True and j == 0:
        app.openZenTime = time.time()
        app.openZen == False
        j += 1
    if app.mode == "Zen" and app.openZen == False:
        app.timerDelay = random.randint(80, 100)
        app.timecalls += 1
        if (time.time() - app.openZenTime) > 90:
            app.zenGameOver = True
        else:
            if app.timecalls % app.fFreq == 0:
                createFruit(app)
            updateFruit(app)
            createSlices(app)
            updateSlices(app)
            if app.zenGameOver == True:
                app.fruits = []
                app.combos = []
                app.starfruits = []
                app.bombs = []

''' FRUIT/BOMB/SLICES CREATION '''

# generates fruits in each mode
def createFruit(app):
    radOptions = [12,14,16,18,20,22,24,26]
    if app.mode != "Classic":
        r = random.choice(radOptions)
        v = 50 - (r - 12)
        vx = v / 30 
        x0 = random.randint(50, 700) 
    elif app.mode == "Classic": 
        r = random.choice(radOptions)
        v = 50 - (r - 12)
        vx = v / (30 + (2 * (app.level - 1)))
        if len(app.fruits) >= 1:
            avg = averageXPos(app)
            if (avg - (app.level * 100) >= 0) and (avg + (app.level * 100) <= app.width): 
                try:
                    x0 = random.randrange((avg - (app.level * 100)), (avg + (app.level * 100)))
                except:
                    x0 = random.randrange(0, app.width - r)
            else:
                x0 = random.randrange(0, app.width - r)
        else:
             x0 = random.randrange(0, app.width - r)
    vy = -v 
    ax = 0 
    ay = 2
    y0 = app.height
    col = random.choice(["red", "orange", "yellow", "green", "blue", "purple"])
    newFruit = Fruit(x0=x0, y0=y0, cx=x0, cy=y0, v=v, vx=vx, vy=vy, ax=ax, ay=ay, col=col, r=r)
    app.fruits.append(newFruit)

# calculates the average x position of the fruits 
def averageXPos(app):
    res = []
    for fruit in app.fruits:
        res.append(fruit.cx)
    s = sum(res)
    l = len(app.fruits)
    return (s / l)

# generates starfruits for arcade mode 
def createStarFruit(app):
    v = 45
    ang = 80
    vx = v / 20 
    vy = -v 
    ax = 0 
    ay = 2
    x0 = random.randint(100, 650) 
    y0 = app.height
    col = random.choice(["lightgreen", "lightpink"])
    newFruit = StarFruit(x0=x0, y0=y0, cx=x0, cy=y0, v=v, vx=vx, vy=vy, ax=ax, ay=ay, col=col, r=app.sr)
    app.starfruits.append(newFruit)

# generates fruit combos in classic mode 
def createFruitCombo(app):
    v = random.randrange(35 + (2 * (app.level - 1)), 50 + (2 * (app.level - 1)))
    vx = v / (30 + (2 * (app.level - 1)))
    vy = -v
    ax = 0 
    ay = 2
    x0 = random.randint(50, 700)
    r = random.choice([20, 22, 24, 26])
    y0 = app.height + (2 * r)
    col1, col2, col3, col4, col5 = ("red", "orange", "yellow", "green", "blue")
    newFruit1 = Combo(x0=x0 - (4 * r), y0=y0, cx=x0  - (4 * r), cy=y0, v=v, vx=vx, vy=vy, ax=ax, ay=ay, col=col1, r=r)
    app.combos.append(newFruit1)
    newFruit2 = Combo(x0=x0 - (2 * r), y0=y0, cx=x0 - (2 * r), cy=y0 - r, v=v, vx=vx, vy=vy, ax=ax, ay=ay, col=col2, r=r)
    app.combos.append(newFruit2)
    newFruit3 = Combo(x0=x0, y0=y0, cx=x0, cy=y0 - (2 * r), v=v, vx=vx, vy=vy, ax=ax, ay=ay, col=col3, r=r)
    app.combos.append(newFruit3)
    newFruit4 = Combo(x0=x0 + (2 * r), y0=y0, cx=x0 + (2 * r), cy=y0 - (3 * r), v=v, vx=vx, vy=vy, ax=ax, ay=ay, col=col4, r=r)
    app.combos.append(newFruit4)
    newFruit5 = Combo(x0=x0 + (4 * r), y0=y0, cx=x0 + (4 * r), cy=y0 - (4 * r), v=v, vx=vx, vy=vy, ax=ax, ay=ay, col=col5, r=r)
    app.combos.append(newFruit5)

# generates bombs for zen and arcade modes 
def createBomb(app):
    v = app.br - 5
    vx = v / 30 
    vy = -v 
    ax = 0 
    ay = 2
    x0 = random.randint(100, 650)
    y0 = app.height
    col = "black"
    newBomb = Bomb(x0=x0, y0=y0, cx=x0, cy=y0, v=v, vx=vx, vy=vy, ax=ax, ay=ay, col=col)
    app.bombs.append(newBomb)

# creates bombs in classic mode based on current level 
def createClassicBomb(app):
    a = len(app.fruits)
    if a == 0:
        v = random.choice([35, 40, 45, 50])
        r = 30 - (3 * app.level)
        ang = 80
        vx = v / 30 
        vy = -v 
        ax = 0 
        ay = 2
        x0 = random.randint(100, 650)
        y0 = app.height
        col = "black"
        newBomb = ClassicBomb(x0=x0, y0=y0, cx=x0, cy=y0, v=v, vx=vx, vy=vy, ax=ax, ay=ay, col=col, r=r)
        app.classicbombs.append(newBomb)
    else:
        if len(app.fruits) > 1:
            d = list(range(len(app.fruits)))
            b = random.choice(d)
        elif len(app.fruits) == 1:
            b = 0
        c = app.fruits[b].cx
        if (30 + (2 * app.level)) <= 50:
            v = random.randrange(30, 30 + (2 * app.level))
        r = 30 - (3 * app.level)
        ang = 80
        vx = v / 30 
        vy = -v 
        ax = 0 
        ay = 2
        rng = app.width - 50 - c
        left = (c - (c // app.level))
        right = (c + (rng // app.level))
        if left < app.br:
            left += app.br
        if right > app.height - app.br:
            right -= app.br
        xrng = list(range(int(left), int(right - 1)))
        x0 = random.choice(xrng)
        y0 = app.height
        col = "black"
        newBomb = ClassicBomb(x0=x0, y0=y0, cx=x0, cy=y0, v=v, vx=vx, vy=vy, ax=ax, ay=ay, col=col, r=r)
        app.classicbombs.append(newBomb)

# creates fruit slices when slid through with mouse
def createSlices(app):
    if app.mousepress != None and app.mouserelease != None and app.onHomepage == False:
        x0 = app.mousepress[0]
        x1 = app.mouserelease[0]
        y0 = app.mousepress[1]
        y1 = app.mouserelease[1]
        dy = y1 - y0
        dx = x1 - x0
        endGame(app, x0, x1, y0, y1, dx, dy)
        createFruitSlices(app, x0, x1, y0, y1, dx, dy)
        createStarFruitSlices(app, x0, x1, y0, y1, dx, dy)
        createComboSlices(app, x0, x1, y0, y1, dx, dy)

def endGame(app, x0, x1, y0, y1, dx, dy):
    for bomb in app.bombs:
        if (x0 <= bomb.cx <= x1 and y1 <= bomb.cy <= y0) or (x0 <= bomb.cx <= x1 and y0 <= bomb.cy <= y1) or (bomb.cx - app.br <= x0 <= bomb.cx + app.br and y0 <= bomb.cx <= y1):
            app.arcadeGameOver = True
            app.classicGameOver = True
            app.zenGameOver = True
    for bomb in app.classicbombs: 
        if (x0 <= bomb.cx <= x1 and y1 <= bomb.cy <= y0) or (x0 <= bomb.cx <= x1 and y0 <= bomb.cy <= y1) or (bomb.cx - app.br <= x0 <= bomb.cx + app.br and y0 <= bomb.cx <= y1):
            app.arcadeGameOver = True
            app.classicGameOver = True
            app.zenGameOver = True

def createFruitSlices(app, x0, x1, y0, y1, dx, dy):
    for fruit in app.fruits:
        if (x0 <= fruit.cx <= x1 and y1 <= fruit.cy <= y0) or (x0 <= fruit.cx <= x1 and y0 <= fruit.cy <= y1) or (fruit.cx - app.r <= x0 <= fruit.cx + app.r and y0 <= fruit.cx <= y1):
            if ((x0 < x1) and (y1 < y0)):                
                res = intersectionCircleLine(app, fruit.cx, fruit.cy)
                if res != None:
                    app.fruits.remove(fruit)
                    app.score += 5
                    xPos1 = res[0][0]
                    yPos1 = res[0][1]
                    xPos2 = res[1][0]
                    yPos2 = res[1][1]
                    dist = math.sqrt((yPos2 - yPos1)**2 + (xPos2 - xPos1)**2)
                    # bottom left to top right with intersection along midline & bottom left to top right with both points above midline
                    if (yPos2 < fruit.cy and yPos1 > fruit.cy) or (yPos2 < fruit.cy and yPos1 < fruit.cy):
                        ang1 = abs(math.degrees(math.atan((fruit.cy-y1) / (x1-fruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # bottom left to top right with intersections under midline
                    elif (yPos1 > fruit.cy and yPos2 > fruit.cy):
                        ang1 =  - abs(math.degrees(math.atan((fruit.cy-y1) / (x1-fruit.cx))))
                        angdiff = 360 - (math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2)))) - abs(ang1))
                if res == None:
                    continue
            elif (x1 > x0) and (y1 > y0):
                res = intersectionCircleLine(app, fruit.cx, fruit.cy)
                if dx != 0:
                    ang = - math.degrees(math.atan(dy/dx))
                    ang1 = - math.degrees(math.atan(y1 - fruit.cy / x1 - fruit.cx))
                if res != None:
                    app.fruits.remove(fruit)
                    app.score += 5
                    xPos1 = res[0][0]
                    yPos1 = res[0][1]
                    xPos2 = res[1][0]
                    yPos2 = res[1][1]
                    dist = math.sqrt((yPos2 - yPos1)**2 + (xPos2 - xPos1)**2)
                    # top left to bottom right with points above and below midline
                    if (yPos2 > fruit.cy and yPos1 < fruit.cy): 
                        ang1 = - abs(math.degrees(math.atan((fruit.cy-y1) / (x1-fruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2)))) + abs(ang1)
                    # top left to bottom right with intersection above the midline
                    elif (yPos2 < fruit.cy and yPos1 < fruit.cy):
                        ang1 = abs(math.degrees(math.atan((fruit.cy-y1) / (x1-fruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # top left to bottom right with intersections under midline
                    elif yPos1 > fruit.cy and yPos2 > fruit.cy:
                        ang1 = - abs(math.degrees(math.atan((fruit.cy-y1) / (x1-fruit.cx))))
                        angdiff = 360 - math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                if res == None:
                    continue
            newSlice1 = Slice1(inity0=yPos1, inity1=yPos2,x0=fruit.cx-fruit.r, y0=fruit.cy-fruit.r, x1=fruit.cx + fruit.r, y1=fruit.cy+fruit.r, v=0, vx=0, vy= 0, ax=0, ay=-2, col=fruit.col, ang1 = ang1, ang2=ang1 + angdiff, typ="r", r=fruit.r)
            newSlice2 = Slice2(inity0=yPos1, inity1=yPos2,x0=fruit.cx-fruit.r, y0=fruit.cy-fruit.r, x1=fruit.cx + fruit.r, y1=fruit.cy+fruit.r, v=0, vx=0, vy= 0, ax=0, ay=-2, col=fruit.col, ang1 = ang1, ang2= - (360- (angdiff + ang1)), typ="r", r=fruit.r)
            app.slice1s.append(newSlice1)
            app.slice2s.append(newSlice2)
            app.mousepress = None
            app.mouserelease = None
        elif (x1 <= fruit.cx <= x0 and y1 <= fruit.cy <= y0) or (x1 <= fruit.cx <= x0 and y0 <= fruit.cy <= y1): 
            if (x1 < x0) and (y1 > y0):
                ang1 = - math.degrees(math.atan(y0 - fruit.cy / x0 - fruit.cx))
                res = intersectionCircleLine(app, fruit.cx, fruit.cy)
                if res != None:
                    app.fruits.remove(fruit)
                    app.score += 5
                    xPos1 = res[0][0]
                    yPos1 = res[0][1]
                    xPos2 = res[1][0]
                    yPos2 = res[1][1] 
                    dist = math.sqrt((yPos2 - yPos1)**2 + (xPos2 - xPos1)**2)
                    # top right to bottom left with intersections above midline 
                    if (yPos2 < fruit.cy and yPos1 < fruit.cy):
                        ang1 = abs(math.degrees(math.atan((fruit.cy-y0) / (x0-fruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # top right to bottom left with intersections above and below the midline
                    if (yPos2 < fruit.cy and yPos1 > fruit.cy):
                        ang1 = abs(math.degrees(math.atan((fruit.cy-y0) / (x0-fruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # top right to bottom left with intersections under midline
                    elif (yPos2 > fruit.cy and yPos1 > fruit.cy):
                        ang1 =  - abs(math.degrees(math.atan((fruit.cy-y0) / (x0-fruit.cx))))
                        angdiff = 360 - (math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2)))) + abs(ang1))
                elif res == None:
                    continue
            elif (x1 < x0) and (y1 < y0):
                ang1 = - math.degrees(math.atan(y0 - fruit.cy / x0 - fruit.cx))
                res = intersectionCircleLine(app, fruit.cx, fruit.cy)
                if res != None:
                    app.fruits.remove(fruit)
                    app.score += 5
                    xPos1 = res[0][0]
                    yPos1 = res[0][1]
                    xPos2 = res[1][0]
                    yPos2 = res[1][1]
                    dist = math.sqrt((yPos2 - yPos1)**2 + (xPos2 - xPos1)**2)
                    # bottom right to top left with both points above midline
                    if (yPos2 < fruit.cy and yPos1 < fruit.cy): 
                        ang1 = abs(math.degrees(math.atan((fruit.cy-y1) / (x1-fruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # bottom right to top left with intersections below the midline
                    elif (yPos2 > fruit.cy and yPos1 > fruit.cy):
                        ang1 =  - abs(math.degrees(math.atan((fruit.cy-y0) / (x0-fruit.cx))))
                        angdiff = 360 - (math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2)))) + abs(ang1))
                    # bottom right to top left with intersections along the midline
                    elif yPos1 < fruit.cy and yPos2 > fruit.cy:
                        ang1 = - abs(math.degrees(math.atan((fruit.cy-y1) / (x1-fruit.cx))))
                        angdiff = 360 - math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                elif res == None:
                    continue
            elif (x1 < x0) and (y0 == y1):
                if dx != 0:
                    ang = - math.degrees(math.atan(dy/dx))
                    ang1 = - math.degrees(math.atan(y1 - fruit.cx / x1 - fruit.cx))
                    ang2 = - math.degrees(math.atan(fruit.cy - y0 / fruit.cx - x0))
                res = intersectionCircleLine(app, fruit.cx, fruit.cy)
                if res != None:
                    app.fruits.remove(fruit)
                    app.score += 5
                    xPos1 = res[1][0]
                    yPos1 = res[1][1]
                    xPos2 = res[0][0]
                    yPos2 = res[0][1]
                if res == None:
                    continue
            elif (x0 == x1) and (y0 < y1):
                if dx != 0:
                    ang = - math.degrees(math.atan(dy/dx))
                res = intersectionCircleLine(app, fruit.cx, fruit.cy)
                if res != None:
                    app.fruits.remove(fruit)
                    app.score += 5
                    xPos1 = res[1][0]
                    yPos1 = res[1][1]
                    xPos2 = res[0][0]
                    yPos2 = res[0][1]
                if res == None:
                    continue
            newSlice1 = Slice1(inity0=yPos1, inity1=yPos2,x0=fruit.cx-fruit.r, y0=fruit.cy-fruit.r, x1=fruit.cx + fruit.r, y1=fruit.cy+fruit.r, v=0, vx=0, vy= 0, ax=0, ay=-2, col=fruit.col, ang1 = ang1, ang2=ang1 + angdiff, typ="r", r=fruit.r)
            newSlice2 = Slice2(inity0=yPos1, inity1=yPos2,x0=fruit.cx-fruit.r, y0=fruit.cy-fruit.r, x1=fruit.cx + fruit.r, y1=fruit.cy+fruit.r, v=0, vx=0, vy= 0, ax=0, ay=-2, col=fruit.col, ang1 = ang1, ang2= - (360- (angdiff + ang1)), typ="r", r=fruit.r)
            app.slice1s.append(newSlice1)
            app.slice2s.append(newSlice2)
            app.mousepress = None
            app.mouserelease = None

def createStarFruitSlices(app, x0, x1, y0, y1, dx, dy):
    for sfruit in app.starfruits:
        if (x0 <= sfruit.cx <= x1 and y1 <= sfruit.cy <= y0) or (x0 <= sfruit.cx <= x1 and y0 <= sfruit.cy <= y1):
            if ((x0 < x1) and (y1 < y0)):                
                res = intersectionCircleLine(app, sfruit.cx, sfruit.cy)
                if res != None:
                    app.starfruits.remove(sfruit)
                    app.score += 10
                    xPos1 = res[0][0]
                    yPos1 = res[0][1]
                    xPos2 = res[1][0]
                    yPos2 = res[1][1]
                    dist = math.sqrt((yPos2 - yPos1)**2 + (xPos2 - xPos1)**2)
                    # bottom left to top right with intersection along midline & bottom left to top right with both points above midline
                    if (yPos2 < sfruit.cy and yPos1 > sfruit.cy) or (yPos2 < sfruit.cy and yPos1 < sfruit.cy):
                        ang1 = abs(math.degrees(math.atan((sfruit.cy-y1) / (x1-sfruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # bottom left to top right with intersections under midline
                    elif (yPos1 > sfruit.cy and yPos2 > sfruit.cy):
                        ang1 =  - abs(math.degrees(math.atan((sfruit.cy-y1) / (x1-sfruit.cx))))
                        angdiff = 360 - (math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2)))) - abs(ang1))
                if res == None:
                    continue
            elif (x1 > x0) and (y1 > y0):
                res = intersectionCircleLine(app, sfruit.cx, sfruit.cy)
                if dx != 0:
                    ang = - math.degrees(math.atan(dy/dx))
                    ang1 = - math.degrees(math.atan(y1 - fruit.cy / x1 - fruit.cx))
                if res != None:
                    app.starfruits.remove(sfruit)
                    app.score += 10
                    xPos1 = res[0][0]
                    yPos1 = res[0][1]
                    xPos2 = res[1][0]
                    yPos2 = res[1][1]
                    dist = math.sqrt((yPos2 - yPos1)**2 + (xPos2 - xPos1)**2)
                    # top left to bottom right with points above and below midline
                    if (yPos2 > sfruit.cy and yPos1 < sfruit.cy): 
                        ang1 = - abs(math.degrees(math.atan((fruit.cy-y1) / (x1-fruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2)))) + abs(ang1)
                    # top left to bottom right with intersection above the midline
                    elif (yPos2 < sfruit.cy and yPos1 < sfruit.cy):
                        ang1 = abs(math.degrees(math.atan((sfruit.cy-y1) / (x1-sfruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # top left to bottom right with intersections under midline
                    elif yPos1 > fruit.cy and yPos2 > fruit.cy:
                        ang1 = - abs(math.degrees(math.atan((sfruit.cy-y1) / (x1-sfruit.cx))))
                        angdiff = 360 - math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                if res == None:
                    continue
            newSlice1 = Slice1(inity0=yPos1, inity1=yPos2,x0=sfruit.cx-sfruit.r, y0=sfruit.cy-sfruit.r, x1=sfruit.cx + sfruit.r, y1=sfruit.cy+sfruit.r, v=0, vx=0, vy= 0, ax=0, ay=-2, col=sfruit.col, ang1 = ang1, ang2=ang1 + angdiff, typ="s", r=sfruit.r)
            newSlice2 = Slice2(inity0=yPos1, inity1=yPos2,x0=sfruit.cx-sfruit.r, y0=sfruit.cy-sfruit.r, x1=sfruit.cx + sfruit.r, y1=sfruit.cy+sfruit.r, v=0, vx=0, vy= 0, ax=0, ay=-2, col=sfruit.col, ang1 = ang1, ang2= - (360- (angdiff + ang1)), typ="s", r=sfruit.r)
            app.slice1s.append(newSlice1)
            app.slice2s.append(newSlice2)
            app.mousepress = None
            app.mouserelease = None
        elif (x1 <= sfruit.cx <= x0 and y1 <= sfruit.cy <= y0) or (x1 <= sfruit.cx <= x0 and y0 <= sfruit.cy <= y1): 
            if (x1 < x0) and (y1 > y0):
                ang1 = - math.degrees(math.atan(y0 - sfruit.cy / x0 - sfruit.cx))
                res = intersectionCircleLine(app, sfruit.cx, sfruit.cy)
                if res != None:
                    app.starfruits.remove(sfruit)
                    app.score += 10
                    xPos1 = res[0][0]
                    yPos1 = res[0][1]
                    xPos2 = res[1][0]
                    yPos2 = res[1][1] 
                    dist = math.sqrt((yPos2 - yPos1)**2 + (xPos2 - xPos1)**2)
                    # top right to bottom left with intersections above midline 
                    if (yPos2 < sfruit.cy and yPos1 < sfruit.cy):
                        ang1 = abs(math.degrees(math.atan((sfruit.cy-y0) / (x0-sfruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # top right to bottom left with intersections above and below the midline
                    if (yPos2 < sfruit.cy and yPos1 > sfruit.cy):
                        ang1 = abs(math.degrees(math.atan((sfruit.cy-y0) / (x0-sfruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # top right to bottom left with intersections under midline
                    elif (yPos2 > sfruit.cy and yPos1 > sfruit.cy):
                        ang1 =  - abs(math.degrees(math.atan((sfruit.cy-y0) / (x0-sfruit.cx))))
                        angdiff = 360 - (math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2)))) + abs(ang1))
                elif res == None:
                    continue
            elif (x1 < x0) and (y1 < y0):
                ang1 = - math.degrees(math.atan(y0 - sfruit.cy / x0 - sfruit.cx))
                res = intersectionCircleLine(app, sfruit.cx, sfruit.cy)
                if res != None:
                    app.starfruits.remove(sfruit)
                    app.score += 10
                    xPos1 = res[0][0]
                    yPos1 = res[0][1]
                    xPos2 = res[1][0]
                    yPos2 = res[1][1]
                    dist = math.sqrt((yPos2 - yPos1)**2 + (xPos2 - xPos1)**2)
                    # bottom right to top left with both points above midline
                    if (yPos2 < sfruit.cy and yPos1 < sfruit.cy): 
                        ang1 = abs(math.degrees(math.atan((sfruit.cy-y1) / (x1-sfruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # bottom right to top left with intersections below the midline
                    elif (yPos2 > sfruit.cy and yPos1 > sfruit.cy):
                        ang1 =  - abs(math.degrees(math.atan((sfruit.cy-y0) / (x0-sfruit.cx))))
                        angdiff = 360 - (math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2)))) + abs(ang1))
                    # bottom right to top left with intersections along the midline
                    elif yPos1 < sfruit.cy and yPos2 > sfruit.cy:
                        ang1 = - abs(math.degrees(math.atan((sfruit.cy-y1) / (x1-sfruit.cx))))
                        angdiff = 360 - math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                elif res == None:
                    continue
            elif (x1 < x0) and (y0 == y1):
                if dx != 0:
                    ang = - math.degrees(math.atan(dy/dx))
                    ang1 = - math.degrees(math.atan(y1 - sfruit.cx / x1 - sfruit.cx))
                    ang2 = - math.degrees(math.atan(sfruit.cy - y0 / sfruit.cx - x0))
                res = intersectionCircleLine(app, sfruit.cx, sfruit.cy)
                if res != None:
                    app.starfruits.remove(fruit)
                    app.score += 10
                    xPos1 = res[1][0]
                    yPos1 = res[1][1]
                    xPos2 = res[0][0]
                    yPos2 = res[0][1]
                if res == None:
                    continue
            elif (x0 == x1) and (y0 < y1):
                if dx != 0:
                    ang = - math.degrees(math.atan(dy/dx))
                res = intersectionCircleLine(app, sfruit.cx, sfruit.cy)
                if res != None:
                    app.starfruits.remove(sfruit)
                    app.score += 10
                    xPos1 = res[1][0]
                    yPos1 = res[1][1]
                    xPos2 = res[0][0]
                    yPos2 = res[0][1]
                if res == None:
                    continue
            newSlice1 = Slice1(inity0=yPos1, inity1=yPos2,x0=sfruit.cx-sfruit.r, y0=sfruit.cy-fruit.r, x1=sfruit.cx + sfruit.r, y1=sfruit.cy+sfruit.r, v=0, vx=0, vy= 0, ax=0, ay=-2, col=sfruit.col, ang1 = ang1, ang2=ang1 + angdiff, typ="s", r=sfruit.r)
            newSlice2 = Slice2(inity0=yPos1, inity1=yPos2,x0=sfruit.cx-sfruit.r, y0=sfruit.cy-fruit.r, x1=sfruit.cx + sfruit.r, y1=sfruit.cy+sfruit.r, v=0, vx=0, vy= 0, ax=0, ay=-2, col=sfruit.col, ang1 = ang1, ang2= - (360- (angdiff + ang1)), typ="s", r=sfruit.r)
            app.slice1s.append(newSlice1)
            app.slice2s.append(newSlice2)
            app.mousepress = None
            app.mouserelease = None

def createComboSlices(app, x0, x1, y0, y1, dx, dy): 
    for cfruit in app.combos:
        if (x0 <= cfruit.cx <= x1 and y1 <= cfruit.cy <= y0) or (x0 <= cfruit.cx <= x1 and y0 <= cfruit.cy <= y1):
            if ((x0 < x1) and (y1 < y0)):                
                res = intersectionCircleLine(app, cfruit.cx, cfruit.cy)
                if res != None:
                    app.combos.remove(cfruit)
                    app.score += 5
                    xPos1 = res[0][0]
                    yPos1 = res[0][1]
                    xPos2 = res[1][0]
                    yPos2 = res[1][1]
                    dist = math.sqrt((yPos2 - yPos1)**2 + (xPos2 - xPos1)**2)
                    # bottom left to top right with intersection along midline & bottom left to top right with both points above midline
                    if (yPos2 < cfruit.cy and yPos1 > cfruit.cy) or (yPos2 < cfruit.cy and yPos1 < cfruit.cy):
                        ang1 = abs(math.degrees(math.atan((cfruit.cy-y1) / (x1-cfruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # bottom left to top right with intersections under midline
                    elif (yPos1 > cfruit.cy and yPos2 > cfruit.cy):
                        ang1 =  - abs(math.degrees(math.atan((cfruit.cy-y1) / (x1-cfruit.cx))))
                        angdiff = 360 - (math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2)))) - abs(ang1))
                if res == None:
                    continue
            elif (x1 > x0) and (y1 > y0):
                res = intersectionCircleLine(app, cfruit.cx, cfruit.cy)
                if dx != 0:
                    ang = - math.degrees(math.atan(dy/dx))
                    ang1 = - math.degrees(math.atan(y1 - cfruit.cy / x1 - cfruit.cx))
                if res != None:
                    app.combos.remove(cfruit)
                    app.score += 5
                    xPos1 = res[0][0]
                    yPos1 = res[0][1]
                    xPos2 = res[1][0]
                    yPos2 = res[1][1]
                    dist = math.sqrt((yPos2 - yPos1)**2 + (xPos2 - xPos1)**2)
                    # top left to bottom right with points above and below midline
                    if (yPos2 > cfruit.cy and yPos1 < cfruit.cy): 
                        ang1 = - abs(math.degrees(math.atan((cfruit.cy-y1) / (x1-cfruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2)))) + abs(ang1)
                    # top left to bottom right with intersection above the midline
                    elif (yPos2 < cfruit.cy and yPos1 < cfruit.cy):
                        ang1 = abs(math.degrees(math.atan((cfruit.cy-y1) / (x1-cfruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # top left to bottom right with intersections under midline
                    elif yPos1 > cfruit.cy and yPos2 > cfruit.cy:
                        ang1 = - abs(math.degrees(math.atan((cfruit.cy-y1) / (x1-cfruit.cx))))
                        angdiff = 360 - math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                if res == None:
                    continue
            newSlice1 = Slice1(inity0=yPos1, inity1=yPos2,x0=cfruit.cx-cfruit.r, y0=cfruit.cy-cfruit.r, x1=cfruit.cx + cfruit.r, y1=cfruit.cy+cfruit.r, v=0, vx=0, vy= 0, ax=0, ay=-2, col=cfruit.col, ang1 = ang1, ang2=ang1 + angdiff, typ="r", r=cfruit.r)
            newSlice2 = Slice2(inity0=yPos1, inity1=yPos2,x0=cfruit.cx-cfruit.r, y0=cfruit.cy-cfruit.r, x1=cfruit.cx + cfruit.r, y1=cfruit.cy+cfruit.r, v=0, vx=0, vy= 0, ax=0, ay=-2, col=cfruit.col, ang1 = ang1, ang2= - (360- (angdiff + ang1)), typ="r", r=cfruit.r)
            app.slice1s.append(newSlice1)
            app.slice2s.append(newSlice2)
        elif (x1 <= cfruit.cx <= x0 and y1 <= cfruit.cy <= y0) or (x1 <= cfruit.cx <= x0 and y0 <= cfruit.cy <= y1): 
            app.score += 5
            if (x1 < x0) and (y1 > y0):
                ang1 = - math.degrees(math.atan(y0 - cfruit.cy / x0 - cfruit.cx))
                res = intersectionCircleLine(app, cfruit.cx, cfruit.cy)
                if res != None:
                    app.combos.remove(cfruit)
                    app.score += 5
                    xPos1 = res[0][0]
                    yPos1 = res[0][1]
                    xPos2 = res[1][0]
                    yPos2 = res[1][1] 
                    dist = math.sqrt((yPos2 - yPos1)**2 + (xPos2 - xPos1)**2)
                    # top right to bottom left with intersections above midline 
                    if (yPos2 < cfruit.cy and yPos1 < cfruit.cy):
                        ang1 = abs(math.degrees(math.atan((cfruit.cy-y0) / (x0-cfruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # top right to bottom left with intersections above and below the midline
                    if (yPos2 < cfruit.cy and yPos1 > cfruit.cy):
                        ang1 = abs(math.degrees(math.atan((cfruit.cy-y0) / (x0-cfruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # top right to bottom left with intersections under midline
                    elif (yPos2 > cfruit.cy and yPos1 > cfruit.cy):
                        ang1 =  - abs(math.degrees(math.atan((cfruit.cy-y0) / (x0-cfruit.cx))))
                        angdiff = 360 - (math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2)))) + abs(ang1))
                elif res == None:
                    continue
            elif (x1 < x0) and (y1 < y0):
                ang1 = - math.degrees(math.atan(y0 - cfruit.cy / x0 - cfruit.cx))
                res = intersectionCircleLine(app, cfruit.cx, cfruit.cy)
                if res != None:
                    app.combos.remove(cfruit)
                    app.score += 5
                    xPos1 = res[0][0]
                    yPos1 = res[0][1]
                    xPos2 = res[1][0]
                    yPos2 = res[1][1]
                    dist = math.sqrt((yPos2 - yPos1)**2 + (xPos2 - xPos1)**2)
                    # bottom right to top left with both points above midline
                    if (yPos2 < cfruit.cy and yPos1 < cfruit.cy): 
                        ang1 = abs(math.degrees(math.atan((cfruit.cy-y1) / (x1-cfruit.cx))))
                        angdiff = math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                    # bottom right to top left with intersections below the midline
                    elif (yPos2 > cfruit.cy and yPos1 > cfruit.cy):
                        ang1 =  - abs(math.degrees(math.atan((cfruit.cy-y0) / (x0-cfruit.cx))))
                        angdiff = 360 - (math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2)))) + abs(ang1))
                    # bottom right to top left with intersections along the midline
                    elif yPos1 < cfruit.cy and yPos2 > cfruit.cy:
                        ang1 = - abs(math.degrees(math.atan((cfruit.cy-y1) / (x1-cfruit.cx))))
                        angdiff = 360 - math.degrees(math.acos((dist**2 - (2*(app.r**2))) / (-2 * (app.r**2))))
                elif res == None:
                    continue
            elif (x1 < x0) and (y0 == y1):
                if dx != 0:
                    ang = - math.degrees(math.atan(dy/dx))
                    ang1 = - math.degrees(math.atan(y1 - cfruit.cx / x1 - cfruit.cx))
                    ang2 = - math.degrees(math.atan(cfruit.cy - y0 / cfruit.cx - x0))
                res = intersectionCircleLine(app, cfruit.cx, cfruit.cy)
                if res != None:
                    app.combos.remove(cfruit)
                    app.score += 5
                    xPos1 = res[1][0]
                    yPos1 = res[1][1]
                    xPos2 = res[0][0]
                    yPos2 = res[0][1]
                if res == None:
                    continue
            elif (x0 == x1) and (y0 < y1):
                if dx != 0:
                    ang = - math.degrees(math.atan(dy/dx))
                res = intersectionCircleLine(app, cfruit.cx, cfruit.cy)
                if res != None:
                    app.combos.remove(cfruit)
                    app.score += 5
                    xPos1 = res[1][0]
                    yPos1 = res[1][1]
                    xPos2 = res[0][0]
                    yPos2 = res[0][1]
                if res == None:
                    continue
            newSlice1 = Slice1(inity0=yPos1, inity1=yPos2,x0=cfruit.cx-cfruit.r, y0=cfruit.cy-cfruit.r, x1=cfruit.cx + cfruit.r, y1=cfruit.cy+cfruit.r, v=0, vx=0, vy= 0, ax=0, ay=-2, col=cfruit.col, ang1 = ang1, ang2=ang1 + angdiff, typ="r", r=cfruit.r)
            newSlice2 = Slice2(inity0=yPos1, inity1=yPos2,x0=cfruit.cx-cfruit.r, y0=cfruit.cy-cfruit.r, x1=cfruit.cx + cfruit.r, y1=cfruit.cy+cfruit.r, v=0, vx=0, vy= 0, ax=0, ay=-2, col=cfruit.col, ang1 = ang1, ang2= - (360- (angdiff + ang1)), typ="r", r=cfruit.r)
            app.slice1s.append(newSlice1)
            app.slice2s.append(newSlice2)


''' UPDATE FRUIT/BOMBS/SLICES '''

# updates fruit position
def updateFruit(app):
    for fruit in app.fruits:
        fruit.cx = fruit.cx + fruit.vx
        fruit.vy = fruit.vy + fruit.ay
        fruit.cy = fruit.cy + fruit.vy

# updates bomb position  
def updateBomb(app):
    if app.mode != "Classic":
        for bomb in app.bombs:
            bomb.cx = bomb.cx + bomb.vx
            bomb.vy = bomb.vy + bomb.ay
            bomb.cy = bomb.cy + bomb.vy
    elif app.mode == "Classic":
        for cbomb in app.classicbombs:
            cbomb.cx = cbomb.cx + cbomb.vx
            cbomb.vy = cbomb.vy + cbomb.ay
            cbomb.cy = cbomb.cy + cbomb.vy

# updates fruit combo position
def updateFruitCombo(app):
    for cfruit in app.combos:
        cfruit.cx = cfruit.cx + cfruit.vx
        cfruit.vy = cfruit.vy + cfruit.ay
        cfruit.cy = cfruit.cy + cfruit.vy

# updates starfruit position
def updateStarFruit(app):
    for sfruit in app.starfruits:
        sfruit.cx = sfruit.cx + sfruit.vx
        sfruit.vy = sfruit.vy + sfruit.ay
        sfruit.cy = sfruit.cy + sfruit.vy

# update slices positions
def updateSlices(app):
    for slices in app.slice1s:
        if slices.inity0 > slices.inity1:
            slices.vy = slices.vy + slices.ay
            slices.vx = slices.vx + 0.25
            slices.x0 = slices.x0 - slices.vx
            slices.x1 = slices.x1 - slices.vx
            slices.y0 = slices.y0 - slices.vy
            slices.y1 = slices.y1 - slices.vy
        if slices.inity1 > slices.inity0:
            slices.vy = slices.vy + slices.ay
            slices.vx = slices.vx + 0.25
            slices.x0 = slices.x0 + slices.vx
            slices.x1 = slices.x1 + slices.vx
            slices.y0 = slices.y0 - slices.vy
            slices.y1 = slices.y1 - slices.vy
    for slice2s in app.slice2s: 
        if slice2s.inity1 < slice2s.inity0:
            slice2s.vy = slice2s.vy + slice2s.ay
            slice2s.vx = slice2s.vx + 0.25
            slice2s.x0 = slice2s.x0 + slice2s.vx
            slice2s.x1 = slice2s.x1 + slice2s.vx
            slice2s.y0 = slice2s.y0 - slice2s.vy
            slice2s.y1 = slice2s.y1 - slice2s.vy
        elif slice2s.inity0 < slice2s.inity1:
            slice2s.vy = slice2s.vy + slice2s.ay
            slice2s.vx = slice2s.vx + 0.25
            slice2s.x0 = slice2s.x0 - slice2s.vx
            slice2s.x1 = slice2s.x1 - slice2s.vx
            slice2s.y0 = slice2s.y0 - slice2s.vy
            slice2s.y1 = slice2s.y1 - slice2s.vy
            
def intersectionCircleLine(app, cx, cy):
    r = 25
    (x0, y0) = app.mousepress
    (x1, y1) = app.mouserelease
    slope = (y1 - y0) / (x1 - x0)
    yint = y1 - (slope * x1)
    a = 1**2 + slope**2
    b =(-2 * cx) + (2 * slope * (yint - cy))
    c = cx**2 + (yint - cy)**2 - (r**2)
    try:
        solx1 = (-b - math.sqrt(b**2 - (4*a*c))) / (2 * a)
        solx2 = (-b + math.sqrt(b**2 - (4*a*c))) / (2 * a)
        soly1 = solx1 * slope + yint
        soly2 = solx2 * slope + yint
        return (solx1, soly1), (solx2, soly2)
    except:
        return None
