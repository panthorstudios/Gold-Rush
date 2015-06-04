from random import random
import pygame
from pygame.locals import *

from miner import Miner
from explosion import Explosion

class Game(object):
    TITLE = "Gold Rush!"
    BOARD_LEFT = 20
    BOARD_TOP = 100
    NUGGET_SIZE = 32
    BLACK = (0,0,0)
    FRAMES_PER_SECOND = 30
    def __init__(self):
        pygame.mixer.pre_init(44100,-16,2,2048)
        pygame.init()
        self.screen=pygame.display.set_mode((680,600))
        pygame.display.set_caption(self.TITLE)
        self.pressedkey=None
        self.bellsound=pygame.mixer.Sound('sounds/bell.ogg')
        self.bombsound=pygame.mixer.Sound('sounds/bomb.ogg')
        self.yeehawsound=pygame.mixer.Sound('sounds/yeehaw.ogg')
        self.kachingsound=pygame.mixer.Sound('sounds/kaching.ogg')
        self.board=[]
        self.bg=pygame.image.load('images/background.png') 
        self.digits=pygame.image.load('images/digits.png') 
        self.gamearea=pygame.Surface(self.bg.get_size())
 
# currently 2 nugget images
        self.nuggets=[]
        self.nuggets.append(pygame.image.load('images/gold01-%dpx.png' % self.NUGGET_SIZE))
        self.nuggets.append(pygame.image.load('images/gold02-%dpx.png' % self.NUGGET_SIZE))

        self.explosion=Explosion(0,0)
        self.explosion_group=pygame.sprite.RenderPlain(self.explosion)
        self.miner=Miner(0,0)
        self.miner_group=pygame.sprite.RenderPlain(self.miner)


        self.clock=pygame.time.Clock()

# initialize score items
        self.cash=0
        self.gold=0
        self.bombs=10

        self.board=[]
# top row of empty spaces
        pathsup=2
        self.board.append([' ']*20)
#        self.board.append(['*']*20)
        for y in range(1,14):
            row=[]
            for x in range(20):
                c='*'
                if random()<0.4:
# make a hole
                    self.bg.fill(self.BLACK,(x*self.NUGGET_SIZE,y*self.NUGGET_SIZE,self.NUGGET_SIZE,self.NUGGET_SIZE))
                    c=' '
                    if y>1:
                        c='G'
                        nugg=self.nuggets[0 if random()<0.5 else 1] 
                        self.bg.blit(nugg,(x*self.NUGGET_SIZE,y*self.NUGGET_SIZE))
                row.append(c)
            self.board.append(row)

# add title
        text=pygame.image.load('images/text_title.png')
        self.screen.blit(text,(self.BOARD_LEFT-8,self.BOARD_LEFT))

# add "Gold"
        text=pygame.image.load('images/text_gold.png')
        self.screen.blit(text,(340,self.BOARD_LEFT))
        self.display_gold()

# add "Cash"
        text=pygame.image.load('images/text_cash.png')
        self.screen.blit(text,(self.BOARD_LEFT-8,554))
        self.display_cash()

# add "Charges"
        text=pygame.image.load('images/text_charges.png')
        self.screen.blit(text,(380,554))
        self.display_charges()

# add assay office
        office=pygame.image.load('images/assayoffice.png')
        ox=540
        oy=50
        self.bg.blit(office,(ox,oy-self.BOARD_TOP))
        self.screen.blit(office,(ox+self.BOARD_LEFT,oy))



