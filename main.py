import pygame as pg
from config import Config
from massManager import MassManager
from random import random

class Screen:
    def __init__(self,config):
        self.size=config.screenSize
        self.display=pg.display.set_mode((config.screenSize[0], config.screenSize[1]))
        self.pos=0
        self.zoom=5
        self.margin=config.screenMargin
        self.zoomRate=config.screenZoomRate
        self.stars=[]
        self.starColor=config.starColor
        self.starRadius=config.starRadius
        self.starWidth=config.starWidth

        for i in range(0,config.numStars):
            self.stars.append((int(self.size[0]*random()),int(self.size[1]*random())))

    def convertCoords(self,worldComplex):
        screenTup=(int((worldComplex.real-self.pos.real)/self.zoom +self.size[0]/2),int((worldComplex.imag-self.pos.imag)/self.zoom+self.size[1]/2))
        return(screenTup)

    def renderStars(self):
        for star in self.stars:
            pg.draw.circle(self.display,self.starColor,star,self.starRadius,self.starWidth)

    
class GameManager: 
    def __init__(self,config):

        self.hasQuit=False
        self.tickNumber=0

        self.clock=pg.time.Clock()

        self.config=config
        self.fps=config.fps
        self.spf=1/config.fps


        
        self.massMgr=MassManager(config)
        self.plr=self.massMgr.massList[0]

        self.screen=Screen(config)
        self.screen.pos=self.plr.pos

    
    def applyControls(self):
        for event in pg.event.get():
            # checks if user has quit
            if event.type == pg.QUIT:
                self.hasQuit=True
            
            if event.type == pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    self.plr.booster.activateAfterburner()
            if event.type == pg.KEYUP:
                if event.key ==pg.K_SPACE:
                    self.plr.booster.deactivateAfterburner()
        
        plrRot=0
        plrBoost=False
        keys=pg.key.get_pressed()
        if keys[pg.K_d]:
            plrRot+=1
        if keys[pg.K_a]:
            plrRot+=-1
        if keys[pg.K_w]:
            plrBoost=True
        if keys[pg.K_q]:
            self.screen.zoom+=self.screen.zoomRate
        if keys[pg.K_e] and self.screen.zoom>0.5:
            self.screen.zoom-=self.screen.zoomRate
        self.plr.applyControls(self.spf,plrBoost,plrRot)
        
            

                
    def gameLoop(self):
        pg.init()
        pg.display.set_caption("Sol Surfer")
        while not self.hasQuit:

            self.applyControls()

            if self.tickNumber%100==0:
                print(self.clock)

            self.clock.tick_busy_loop(self.fps)

            self.screen.renderStars()
            self.massMgr.handler(self.screen,self.tickNumber,self.spf)

            pg.display.update()
            pg.Surface.fill(self.screen.display,(35, 34, 49))

            self.tickNumber+=1
            

if __name__=="__main__":
    cfg=Config()
    gameMgr=GameManager(cfg)
    gameMgr.gameLoop()