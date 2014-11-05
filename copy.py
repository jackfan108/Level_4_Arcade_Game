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

#cord to pixel
def screen_pos (x,y):
    return (x*CELL_SIZE+10,y*CELL_SIZE+10)

#pixel to cord
def pixel_to_index (x,y):
    indx = (x-10) / CELL_SIZE
    indy = (y-10) / CELL_SIZE
    return indx, indy

#screen 1-D array to cord
def screen_pos_index (index):
    x = index % LEVEL_WIDTH
    y = (index - x) / LEVEL_WIDTH
    return screen_pos(x,y)

#cord to screen 1-D array
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
                if self._level[index(tx,ty)] == 2 or ((self._level[index(tx,ty)] == 0 or self._level[index(tx,ty)] == 3)and self._level[index(self._x, self._y)] == 2):
                  self._x = tx
                  self._y = ty
                  self._img.move(dx*CELL_SIZE,dy*CELL_SIZE)
                
                

class Player (Character):
    def __init__ (self,x,y,window,level):
        Character.__init__(self,'android.gif',x,y,window,level)

    def at_exit (self):
        return (self._y == 0)

    def digright (self, screen, brickdic):
        if screen[index(self._x+1,self._y)] == 0 and screen[index(self._x+1,self._y+1)] == 1:
            screen[index(self._x+1,self._y+1)] = 0
            brickdic[(self._x+1, self._y+1)].undraw()
            return screen
    def digleft (self, screen, brickdic):
        if screen[index(self._x-1,self._y)] == 0 and screen[index(self._x-1,self._y+1)] == 1:
            screen[index(self._x-1,self._y+1)] = 0
            brickdic[(self._x-1, self._y+1)].undraw()
            return screen

class Baddie (Character):
    baddiecords = []
    def __init__ (self,x,y,window,level,player):
        Character.__init__(self,'red.gif',x,y,window,level)
        self._player = player
        Baddie.baddiecords.append((x,y))

def gold_collected (player, window, level, golddic):

    if len(golddic) == 0:
        for i in range(3):
            level[index(34,i)] = 2
            draw_item(level, window, 'ladder', index(34,i))
        player._img.undraw()
        player._img.draw(window)




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
    screen.extend([2,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,2,0,0,0,0,0,1,0,0,2,0,0,1,0,0,0,1,2])
    screen.extend([2,0,1,1,1,1,0,0,1,2,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,2,0,0,1,1,1,1,1,2])
    screen.extend([2,0,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,2])
    screen.extend([1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1])
    screen.extend([1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,2,0,0,0,0,0,0,0,1])
    screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])


    # screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,2,0,0,0,0,0,0,0,2,1,1,1,1,1,1,1,1,1,1,1,1,0])
    # screen.extend([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    # screen.extend([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0])
    # screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1])
    # screen.extend([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1,2,1,0,0,0,1,2,0,1])
    # screen.extend([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,1,1,1,1])
    # screen.extend([3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,0,0,0,0,0,0,0,0,2,0,0,0,0,3,3,3,3])
    # screen.extend([2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0])
    # screen.extend([2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1])
    # screen.extend([2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,2,3,3,3,3,3,3,3,2])
    # screen.extend([2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2])
    # screen.extend([2,0,0,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2])
    # screen.extend([2,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,2,1,0,0,0,0,3,3,3,2,0,0,1,1,1,1,1,2])
    # screen.extend([2,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,2,1,1,1,1,1,1,0,0,2,0,0,1,0,0,0,1,2])
    # screen.extend([2,0,1,4,4,1,0,0,1,0,4,4,4,1,0,0,1,2,0,4,4,4,0,1,0,0,2,0,0,1,4,4,4,1,2])
    # screen.extend([2,0,1,1,1,1,0,0,1,2,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,2,0,0,1,1,1,1,1,2])
    # screen.extend([2,0,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,2])
    # screen.extend([1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1])
    # screen.extend([1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,2,0,0,0,0,0,0,0,1])
    # screen.extend([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    return screen

def draw_item(level, window, item, index):
    def image (sx,sy,what):
        return Image(Point(sx+CELL_SIZE/2,sy+CELL_SIZE/2),what)
    item = item + '.gif'
    sx, sy = screen_pos_index(index)
    elt = image(sx, sy, item)
    elt.draw(window)
    return sx, sy, elt

def create_screen (level,window):
    # use this instead of Rectangle below for nicer screen
    brickdic = {}
    golddic = {}
    for (index,cell) in enumerate(level):
        if cell == 1:
            sx, sy, elt = draw_item(level, window, 'brick', index)
            brickdic[pixel_to_index(sx, sy)] = elt
        elif cell == 2:
            draw_item(level, window, 'ladder', index)
        elif cell == 3:
            draw_item(level, window, 'rope', index)
        elif cell == 4:
            sx, sy, elt = draw_item(level, window, 'gold', index)
            golddic[pixel_to_index(sx, sy)] = elt
    return brickdic, golddic


MOVE = {
    'Left': (-1,0),
    'Right': (1,0),
    'Up' : (0,-1),
    'Down' : (0,1)
}

#returns whatever the character is
def collision_detetction(window, level, player, baddiecords, golddic):
    px = player._x
    py = player._y
    if level[index(px,py)] == 4:
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

    #baddie1 = Baddie(5,2, window,level,p)
    #baddie2 = Baddie(18,1,window,level,p)
    #baddie3 = Baddie(32,2,window,level,p)

    while not p.at_exit():
        key = window.checkKey()
        if key == 'q':
            window.close()
            exit(0)
        elif key == 'a':
            p.digleft(level, brickdic)
        elif key == 'z':
            p.digright(level, brickdic)
        elif key in MOVE:
            (dx,dy) = MOVE[key]
            p.move(dx,dy)
            collision = collision_detetction(window, level, p, Baddie.baddiecords, golddic)
            if collision == 'gold':
                level[index(p._x, p._y)] = 0
                golddic[(p._x, p._y)].undraw()
                del golddic[(p._x, p._y)]
                gold_collected (p, window, level, golddic)
                print golddic
            elif collision == 'baddie':
                lost(window)

        # baddies should probably move here

    won(window)

if __name__ == '__main__':
    main()
