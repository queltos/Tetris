#! /usr/bin/env python

import pygame
import sys
import random

pygame.init()

white = pygame.Color("white")

class fieldsize:
    x = 10
    y = 18

rectsize = 20

#size = width, height = rectsize * fieldsize.x, rectsize * fieldsize.y
size = 640, 480

screen = pygame.display.set_mode(size)

ground = [[0] * fieldsize.y for x in range(fieldsize.x + 1)]

class Shape:
    def __init__(self, x = 0, y = 0, color = pygame.Color("yellow")):
        self.x = x
        self.y = y
        self.speed = 0

        self.color = color
        self.__init_bases__()

        self.rotation = 0
        self.blocks = self.bases[self.rotation]

    def create_base(self, bstring):
        base = []
        for (l_no, line) in enumerate(bstring.splitlines()):
            if line.strip() != "":
                for (c_no, char) in enumerate(line.split()):
                    if char == '#':
                        base.append(Block(c_no, l_no, self.color))
                    
        return base

    def __init_bases__(self):
        self.bases = []
        for bstring in self.bstrings:
            self.bases.append(self.create_base(bstring))

    def rotate(self):
        future_rotation = (self.rotation + 1) % len(self.bases)
        future_blocks = self.bases[future_rotation]
        
        if not self.collides(0, 0, future_blocks):
            self.rotation = (self.rotation + 1) % len(self.bases)
            self.blocks = self.bases[self.rotation]

    def get_rects(self):
        return self.rects

    def get_blocks(self):
        printables = []
        for block in self.blocks:
            xrel = block.x
            yrel = block.y
            xabs = self.x + xrel
            yabs = self.y + yrel
            printables.append(Block(xabs, yabs, block.color))
        return printables

    def move_left(self):
        if not self.collides(-1):
            self.x = self.x - 1

    def move_right(self):
        if not self.collides(1):
            self.x = self.x + 1

    def move_down(self):
        if not self.ground_collides(1):
            self.y = self.y + 1
            return True
        return False

    def collides(self, dx = 0, dy = 0, blocks = None):
        if blocks == None:
            blocks = self.blocks
        for block in blocks:
            x = block.x + self.x + dx
            y = block.y + self.y + dy
            if x < 0 or y < 0:
                return True
            if x > fieldsize.x - 1:
                return True
            if ground[x][y] != 0:
                return True
        return False

    def ground_collides(self, dy = 0):
        for block in self.blocks:
            x = block.x + self.x
            y = block.y + self.y
            if y + dy > fieldsize.y - 1:
                return True
            if ground[x][y + dy] != 0:
                return True
        return False

class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    
    def collides(self):
        x = block.x
        y = block.y
        if x < 0:
            return True
        if y > fieldsize.x - 1:
            return True
        if ground[x][y] != 0:
            return True
        return False

class Long(Shape):
    bstrings = []
    bstrings.append("""     0 0 0 0
                            # # # #
                            0 0 0 0
                            0 0 0 0
                   """)
    bstrings.append("""     0 # 0 0
                            0 # 0 0
                            0 # 0 0
                            0 # 0 0
                   """)

class Square(Shape):
    bstrings = []
    bstrings.append("""     # #
                            # #
                    """)

class StepRight(Shape):
    bstrings = []
    bstrings.append("""    0 # #
                           # # 0
                    """)
    bstrings.append("""    0 # 0
                           0 # #
                           0 0 #
                    """)

class StepLeft(Shape):
    bstrings = []
    bstrings.append("""    # # 0
                           0 # #
                    """)
    
    bstrings.append("""    0 # 0
                           # # 0
                           # 0 0
                    """)

class DoubleStep(Shape):
    bstrings = []
    bstrings.append("""    0 # 0
                           # # #
                    """)
    bstrings.append("""    0 # 0
                           0 # #
                           0 # 0
                    """)
    bstrings.append("""    0 0 0
                           # # #
                           0 # 0
                    """)
    bstrings.append("""    0 # 0
                           # # 0
                           0 # 0
                    """)

class LLeft(Shape):
    bstrings = []
    bstrings.append("""
                            0 0 0
                            # # #
                            0 0 #
                    """)
    bstrings.append("""
                            0 # 0
                            0 # 0
                            # # 0
                    """)
    bstrings.append("""
                            # 0 0
                            # # #
                            0 0 0
                    """)
    bstrings.append("""
                            0 # #
                            0 # 0
                            0 # 0
                    """)

class LRight(Shape):
    bstrings = []
    bstrings.append("""
                            0 0 0
                            # # #
                            # 0 0
                    """)
    bstrings.append("""
                            # # 0
                            0 # 0
                            0 # 0
                    """)
    bstrings.append("""
                            0 0 #
                            # # #
                            0 0 0
                    """)
    bstrings.append("""
                            0 # 0
                            0 # 0
                            0 # #
                    """)

