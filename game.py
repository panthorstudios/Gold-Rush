from random import random
from random import randint
import pygame
from pygame.locals import *

from miner import Miner
from explosion import Explosion

class Game(object):
    TITLE = "Gold Rush!"
    BOARD_LEFT = 20
    BOARD_TOP = 130
    SQUARE_SIZE = 32
    BLACK = (0,0,0)
    GREEN=(128,255,128)
    YELLOW=(255,255,128)
    RED=(255,128,128)
    FRAMES_PER_SECOND = 30

    ASSAY_X = 540
    ASSAY_Y = 84
    CHARGES_X = 180 
    CASH_X = 20
    CASH_OFFSET = 30 
    GOLD_X = 16
    CHARGES_OFFSET = 32
    HEALTH_X =CHARGES_X + 40
    TITLE_X = 340

    def display_gold(self):
        scoretext='%03d' % self.gold
        for i in range(len(scoretext)):
            num=int(scoretext[i])*24
            pos=i*24
            self.screen.blit(self.digits,(self.CASH_X+self.CASH_OFFSET+(i*24),20),(num,0,24,35))

    def display_charges(self):
        scoretext='%02d' % self.charges
        for i in range(len(scoretext)):
            num=int(scoretext[i])*24
            pos=i*24
            self.screen.blit(self.digits,(self.CHARGES_X+self.CHARGES_OFFSET+(i*24),20),(num,0,24,35))

    def display_cash(self):
        scoretext='%05d' % self.cash
        for i in range(len(scoretext)):
            num=int(scoretext[i])*24
            pos=i*24
            self.screen.blit(self.digits,(self.CASH_X+self.CASH_OFFSET+(i*24),66),(num,0,24,35))

    def display_health(self):
         h=int(84*(self.health/100.0))
         b=84-h
         c=self.GREEN
         if self.health<20:
             c=self.RED
         elif self.health<40:
             c=self.YELLOW
         self.screen.fill(c,(self.HEALTH_X,70,h,32))
         self.screen.fill(self.BLACK,(self.HEALTH_X+h,70,b,32))
#        num=int(scoretext[i])*24
#        pos=i*24
#        self.screen.blit(self.digits,(self.CASH_X+self.CASH_OFFSET+(i*24),66),(num,0,24,35))


    def __init__(self):
        pygame.mixer.pre_init(44100,-16,2,2048)
        pygame.init()
        self.screen=pygame.display.set_mode((680,600))
        pygame.display.set_caption(self.TITLE)
        self.pressedkey=None
        self.bellsound=pygame.mixer.Sound('assets/sounds/bell.ogg')
        self.chargesound=pygame.mixer.Sound('assets/sounds/bomb.ogg')
        self.yeehawsound=pygame.mixer.Sound('assets/sounds/yeehaw.ogg')
        self.kachingsound=pygame.mixer.Sound('assets/sounds/kaching.ogg')
        self.board=[]
        self.bgbase=pygame.image.load('assets/images/background.png')
        self.bg=pygame.image.load('assets/images/background.png') 
        self.digits=pygame.image.load('assets/images/digits.png') 
        self.gamearea=pygame.Surface(self.bg.get_size())
        self.is_playing=False
 
# currently 2 nugget images
        self.nuggets=[]
        self.nuggets.append(pygame.image.load('assets/images/gold01-%dpx.png' % self.SQUARE_SIZE))
        self.nuggets.append(pygame.image.load('assets/images/gold02-%dpx.png' % self.SQUARE_SIZE))

        self.explosion=Explosion(0,0,self.SQUARE_SIZE)
        self.explosion_group=pygame.sprite.RenderPlain(self.explosion)
        self.miner=Miner(0,0)
        self.miner_group=pygame.sprite.RenderPlain(self.miner)
        self.clock=pygame.time.Clock()

# add title
        text=pygame.image.load('assets/images/text_title.png')
        self.screen.blit(text,(self.TITLE_X,self.BOARD_LEFT))

# add assay office
        self.office=pygame.image.load('assets/images/assayoffice.png')
        self.screen.blit(self.office,(self.ASSAY_X+self.BOARD_LEFT,self.ASSAY_Y))

        self.cash=0
        self.gold=0
        self.charges=10
        self.health=100

# add "Gold"
        text=pygame.image.load('assets/images/nugget.png')
        self.screen.blit(text,(self.GOLD_X,self.BOARD_LEFT))
        self.display_gold()

# add "Cash"
        text=pygame.image.load('assets/images/text_cash.png')
        self.screen.blit(text,(self.CASH_X,66))
        self.display_cash()

