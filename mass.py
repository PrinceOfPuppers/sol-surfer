import pygame as pg
import pygame.gfxdraw as gfx
from math import sin,cos,pi,sqrt
from cmath import phase
import numpy as np
from helperFuncs import rotateVecs,sortByRadius,cmplxCross,cmplxDot,angleUnsigned


class Mass:
    def __init__(self,massId,initalPos,radius,color,secondColor,surfaceFeat,initalVel=0+0j):
        self.color=color
        self.secondColor=secondColor
        self.surfaceFeatAsset=surfaceFeat
        self.surfaceFeatDisplay=np.array(surfaceFeat[:][:])
        self.id=massId
        self.constructor(initalPos,radius,initalVel)
        
    def constructor(self,pos,radius,vel):
        self.pos=pos
        self.radius=radius
        self.vel=vel
        self.mass=pi*(radius**2)
    
    def applyForce(self,forceVec,deltaT):
        self.vel+=forceVec*deltaT/self.mass

    def applyImpulse(self,impulse):
        self.vel+=impulse/self.mass


    def applyMotion(self):
        self.pos+=self.vel
    
    def render(self,screen):
        point1=screen.convertCoords(self.pos)
        #checks if planet is off screen
        rad=self.radius/screen.zoom
        if (point1[0]+rad)<-screen.margin or (point1[1]+rad)<-screen.margin or (point1[0]-rad)>screen.size[0]+screen.margin or (point1[1]-rad)>screen.size[1]+screen.margin:
            pass
        else:
            gfx.filled_circle(screen.display,point1[0],point1[1],int(self.radius/screen.zoom),self.color)
            gfx.aacircle(screen.display,point1[0],point1[1],int(self.radius/screen.zoom),self.color)
            for i,feature in enumerate(self.surfaceFeatAsset):
                for j,point2 in enumerate(feature):
                    self.surfaceFeatDisplay[i][j][0]=point1[0]+point2[0]*rad
                    self.surfaceFeatDisplay[i][j][1]=point1[1]+point2[1]*rad
                gfx.filled_polygon(screen.display,self.surfaceFeatDisplay[i],self.secondColor)
                gfx.aapolygon(screen.display,self.surfaceFeatDisplay[i],self.secondColor)

    
    def handler(self,screen,deltaT,tickNumber):
        self.applyMotion()
        self.render(screen)
    




