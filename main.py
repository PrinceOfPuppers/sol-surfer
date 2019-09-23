import pygame as pg
from random import random
from menu import Button,TextBox
from config import Config
from massManager import MassManager


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


        

 

        self.screen=Screen(config)
        self.massMgr=MassManager(config,self.screen)
        self.plr=self.massMgr.plr
        self.screen.pos=self.plr.pos

        self.levelNum=0

    
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

    def titleControls(self,enterHit):
        levelNumChanged=False
        for event in pg.event.get():
            # checks if user has quit
            if event.type == pg.QUIT:
                self.hasQuit=True
            
            if event.type == pg.KEYDOWN:
                if event.key==pg.K_d:
                    self.levelNum+=1
                    levelNumChanged=True
                elif event.key==pg.K_a:
                    self.levelNum-=1
                    levelNumChanged=True
                elif event.key==pg.K_RETURN or event.key==pg.K_SPACE:
                    enterHit=True
            
        self.levelNum%=len(self.massMgr.levels)
        return(enterHit,levelNumChanged)

    def titleScreenTransition(self):
        #plays game while zooming in the camera to the players positition 
        startZoom=self.config.zoomInStart
        zoomTime=self.config.zoomTime
        endZoom=self.config.initalGameZoom
        zoomRate=(endZoom-startZoom)/zoomTime

        titleTextVel=(0,-self.config.titleTextSpeedMultiplier*(self.titleText.center[1]+self.titleText.boxHeight)/zoomTime)
        levelTextVel=(0,self.config.titleTextSpeedMultiplier*(self.levelText.center[1]+self.levelText.boxHeight)/zoomTime)

        self.tickNumber=0
        self.screen.zoom=startZoom
        while not (self.hasQuit or zoomTime<self.tickNumber):
            #title movement and rendering 
            self.screen.zoom+=zoomRate
            self.titleText.moveText(titleTextVel)
            self.levelText.moveText(levelTextVel)

            if not self.titleText.allLinesActivated:
                self.titleText.activateRandomLine()
            
            self.titleText.displayActiveLines(self.screen.display)
            
            if not self.levelText.allLinesActivated:
                self.levelText.activateRandomLine()
            self.levelText.displayActiveLines(self.screen.display)


            #normal game loop
            self.applyControls()

            if self.tickNumber%100==0:
                print(self.clock)

            self.clock.tick_busy_loop(self.fps)

            self.screen.renderStars()
            self.massMgr.handler(self.screen,self.tickNumber,self.spf)

            pg.display.update()
            pg.Surface.fill(self.screen.display,(35, 34, 49))

            self.tickNumber+=1
            
    def titleScreen(self):
        enterHit=False
        self.titleText=TextBox("SOL SURFER",(255,255,255),(self.screen.size[0]/2,self.screen.size[1]/3),self.screen.size[0]/20)
        self.levelText=TextBox(self.massMgr.levels[self.levelNum]["name"],(255,255,255),(self.screen.size[0]/2,2*self.screen.size[1]/3),self.screen.size[0]/30)
        self.titleText.initalizeTextBox()
        self.levelText.initalizeTextBox()

        levelTextDelay=self.config.levelTextDelay
        while not (self.hasQuit or enterHit):
            enterHit,levelNumChanged=self.titleControls(enterHit)
            if levelNumChanged:
                self.levelText.changeText(self.massMgr.levels[self.levelNum]["name"])
            if not self.titleText.allLinesActivated:
                self.titleText.activateRandomLine()
            
            self.titleText.displayActiveLines(self.screen.display)

            if self.tickNumber>levelTextDelay:
                if not self.levelText.allLinesActivated:
                    self.levelText.activateRandomLine()
                self.levelText.displayActiveLines(self.screen.display)
            
            self.clock.tick_busy_loop(self.fps)

            self.screen.renderStars()

            pg.display.update()
            pg.Surface.fill(self.screen.display,(35, 34, 49))
            self.tickNumber+=1
        
    def main(self):
        pg.init()
        pg.display.set_caption("Sol Surfer")
        self.titleScreen()
        self.massMgr.constructBodies(self.screen,self.levelNum)
        self.titleScreenTransition()
        while not self.hasQuit:
            self.gameLoop()

if __name__=="__main__":
    cfg=Config()
    gameMgr=GameManager(cfg)
    gameMgr.main()