# add "Charges"
        text=pygame.image.load('assets/images/dynamite.png')
        self.screen.blit(text,(self.CHARGES_X,16))
        self.display_charges()

# add "Miner head"
        text=pygame.image.load('assets/images/miner_head.png')
        self.screen.blit(text,(self.CHARGES_X,66))
        self.display_health()


        self.setup()



    def setup(self):

# initialize score items
        self.cash=0
        self.gold=0
        self.charges=10

# load background image every time
        self.bg=pygame.image.load('assets/images/background.png')

#redraw assay office        
        self.bg.blit(self.office,(self.ASSAY_X,self.ASSAY_Y-self.BOARD_TOP))

        self.board=[]
# top row of empty spaces
        pathsup=2
        self.board.append([' ']*20)
        self.board.append(['*']*20)
        for y in range(2,14):
            row=[]
            for x in range(20):
                c='*'
                if random()<0.4:
# make a hole
                    self.bg.fill(self.BLACK,(x*self.SQUARE_SIZE,y*self.SQUARE_SIZE,self.SQUARE_SIZE,self.SQUARE_SIZE))
                    c=' '
                    if y>1:
                        c='G'
                        nugg=self.nuggets[0 if random()<0.5 else 1] 
                        self.bg.blit(nugg,(x*self.SQUARE_SIZE,y*self.SQUARE_SIZE))
                row.append(c)
            self.board.append(row)



# add soil
        self.gamearea.blit(self.bg,(0,0))
        pygame.display.flip()
      

 
    def print_board(self):
        for row in self.board:
            print ' '.join(row)




    def mainloop(self):
        deltat=self.clock.tick(self.FRAMES_PER_SECOND)
        tx=self.miner.x
        ty=self.miner.y
        self.miner_group.clear(self.gamearea,self.bg)
        self.explosion_group.clear(self.gamearea,self.bg)
 
        pressedspace=False
        for event in pygame.event.get():
            #print event
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit(0) 
                elif event.key in (K_RIGHT,K_LEFT,K_UP,K_DOWN):
                    self.pressedkey= event.key
                elif event.key == K_SPACE:
                    pressedspace = True
            elif event.type == KEYUP:
                if event.key in (K_RIGHT,K_LEFT,K_UP,K_DOWN):
                    if self.pressedkey == event.key:
                        self.pressedkey = None
                #elif event.key == K_SPACE:
                    #pressedspace = False

# only draw explosion if necessary
        if self.explosion.update(deltat):
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

                if bx>=0 and bx<20 and (by>0 or (by==0 and self.pressedkey == K_DOWN)) and by<20 and self.charges>0:
                    self.explosion.explode(bx,by)
                    self.charges-=1
#                    print "(%d,%d)->(%d,%d) Boom! %d charges left." % (self.miner.x,self.miner.y,bx,by,self.charges)
                    self.board[by][bx]=' '
                    self.bg.fill(self.BLACK,(bx*self.SQUARE_SIZE,by*self.SQUARE_SIZE,self.SQUARE_SIZE,self.SQUARE_SIZE))
                    self.gamearea.blit(self.bg,(0,0))
                    self.display_charges()
                    #self.screen.blit(self.digits,(460+(i*24),20),(num,0,24,35))
                    self.chargesound.play()
                    for j in range(20):
                        x=randint(0,19)
                        y=randint(2,11)
                        o=self.board[y][x]
                        a=self.board[y-1][x]
                        if o==' ' and a=='*':
                            self.board[y][x]='*'
                            xpos=x*self.SQUARE_SIZE
                            ypos=y*self.SQUARE_SIZE
                            self.bg.blit(self.bgbase,(x*self.SQUARE_SIZE,y*self.SQUARE_SIZE),(xpos,ypos,self.SQUARE_SIZE,self.SQUARE_SIZE))
 
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
                            self.cash+=self.gold*self.charges
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
                    self.bg.fill(self.BLACK,(self.miner.x*self.SQUARE_SIZE,self.miner.y*self.SQUARE_SIZE,self.SQUARE_SIZE,self.SQUARE_SIZE))
                    self.gamearea.blit(self.bg,(0,0))
                self.display_gold()

            self.miner.update_move()
            self.miner_group.update(deltat)
            self.miner_group.draw(self.gamearea)
        if self.miner.y>0:
            self.health-=0.25
            if self.health<0:
                self.health=0
                pass
            self.display_health()
        else:
            self.health+=1
            if self.health>100:
                self.health=100
            self.display_health()
  
        self.screen.blit(self.gamearea,(self.BOARD_LEFT,self.BOARD_TOP))

        pygame.display.flip()





