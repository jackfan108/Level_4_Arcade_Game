#
# MAZE
# 
# Example game
#
# Version without baddies running around
#
import time
from random import choice

from graphics import *

LEVEL_WIDTH = 35
LEVEL_HEIGHT = 20    

CELL_SIZE = 24
WINDOW_WIDTH = CELL_SIZE*LEVEL_WIDTH
WINDOW_HEIGHT = CELL_SIZE*LEVEL_HEIGHT

MOVE = {
    'Left': (-1,0),
    'Right': (1,0),
    'Up' : (0,-1),
    'Down' : (0,1)
}

def time_to_tick(start, tick):
    elapsed = (time.time() - start)*2
    if int(elapsed) != tick:
        return False, int(elapsed)
    return True, int(elapsed)

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
        if in_level(tx,ty):
            dest = self._level[index(tx,ty)]
            if dest != 1: # not brick
                if dy != -1:
                    self._x = tx
                    self._y = ty
                    self._img.move(dx*CELL_SIZE,dy*CELL_SIZE)
                    while (can_fall(self)): #falling
                        self._y += 1
                        self._img.move(0*CELL_SIZE,1*CELL_SIZE)
                elif dy == -1: # only move up on ladders
                    square_at = self._level[index(self._x, self._y)]
                    if (dest == 2 or (dest in [0,3] and square_at == 2)) and square_at == 2:
                        self._x = tx
                        self._y = ty
                        self._img.move(dx*CELL_SIZE,dy*CELL_SIZE)

def in_level(x,y):
    return x >= 0 and y >= 0 and x < LEVEL_WIDTH and y < LEVEL_HEIGHT

def can_fall(character):
    if (character._y < (LEVEL_HEIGHT - 1)):
        square_at = character._level[index(character._x, character._y)]
        square_below = character._level[index(character._x, character._y+1)]
        return square_at not in [2,3,4] and (square_below in [0,3,4])
    return False

class Player (Character):
    def __init__ (self,x,y,window,level):
        Character.__init__(self,'t_android.gif',x,y,window,level)

    def at_exit (self):
        return (self._y == 0)

    def digright (self, screen, brickdic, refill, tick):
        # check right and diagright space
        if screen[index(self._x+1,self._y)] == 0 and screen[index(self._x+1,self._y+1)] == 1:
            screen[index(self._x+1, self._y+1)] = 0
            brickdic[(self._x+1, self._y+1)].undraw()
            refill.append((self._x+1, self._y+1, tick + 4))
            for baddie in Baddie.baddies:
              if (baddie._x, baddie._y) == (self._x+1,self._y): # force falling on dig
                baddie.move(baddie._x, baddie._y)
            return screen
    def digleft (self, screen, brickdic, refill, tick):
        #check left and diagleft space
        if screen[index(self._x-1,self._y)] == 0 and screen[index(self._x-1,self._y+1)] == 1:
            screen[index(self._x-1, self._y+1)] = 0
            brickdic[(self._x-1, self._y+1)].undraw()
            refill.append((self._x-1, self._y+1, tick + 4))
            for baddie in Baddie.baddies:
              if (baddie._x, baddie._y) == (self._x-1,self._y): # force falling on dig
                baddie.move(baddie._x, baddie._y)
            return screen

class Baddie (Character):
    baddies = []
    def __init__ (self,x,y,window,level,player):
        Character.__init__(self,'t_red.gif',x,y,window,level)
        self._player = player
        Baddie.baddies.append(self)

    # returns a list of the possible coordinates to go to
    def possible_moves(self, level):
        moves = []
        x, y = self._x, self._y
        if in_level(x,y):
            if level[index(x, y+1)] != 1:
                moves.append((0, 1))
            if level[index(x+1, y)] != 1:
                moves.append((1, 0))
            if level[index(x-1, y)] != 1:
                moves.append((-1, 0))
            if level[index(x, y-1)] != 1 and level[index(x, y)] == 2:
                moves.append((0, -1))
        return moves

def gold_collected (player, window, level, golddic, exitrow, exitlength):

    if len(golddic) == 0:
        for i in range(exitlength):
            level[index(exitrow,i)] = 2
            draw_item(level, window, 'ladder', index(exitrow,i))
        player._img.undraw()
        player._img.draw(window)
        for baddie in Baddie.baddies:
            baddie._img.undraw()
            baddie._img.draw(window)


