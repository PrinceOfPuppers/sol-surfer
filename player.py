
import pygame as pg
import numpy as np
from math import sin,cos,pi
from helperFuncs import rotateVecs,sortByRadius,cmplxCross,cmplxDot,angleUnsigned
from mass import Mass

class Player(Mass):
    def __init__(self,config,mass,initalPos,radius,color,secondColor,surfaceFeat,initalVel=0+0j,initalRot=0):
        super().__init__(mass,initalPos,radius,color,secondColor,surfaceFeat,initalVel)
        self.rot=initalRot
        self.rotMatrix=np.zeros((2,2),dtype=float)

        self.turnSpeed=config.playerTurnSpeed
        
        #used when player collides with surface
        self.rotVel=0
        self.momentOfInertia=config.playerMomentInertia
        
        self.boosting=False
        self.asset=config.playerAsset
        self.displayPoints=np.copy(config.playerAsset)
        self.displayPointsLen=len(self.displayPoints)

        #used by collision applicaiton
        self.collisionPoints=np.copy(config.playerAsset)
        self.maxImpulse=config.playerMaxImpulse
        self.maxLandingAngle=config.playerMaxLandingAngle

        self.boostForce=config.playerBoostForce
        self.animation=config.boosterAnimation
        self.animationRelPlayer=np.copy(config.boosterAnimation)
        self.numBoostFrames=len(self.animation)




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
        if self.boosting:
            frameNum=tickNumber%self.numBoostFrames
            rotateVecs(self.animation[frameNum],self.animationRelPlayer[frameNum],self.rot+pi/2,self.rotMatrix)
            for i in range(0,len(self.animation[frameNum])):
                self.animationRelPlayer[frameNum][i][0]/=screen.zoom
                self.animationRelPlayer[frameNum][i][1]/=screen.zoom
                self.animationRelPlayer[frameNum][i][0]+=plrPos[0]
                self.animationRelPlayer[frameNum][i][1]+=plrPos[1]
            pg.draw.aalines(screen.display,(255,0,0),True,self.animationRelPlayer[frameNum])



    def applyControls(self,deltaT,boosting,turn):

        #boosting is bool, turn is -1,0,1
        self.rot+=self.turnSpeed*turn
        self.rot+=self.rotVel

        #sets rotational velocity due to collision to zero if player is trying to turn
        if turn!=0:
            self.rotVel=0

        self.boosting=boosting
        if self.boosting:
            self.applyForce(self.boostForce*(cos(self.rot)+sin(self.rot)*1j),deltaT)
            
    def handler(self,screen,tickNumber):
        self.applyMotion()
        screen.pos=self.pos
        self.render(screen,tickNumber)
    
    def applyForceAndTorque(self,forceVec,forcePoint,deltaT):
        self.applyForce(forceVec,deltaT)

        #self.rotVel+=cmplxCross(forcePoint-self.pos,forceVec)*deltaT/self.momentOfInertia

