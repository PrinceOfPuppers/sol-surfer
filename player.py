
import pygame as pg
import numpy as np
from math import sin,cos,pi
from helperFuncs import rotateVecs,sortByRadius,cmplxCross,cmplxDot,angleUnsigned
from mass import Mass
class Booster:
    def __init__(self,config):
        self.boosting=False

        self.afterburner=False
        self.afterburnerMultiplier=config.afterburnerMultiplier
        self.maxAfterBurnerCharge=config.maxAfterBurnerCharge
        self.afterburnerCharge=config.maxAfterBurnerCharge

        self.color=(255,0,0)
        self.boostForce=config.playerBoostForce
        self.animation=config.boosterAnimation
        self.animationRelPlayer=np.copy(config.boosterAnimation)
        self.numBoostFrames=len(self.animation)

    def render(self,screen,plr,tickNumber,plrPos):
        frameNum=tickNumber%self.numBoostFrames
        rotateVecs(self.animation[frameNum],self.animationRelPlayer[frameNum],plr.rot+pi/2,plr.rotMatrix)
        for i in range(0,len(self.animation[frameNum])):
            self.animationRelPlayer[frameNum][i][0]/=screen.zoom
            self.animationRelPlayer[frameNum][i][1]/=screen.zoom
            self.animationRelPlayer[frameNum][i][0]+=plrPos[0]
            self.animationRelPlayer[frameNum][i][1]+=plrPos[1]
        pg.draw.aalines(screen.display,self.color,True,self.animationRelPlayer[frameNum])
    
    def boostHandler(self,plr,deltaT):
        if self.afterburner:
            self.afterburnerCharge-=1
            plr.applyForce(self.afterburnerMultiplier*self.boostForce*(cos(plr.rot)+sin(plr.rot)*1j),deltaT)
            if self.afterburnerCharge<=0:
                self.deactivateAfterburner()

        elif self.boosting:
            plr.applyForce(self.boostForce*(cos(plr.rot)+sin(plr.rot)*1j),deltaT)
        
        if self.afterburnerCharge<self.maxAfterBurnerCharge and not self.afterburner:
            self.afterburnerCharge+=1
        



    def activateAfterburner(self):
        self.afterburner=True
        self.color=(0,255,255)
    
    def deactivateAfterburner(self):
        self.afterburner=False
        self.color=(255,0,0)


class Player(Mass):
    def __init__(self,config,massId,initalPos,radius,color,secondColor,surfaceFeat,initalVel=0+0j):
        self.rot=0
        self.rotMatrix=np.zeros((2,2),dtype=float)

        self.turnSpeed=config.playerTurnSpeed
        
        #used when player collides with surface
        self.rotVel=0
        

        self.asset=config.playerAsset
        self.displayPoints=np.copy(config.playerAsset)
        self.displayPointsLen=len(self.displayPoints)

        #used by collision applicaiton
        self.collisionPoints=np.copy(config.playerAsset)
        self.maxImpulse=config.playerMaxImpulse
        self.maxLandingAngle=config.playerMaxLandingAngle
        self.booster=Booster(config)
        super().__init__(massId,initalPos,radius,color,secondColor,surfaceFeat,initalVel)

    def constructor(self,pos,radius,vel):
        self.pos=pos
        self.radius=radius
        self.vel=vel
        self.mass=pi*(radius**2)
        self.momentOfInertia=0.5*pi*self.radius**4
        self.rotVel=0
        self.rot=0

        self.booster.boosting=False
        self.booster.afterburner=False
        self.booster.afterburnerCharge=self.booster.maxAfterBurnerCharge


    def render(self,screen,tickNumber):
        #draws player asset
        rotateVecs(self.asset,self.displayPoints,self.rot+pi/2,self.rotMatrix)
        plrPos=screen.convertCoords(self.pos)
        for i in range(0,self.displayPointsLen):
            self.displayPoints[i][0]/=screen.zoom
            self.displayPoints[i][1]/=screen.zoom
            self.displayPoints[i][0]+=plrPos[0]
            self.displayPoints[i][1]+=plrPos[1]
        pg.draw.aalines(screen.display,self.color,True,self.displayPoints)

        #draws booster animation
        if self.booster.boosting or self.booster.afterburner:
            self.booster.render(screen,self,tickNumber,plrPos)





    def applyControls(self,deltaT,boosting,turn):

        #boosting is bool, turn is -1,0,1
        self.rot+=self.turnSpeed*turn
        self.rot+=self.rotVel

        #sets rotational velocity due to collision to zero if player is trying to turn
        if turn!=0:
            self.rotVel=0

        self.booster.boosting=boosting

            
    def handler(self,screen,deltaT,tickNumber):
        self.applyMotion()
        screen.pos=self.pos
        self.render(screen,tickNumber)
        self.booster.boostHandler(self,deltaT)
    
    def applyForceAndTorque(self,forceVec,forcePoint,deltaT):
        self.applyForce(forceVec,deltaT)

        #self.rotVel+=cmplxCross(forcePoint-self.pos,forceVec)*deltaT/self.momentOfInertia