def refill (window, level, brickdic, refill, sameTick, tick, player, baddielist):
    for x, y, btick in refill:
        if not sameTick and tick == btick:
            level[index(x, y)] = 1
            brickdic[(x, y)].draw(window)
            if (x, y) == (player._x, player._y):
                lost(window)
            for baddie in baddielist:
                if (x, y) == (baddie._x, baddie._y):
                    baddie._img.undraw()
                    baddielist.remove(baddie)

    return level




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

def create_level(level):
    screen = []
    # convert string into list of ints
    for line in range(1,LEVEL_HEIGHT+1):
      screen.extend(map(int,level[line].strip().split(',')))
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

#returns whatever the character is
def collision_detetction(window, level, character, player, golddic):
    px = player._x
    py = player._y
    cx = character._x
    cy = character._y
    # anyone can pick up gold
    if level[index(cx,cy)] == 4:
        return 'gold'
    # we only care about baddie-player collisions
    for baddie in Baddie.baddies:
        if (px, py) == (baddie._x, baddie._y):
            return 'baddie'
    return None

def main ():

    window = GraphWin("Maze", WINDOW_WIDTH+20, WINDOW_HEIGHT+20)
    for currentlevel in ['level1','level52','level148']:
      rect = Rectangle(Point(5,5),Point(WINDOW_WIDTH+15,WINDOW_HEIGHT+15))
      rect.setFill('sienna')
      rect.setOutline('sienna')
      rect.draw(window)
      rect = Rectangle(Point(10,10),Point(WINDOW_WIDTH+10,WINDOW_HEIGHT+10))
      rect.setFill('white')
      rect.setOutline('white')
      rect.draw(window)
      levelfile = open(currentlevel+'.txt', 'r').read().splitlines()
      
      level = create_level(levelfile)
      brickdic, golddic = create_screen(level,window)
      refilllist = []
      p = Player(int(levelfile[23]),int(levelfile[24]),window,level) # spawn player from the file
      for i in range(1,int(levelfile[27])+1): # create baddies out of the file
        baddie = Baddie(int(levelfile[2*i+26]),int(levelfile[2*i+27]),window,level,p)
      start = time.time()
      tick = 0
      exitrow = int(levelfile[38])
      exitlength = int(levelfile[39])
      
      while not p.at_exit():
          sameTick, tick = time_to_tick(start, tick)
          if sameTick == False:
              level = refill(window, level, brickdic, refilllist, sameTick, tick, p, Baddie.baddies)
              for baddie in Baddie.baddies:
                  try:
                    x, y = choice(baddie.possible_moves(level))
                    baddie.move(x, y)
                  except IndexError: # if we don't have any moves
                    baddie.move(baddie._x, baddie._y)
                  collision = collision_detetction(window, level, baddie, p, golddic) # need to also run collision detection with bad guys
                  if collision == 'gold':
                      level[index(baddie._x, baddie._y)] = 0
                      golddic[(baddie._x, baddie._y)].undraw()
                      del golddic[(baddie._x, baddie._y)]
                      gold_collected (p, window, level, golddic, exitrow, exitlength)
                  elif collision == 'baddie':
                      lost(window)
          key = window.checkKey()
          if key == 'q':
              window.close()
              exit(0)
          elif key == 'a':
              p.digleft(level, brickdic, refilllist, tick)
          elif key == 'z':
              p.digright(level, brickdic, refilllist, tick)
          elif key in MOVE:
              (dx,dy) = MOVE[key]
              p.move(dx,dy)
              collision = collision_detetction(window, level, p, p, golddic)
              if collision == 'gold':
                  level[index(p._x, p._y)] = 0
                  golddic[(p._x, p._y)].undraw()
                  del golddic[(p._x, p._y)]
                  gold_collected (p, window, level, golddic, exitrow, exitlength)
              elif collision == 'baddie':
                  lost(window)
      for item in window.items[:]:
        item.undraw()
      Baddie.baddies = [] # reset the enemy list
    won(window)

if __name__ == '__main__':
    main()
