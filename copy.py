#
# MAZE
# 
# Example game
#
# Version without baddies running around
#


from graphics import *

LEVEL_WIDTH = 35
LEVEL_HEIGHT = 20    

CELL_SIZE = 24
WINDOW_WIDTH = CELL_SIZE*LEVEL_WIDTH
WINDOW_HEIGHT = CELL_SIZE*LEVEL_HEIGHT


def screen_pos (x,y):
    return (x*CELL_SIZE+10,y*CELL_SIZE+10)

def screen_pos_index (index):
    x = index % LEVEL_WIDTH
    y = (index - x) / LEVEL_WIDTH
    return screen_pos(x,y)

def pixel_to_index (x,y):
    indx = (x-10) / CELL_SIZE
    indy = (y-10) / CELL_SIZE
    return indx, indy

def index (x,y):
    return x + (y*LEVEL_WIDTH)

class Character (object):
    def __init__ (self,pic,x,y,window,level):
        (sx,sy) = screen_pos(x,y)
        self._img = Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2+2),pic)
        self._window = window
        self._img.draw(window)
        self._x = x
        self._y = y
        self._level = level

    def same_loc (self,x,y):
        return (self._x == x and self._y == y)

    def move (self,dx,dy):
        tx = self._x + dx
        ty = self._y + dy
        if tx >= 0 and ty >= 0 and tx < LEVEL_WIDTH and ty < LEVEL_HEIGHT:
            if self._level[index(tx,ty)] != 1:
              if dy != -1:
                self._x = tx
                self._y = ty
                self._img.move(dx*CELL_SIZE,dy*CELL_SIZE)
                while (self._level[index(self._x, self._y)] != 3 and (self._level[index(self._x, self._y+1)] == 0 or self._level[index(self._x, self._y+1)] == 3)): #falling
                  self._y += 1
                  self._img.move(0*CELL_SIZE,1*CELL_SIZE)
              elif dy == -1: # only move up on ladders
                if self._level[index(tx,ty)] == 2 or (self._level[index(tx,ty)] == 0 and self._level[index(self._x, self._y)] == 2):
                  self._x = tx
                  self._y = ty
                  self._img.move(dx*CELL_SIZE,dy*CELL_SIZE)
                
                

class Player (Character):
    def __init__ (self,x,y,window,level):
        Character.__init__(self,'android.gif',x,y,window,level)

    def at_exit (self):
        return (self._y == 0)


class Baddie (Character):
    baddiecords = []
    def __init__ (self,x,y,window,level,player):
        Character.__init__(self,'red.gif',x,y,window,level)
        self._player = player
        Baddie.baddiecords.append((x,y))


def lost (window):
    t = Text(Point(WINDOW_WIDTH/2+10,WINDOW_HEIGHT/2+10),'YOU LOST!')
    t.setSize(36)
    t.setTextColor('red')
    t.draw(window)
    window.getKey()
    exit(0)

def won (window):
    t = Text(Point(WINDOW_WIDTH/2+10,WINDOW_HEIGHT/2+10),'YOU WON!')
    t.setSize(36)
    t.setTextColor('red')
    t.draw(window)
    window.getKey()
    exit(0)

# 0 empty
# 1 brick
# 2 ladder
# 3 rope
# 4 gold

def create_level(self):
    screen = []
    screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,0])
    screen.extend([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    screen.extend([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0])
    screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1])
    screen.extend([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1,2,1,0,0,0,1,2,0,1])
    screen.extend([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,1,1,1,1])
    screen.extend([3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,0,0,0,0,0,0,0,0,2,0,0,0,0,3,3,3,3])
    screen.extend([2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0])
    screen.extend([2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1])
    screen.extend([2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,2,3,3,3,3,3,3,3,2])
    screen.extend([2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2])
    screen.extend([2,0,0,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2])
    screen.extend([2,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,2,1,0,0,0,0,3,3,3,2,0,0,1,1,1,1,1,2])
    screen.extend([2,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,2,1,1,1,1,1,1,0,0,2,0,0,1,0,0,0,1,2])
    screen.extend([2,0,1,4,4,1,0,0,1,0,4,4,4,1,0,0,1,2,0,4,4,4,0,1,0,0,2,0,0,1,4,4,4,1,2])
    screen.extend([2,0,1,1,1,1,0,0,1,2,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,2,0,0,1,1,1,1,1,2])
    screen.extend([2,0,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,2])
    screen.extend([1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1])
    screen.extend([1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,2,0,0,0,0,0,0,0,1])
    screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    return screen

def create_screen (level,window):
    # use this instead of Rectangle below for nicer screen
    brick = 'brick.gif'
    ladder = 'ladder.gif'
    gold = 'gold.gif'
    rope = 'rope.gif'
    brickdic = {}
    golddic = {}
    def image (sx,sy,what):
        return Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2),what)

    for (index,cell) in enumerate(level):
        if cell == 1:
            (sx,sy) = screen_pos_index(index)
            elt = image(sx,sy,brick)
            brickdic[pixel_to_index(sx, sy)] = elt
            elt.draw(window)
        elif cell == 2:
            (sx,sy) = screen_pos_index(index)
            elt = image(sx,sy,ladder)
            elt.draw(window)
        elif cell == 3:
            (sx,sy) = screen_pos_index(index)
            elt = image(sx,sy,rope)
            elt.draw(window)
        elif cell == 4:
            (sx,sy) = screen_pos_index(index)
            elt = image(sx,sy,gold)
            golddic[pixel_to_index(sx, sy)] = elt
            elt.draw(window)
    return brickdic, golddic


MOVE = {
    'Left': (-1,0),
    'Right': (1,0),
    'Up' : (0,-1),
    'Down' : (0,1)
}

#returns whatever the character is
def collision_detetction(player, screen, baddiecords):
    px = player._x
    py = player._y
    if screen[index(px,py)] == 4:
        return 'gold'
    for cord in baddiecords:
        if (px, py) == cord:
            return 'baddie'
    return None

def main ():

    window = GraphWin("Maze", WINDOW_WIDTH+20, WINDOW_HEIGHT+20)

    rect = Rectangle(Point(5,5),Point(WINDOW_WIDTH+15,WINDOW_HEIGHT+15))
    rect.setFill('sienna')
    rect.setOutline('sienna')
    rect.draw(window)
    rect = Rectangle(Point(10,10),Point(WINDOW_WIDTH+10,WINDOW_HEIGHT+10))
    rect.setFill('white')
    rect.setOutline('white')
    rect.draw(window)

    level = create_level(1)

    brickdic, golddic = create_screen(level,window)
    p = Player(10,18,window,level)

    baddie1 = Baddie(5,18,window,level,p)
    #baddie2 = Baddie(10,18,window,level,p)
    baddie3 = Baddie(15,18,window,level,p)

    while not p.at_exit():
        key = window.checkKey()
        if key == 'q':
            window.close()
            exit(0)
        if key in MOVE:
            (dx,dy) = MOVE[key]
            p.move(dx,dy)
            collision = collision_detetction(p, level, Baddie.baddiecords)
            if collision == 'gold':
                level[index(p._x, p._y)] = 0
                golddic[(p._x, p._y)].undraw()
            elif collision == 'baddie':
                lost(window)

        # baddies should probably move here

    won(window)

if __name__ == '__main__':
    main()
