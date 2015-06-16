from random import random
from random import randint
import pygame
from pygame.locals import *

from miner import Miner
from explosion import Explosion
from screen import GameScreen
from input_handler import InputHandler
from sounds import Sounds

class Game(object):
    TITLE = "Gold Rush!"
    WIDTH=680
    HEIGHT=600
    WAITING = 1
    PLAYING = 2
    FRAMES_PER_SECOND = 30

    board=[]

    def __init__(self):
        pygame.mixer.pre_init(44100,-16,2,2048)
        pygame.init()

        self.sounds=Sounds()


        self.input_handler = InputHandler()
        self.game_screen = GameScreen(self.TITLE,self.WIDTH,self.HEIGHT)
        self.miner=Miner(8,0)
        self.explosion=Explosion(-1,-1)
        self.game_screen.add_sprite(self.miner)
        self.game_screen.add_sprite(self.explosion)
        self.health = 100
         
        self.clock=pygame.time.Clock()
        self.state=self.WAITING
        self.game_screen.display_opening()

 
    def setup(self):
        self.gold=0
        self.charges=10
        self.cash=0
        self.health=100 
        self.board=[]
       
# top row of empty spaces
        self.board.append([' ']*20)
        self.board.append(['*']*20)
        for y in range(2,14):
            row=[]
            for x in range(20):
                c='*'
                if y>1 and random()<0.4:
                    c=' '
                    if random()<0.5:
                        c='0'
                    else:
                        c='1'
                row.append(c)
            self.board.append(row)
        self.miner.set_location(8,0)
        self.game_screen.setup()
        self.game_screen.set_board(self.board)
        self.game_screen.draw_board()



    def mainloop(self):
        deltat=self.clock.tick(self.FRAMES_PER_SECOND)
        running=True
        while running:
            self.input_handler.check()
            if self.input_handler.exit_action:
                running=False
            elif self.state == self.WAITING:
                if self.input_handler.key_press:
                    self.setup()
                    self.state=self.PLAYING
            else:
                self.game_screen.clear_sprites()
                if self.miner.can_move():
                    kpress=self.input_handler.arrow_press

                    if kpress:
                        dx=0
                        dy=0

                        if kpress == K_RIGHT:
                            dx=1
                        elif kpress == K_LEFT:
                            dx=-1
                        elif kpress == K_UP:
                            dy=-1
                        elif kpress == K_DOWN:
                            dy=1

                        if self.input_handler.space_press and (dx!=0 or dy!=0):
                            self.do_explosion(dx,dy)

                        tx=self.miner.x + dx
                        ty=self.miner.y + dy

                        if (dx!=0 or dy!=0) and (tx>=0 and tx<=19 and ty>=0 and ty<=13):
                            o=self.board[ty][tx]
                            if o in ' 01':
                                self.miner.set_location(tx,ty)
                                if o in '01':
                                    self.take_nugget(tx,ty)

                        elif (dy==-1 and tx==17 and ty==-1 and self.gold!=0):
                            self.cash_out()
                            if self.charges==0:
                                self.state=self.WAITING
                                self.input_handler.reset()
                                self.game_screen.display_gameover()



                    if self.miner.y>0:
                        self.health-=1
                        if self.health<0:
                            self.health=0
                        self.game_screen.display_health(self.health)
                    else:
                        self.health+=1
                        if self.health>100:
                            self.health=100
                        self.game_screen.display_health(self.health)
                

            self.game_screen.draw(deltat)
 
        pygame.quit()


    def do_explosion(self,dx,dy):
        bx=self.miner.x + dx
        by=self.miner.y + dy
        if bx>=0 and bx<20 and (by>0 or (by==0 and dy==1)) and by<14 and self.charges>0:

            self.explosion.explode(bx,by)

            self.charges-=1
            self.board[by][bx]=' '
            self.miner.add_delay(20)

            self.game_screen.clear_square(bx,by)
            self.game_screen.display_charges()
            self.sounds.play_boom()
            self.game_screen.display_charges(self.charges)

            for j in range(20):
                x=randint(0,19)
                y=randint(2,11)
                o=self.board[y][x]
                a=self.board[y-1][x]
                if o==' ' and a=='*':
                    self.board[y][x]='*'
                    self.game_screen.reset_square(x,y)

    def cash_out(self):
        self.cash+=self.gold*self.charges
        self.gold=0
        self.sounds.play_kaching()
        self.game_screen.display_gold(self.gold)
        self.game_screen.display_cash(self.cash)
        self.sounds.play_yeehaw()


    def take_nugget(self,tx,ty):
        self.board[ty][tx]=' '
        self.gold += 1
        self.sounds.play_bell()
        self.game_screen.clear_square(tx,ty)
        self.game_screen.display_gold(self.gold)
 
