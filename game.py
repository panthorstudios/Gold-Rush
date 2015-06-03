from random import random
import pygame

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
        self.gold=0
        self.bombs=10
        self.explosion=Explosion(self.BOARD_LEFT,self.BOARD_TOP)
        self.explosion_group=pygame.sprite.RenderPlain(self.explosion)
        self.miner=Miner(self.BOARD_LEFT,self.BOARD_TOP)
        self.miner_group=pygame.sprite.RenderPlain(self.miner)
        self.bellsound=pygame.mixer.Sound('sounds/bell.ogg')
        self.bombsound=pygame.mixer.Sound('sounds/bomb.ogg')
        self.board=[]
        self.bg=pygame.image.load('images/background.png') #.convert(24)
        title=pygame.image.load('images/text_title.png')
        self.nuggets=[]
        self.nuggets.append(pygame.image.load('images/gold01-%dpx.png' % self.NUGGET_SIZE))
        self.nuggets.append(pygame.image.load('images/gold02-%dpx.png' % self.NUGGET_SIZE))
        self.clock=pygame.time.Clock()
        self.cash=0

        self.board=[]

        self.board.append([' ']*20)
        for y in range(1,14):
            row=[]
            for x in range(20):
                c='*'
                if random()<0.4:
                    self.bg.fill(self.BLACK,(x*self.NUGGET_SIZE+self.BOARD_LEFT,y*self.NUGGET_SIZE+self.BOARD_TOP,self.NUGGET_SIZE,self.NUGGET_SIZE))
                    c=' '
                    if y>2:
                        c='G'
                        nugg=self.nuggets[0 if random()<0.5 else 1] 
                        self.bg.blit(nugg,(x*self.NUGGET_SIZE+self.BOARD_LEFT,y*self.NUGGET_SIZE+self.BOARD_TOP))
                row.append(c)
            self.board.append(row)

# add title
        self.bg.blit(title,(self.BOARD_LEFT,self.BOARD_LEFT))

        self.screen.blit(self.bg,(0,0))

#        font = pygame.font.Font(None, 48)
#        text = font.render("GOLD:", 1, (255,255,255))
#        self.screen.blit(text,(20,548))

        pygame.display.flip()
        self.board.append([' ']*20)
       
    def print_board(self):
        for row in self.board:
            print ' '.join(row)

    def cycle(self):
        deltat=self.clock.tick(self.FRAMES_PER_SECOND)
        tx=self.miner.x
        ty=self.miner.y
        self.miner_group.clear(self.screen,self.bg)
        self.explosion_group.clear(self.screen,self.bg)
 
        pressedspace=False
        for event in pygame.event.get():
            #print event
            if event.type == KEYDOWN:
                if event.key in (K_RIGHT,K_LEFT,K_UP,K_DOWN):
                    self.pressedkey= event.key
                elif event.key == K_SPACE:
                   # print "SPACE!"
                    pressedspace = True
            elif event.type == KEYUP:
                if event.key in (K_RIGHT,K_LEFT,K_UP,K_DOWN):
                    if self.pressedkey == event.key:
                        self.pressedkey = None
                #elif event.key == K_SPACE:
                    #pressedspace = False
                    #print "NOSPACE!"

        if self.explosion.exploding:
            self.explosion.update(deltat)
            self.explosion_group.update(deltat)
            self.explosion_group.draw(self.screen)

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
                    print "(%d,%d)->(%d,%d) Boom! %d bombs left." % (self.miner.x,self.miner.y,bx,by,self.bombs)
                    self.board[by][bx]=' '
                    self.bg.fill(BLACK,(bx*self.NUGGET_SIZE+self.BOARD_LEFT,by*self.NUGGET_SIZE+self.BOARD_TOP,self.NUGGET_SIZE,self.NUGGET_SIZE))
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
                    self.bg.fill(BLACK,(self.miner.x*self.NUGGET_SIZE+self.BOARD_LEFT,self.miner.y*self.NUGGET_SIZE+self.BOARD_TOP,self.NUGGET_SIZE,self.NUGGET_SIZE))
                self.update_score()

            self.miner.update_move()
            self.miner_group.update(deltat)
            self.miner_group.draw(self.screen)

        pygame.display.flip()


    def update_score(self):
        font = pygame.font.Font(None, 48)
        sctext="%04d" % self.gold
        sz=font.size('0')
        fsx=sz[0]*5
        fsy=sz[1]
        pygame.draw.rect(self.screen,BLACK,(140,548,fsx,fsy),0)
        text = font.render(sctext, 1, (255,255,255))
        self.screen.blit(text,(140,548))