# add soil
        self.gamearea.blit(self.bg,(0,0))

        pygame.display.flip()
       
    def print_board(self):
        for row in self.board:
            print ' '.join(row)

    def cycle(self):
        deltat=self.clock.tick(self.FRAMES_PER_SECOND)
        tx=self.miner.x
        ty=self.miner.y
        self.miner_group.clear(self.gamearea,self.bg)
        self.explosion_group.clear(self.gamearea,self.bg)
 
        pressedspace=False
        for event in pygame.event.get():
            #print event
            if event.type == KEYDOWN:
                if event.key in (K_RIGHT,K_LEFT,K_UP,K_DOWN):
                    self.pressedkey= event.key
                elif event.key == K_SPACE:
                    pressedspace = True
            elif event.type == KEYUP:
                if event.key in (K_RIGHT,K_LEFT,K_UP,K_DOWN):
                    if self.pressedkey == event.key:
                        self.pressedkey = None
                #elif event.key == K_SPACE:
                    #pressedspace = False

        if self.explosion.exploding:
            self.explosion.update(deltat)
            self.explosion_group.update(deltat)
            self.explosion_group.draw(self.gamearea)

        else:
            if pressedspace and self.pressedkey:
# Do explosion
                pressedspace=False
                bx=self.miner.x
                by=self.miner.y
                if self.pressedkey == K_LEFT:
                    bx-=1
                if self.pressedkey == K_RIGHT:
                    bx+=1
                if self.pressedkey == K_UP:
                    by-=1
                if self.pressedkey == K_DOWN:
                    by+=1

                if bx>0 and bx<20 and by>1 and by<20 and self.bombs>0:
                    self.explosion.start_explosion(bx,by)
                    self.bombs-=1
#                    print "(%d,%d)->(%d,%d) Boom! %d bombs left." % (self.miner.x,self.miner.y,bx,by,self.bombs)
                    self.board[by][bx]=' '
                    self.bg.fill(self.BLACK,(bx*self.NUGGET_SIZE,by*self.NUGGET_SIZE,self.NUGGET_SIZE,self.NUGGET_SIZE))
                    self.gamearea.blit(self.bg,(0,0))
                    self.display_charges()
                    pygame.display.flip()
                    self.bombsound.play()
  
            if self.pressedkey == K_RIGHT and self.miner.can_move():
                if tx<19:
                    tx += 1
 
            if self.pressedkey == K_LEFT and self.miner.can_move(): 
                if tx>0:
                    tx -= 1
            if self.pressedkey == K_UP and self.miner.can_move():
                if ty>0:
                    ty -= 1
                else:
                    if tx==17:
                        if self.gold!=0:
                            self.cash+=self.gold*10
                            self.gold=0
                            self.kachingsound.play()
                            self.display_gold()
                            self.display_cash()
                            self.yeehawsound.play()
                            
            if self.pressedkey == K_DOWN and self.miner.can_move():
                if ty<13:
                    ty += 1

            
            o=self.board[ty][tx]

            if (tx!=self.miner.x or ty!=self.miner.y) and o in ' G':
                self.miner.set_location(tx,ty)
                if o=='G':
                    self.board[ty][tx]=' '
                    self.gold += 1
                    self.bellsound.play()
                    self.bg.fill(self.BLACK,(self.miner.x*self.NUGGET_SIZE,self.miner.y*self.NUGGET_SIZE,self.NUGGET_SIZE,self.NUGGET_SIZE))
                    self.gamearea.blit(self.bg,(0,0))
                self.display_gold()

            self.miner.update_move()
            self.miner_group.update(deltat)
            self.miner_group.draw(self.gamearea)

        self.screen.blit(self.gamearea,(self.BOARD_LEFT,self.BOARD_TOP))

        pygame.display.flip()


    def display_gold(self):
        scoretext='%03d' % self.gold
        for i in range(len(scoretext)):
            num=int(scoretext[i])*24
            pos=i*24 
            self.screen.blit(self.digits,(460+(i*24),20),(num,0,24,35))

    def display_charges(self):
        scoretext='%02d' % self.bombs
        for i in range(len(scoretext)):
            num=int(scoretext[i])*24
            pos=i*24
            self.screen.blit(self.digits,(580+(i*24),554),(num,0,24,35))

    def display_cash(self):
        scoretext='%05d' % self.cash
        for i in range(len(scoretext)):
            num=int(scoretext[i])*24
            pos=i*24
            self.screen.blit(self.digits,(166+(i*24),554),(num,0,24,35))