class Renderer:
    def draw_Shape(shape, playfield):
        for block in shape.get_blocks():
            draw_Rect(block.x, block.y, playfield, block.color)
    
    def draw_Rect(x, y, playfield, color):
        rect = pygame.Rect(x * rectsize + playfield.x, y * rectsize + playfield.y \
                , rectsize + 1, rectsize + 1)
        screen.fill(color, rect)
        pygame.draw.rect(screen, pygame.Color("black"), rect, 1)
    
    def draw_grid():
        for x in range(0, fieldsize.x + 1):
            for y in range(0, fieldsize.y + 1):
                draw_Rect(x, y, pygame.Color("white"))
    
    def draw_ground(playfield):
        for line in ground:
            for block in line:
                if block != 0:
                    draw_Rect(block.x, block.y, playfield, block.color)

    def draw_enemy():
        for block in logic.enemy_blocks:
            draw_Rect(block.x, block.y, playfield2, block.color)

    def draw_playfield_borders(playfield):
        rect = pygame.Rect(playfield.x, playfield.y, \
                rectsize * playfield.size['x'] + 1, \
                rectsize * playfield.size['y'] + 1)
        pygame.draw.rect(screen, pygame.Color("black"), rect, 1)

class Playfield:
    def __init__(self, x, y, x_size, y_size):
        self.x = x
        self.y = y
        self.size = {'x': x_size, 'y': y_size}

    def draw_borders(self):
        rect = pygame.Rect(self.x, self.y, rectsize * self.size['x'] + 1, \
                rectsize * self.size['y'] + 1)
        pygame.draw.rect(screen, pygame.Color("black"), rect, 1)

class GameLogic():
    def __init__(self):
        self.shape = None
        self.nextshape = self.make_shape()
        self.ticklength = 1000
        self.enemy_blocks = []

    def make_shape(self):
        shapes = [Square, StepRight, StepLeft, Long, DoubleStep, LLeft, LRight]
        shapeclass = random.choice(shapes)
        return shapeclass(fieldsize.x + 2, 1)

    def spawn_shape(self):
        x = fieldsize.x / 2 - 2
        y = 0

        self.shape = self.nextshape

        if type(self.shape) in [Long, LLeft, LRight]:
            y = -1

        self.shape.x = x
        self.shape.y = y
        self.nextshape = self.make_shape()
        self.starttime = pygame.time.get_ticks()

    def start(self):
        if self.shape == None:
           self.spawn_shape()

    def remove_line(self, line_no):
        """Remove single given line from ground, shift blocks above this line down 
        by one"""

        for y in range(line_no, 0, -1):
            for x in range(fieldsize.x):
                ground[x][y] = ground[x][y - 1]
                if ground[x][y] != 0:
                    ground[x][y].y += 1

    def remove_lines(self, lines):
        for y in lines:
            self.remove_line(y)

    def check_rows(self):
        completed = []
        complete = False
        for block in self.shape.get_blocks():
            complete = True
            for x in range(fieldsize.x):
                if ground[x][block.y] == 0:
                    complete = False
                    break
            if complete and block.y not in completed:
                completed.append(block.y)
        self.remove_lines(completed)

    def move_down(self):
        if not self.shape.move_down():
            for block in self.shape.blocks:
                # set absolute coordinates in blocks
                x = block.x + self.shape.x
                y = block.y + self.shape.y
                color = pygame.Color("red")
                ground[x][y] = Block(x, y, color)
            self.check_rows()
            self.spawn_shape()
            
#            self.send_update()
            return False
#        self.send_update()
        return True

    def move_bottom(self):
        while self.move_down():
            pass

    def send_update(self):
        peer.send(ground + self.shape.get_blocks())

class Ticker:
    def __init__(self, interval, function = None):
        self.interval = interval
        self.lasttick = 0
        self.nexttick = 0
        self.function = function
        self.active = True

    def start(self):
        self.lasttick = pygame.time.get_ticks()
        self.nexttick = self.lasttick + self.interval

    def tick(self):
        if pygame.time.get_ticks() >= self.nexttick:
            if self.active:
                self.function()
            self.lasttick = self.nexttick
            self.nexttick += self.interval
        pass

def main():
    playfield = Playfield(5, 5, 10, 18)
    #playfield2 = Playfield(20 + fieldsize.x * rectsize, 5, fieldsize.x, fieldsize.y)
    
    logic = GameLogic()
    logic.start()
    t = Ticker(500, logic.move_down)
    t.start()
    tspeedy = Ticker(100, logic.move_down)
    tspeedy.active = False
    tspeedy.start()
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    logic.shape.rotate()
                if event.key == pygame.K_LEFT:
                    logic.shape.move_left()
                if event.key == pygame.K_RIGHT:
                    logic.shape.move_right()
                if event.key == pygame.K_DOWN:
                    t.active = False
                    tspeedy.active = True
                if event.key == pygame.K_SPACE:
                    logic.move_bottom()
                if event.key == pygame.K_p:
                    t.active = not t.active
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    tspeedy.active = False
                    t.active = True
    
        t.tick()
        tspeedy.tick()
    
        screen.fill(white)
        playfield.draw_borders()
        #playfield2.draw_borders()
        draw_enemy()
    
        draw_Shape(logic.shape, playfield)
        draw_Shape(logic.nextshape, playfield)
        draw_ground(playfield)
    
        pygame.display.flip()

if __name__ == '__main__': main()
