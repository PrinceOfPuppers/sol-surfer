import pygame as pg
import pygame.gfxdraw as gfx
from math import sin,cos,pi,sqrt
import numpy as np
from helperFuncs import rotateVecs,sortByRadius,cmplxCross,cmplxDot



class MassManager:
    def __init__(self,config):
        self.gravConst=config.gravConst
        self.massList=[]
        self.constructBodies(config)
        self.plr=self.massList[0]

        #temp storage for distant object despawning
        self.massesToRemove=[]
    
    def constructBodies(self,config):
        self.massList.clear()
        for i in range(1,len(config.masses)):
            surfFeat=config.featureDict[config.featureTypes[i]]

            self.massList.append(
                Mass(config.masses[i],config.initalPos[i],config.radii[i],config.colors[i],config.secondColors[i],surfFeat,config.initalVels[i])
            )
        self.massList.sort(key=sortByRadius)
        plrSurfFeat=config.featureDict[config.featureTypes[0]]
        plr=Player(config,config.masses[0],config.initalPos[0],config.radii[0],config.colors[0],config.secondColors[0],plrSurfFeat,config.initalVels[0])
        self.massList.insert(0,plr)
        self.numMasses=len(self.massList)


    
    def applyGravAndCheckCol(self,deltaT):
        for i in range(0,self.numMasses):
            for j in range(i+1,self.numMasses):
                #number of masses can change during this loop due to absorbtion
                if i>self.numMasses-1 or j>self.numMasses-1:
                    break
                mass1=self.massList[i]
                mass2=self.massList[j]
                
                displacement=mass2.pos-mass1.pos
                dist=abs(displacement)

                #applyGrav
                force=self.gravConst*mass1.mass*mass2.mass*displacement/(dist**3)
                mass1.applyForce(force,deltaT)
                mass2.applyForce(-force,deltaT)


                depth=dist-(mass1.radius+mass2.radius)
                #objectsCollided
                if depth<=0:

                    #checks if masses should absorb eachother
                    if depth<-min(mass1.radius,mass2.radius):
                        self.absorb(mass1,mass2)
                    
                    #player specific collision
                    if i==0:
                        #for player gravity must be applied first
                        force=self.gravConst*mass1.mass*mass2.mass*displacement/(dist**3)
                        mass1.applyForce(force,deltaT)
                        mass2.applyForce(-force,deltaT)


                        rotateVecs(self.plr.asset,self.plr.collisionPoints,self.plr.rot+pi/2,self.plr.rotMatrix)
                        for point in self.plr.collisionPoints:
                            pointCmplx=point[0]+point[1]*1j+self.plr.pos
                            pointVel=self.plr.vel
                            displacement=pointCmplx-mass2.pos
                            unitVec=displacement/abs(displacement)
                            unitTan=unitVec.real*1j-unitVec.imag
                            displacementMag=abs(displacement)
                            depth=mass2.radius-displacementMag

                            
                            if depth>=0:
                                #point is in planet

                                relVel=pointVel-mass2.vel
                                relVelUnit=relVel/abs(relVel)
                                pointMomentum=self.plr.mass*relVel
                                relVelNorm=cmplxDot(unitVec,relVel)


                                if relVelNorm<-0.01:
                                    #point is moving in 
                                    impulse1=-pointMomentum
                                    impulse2=100000*(-relVelUnit)*deltaT
                                    if abs(impulse1)>abs(impulse2):
                                        self.plr.applyImpulse(impulse2)
                                        mass2.applyImpulse(-impulse2)
                                    else:
                                        self.plr.applyImpulse(impulse1)
                                        mass2.applyImpulse(-impulse1)
                    #all other collision
                    else:
                        pass


    
    def absorb(self,mass1,mass2):
        if mass1.radius>mass2.radius:
            eater=mass1
            eatee=mass2
        else:
            eater=mass2
            eatee=mass1
        
        newMass=round(eater.mass+eatee.mass,5)
        newColor=(eater.color*eater.mass+eatee.color*eatee.mass)/newMass
        newSecondColor=(eater.secondColor*eater.mass+eatee.secondColor*eatee.mass)/newMass
        np.round(newColor)
        np.round(newSecondColor)
        newRadius=round(sqrt(newMass/pi),5)
        newVel=(eater.mass*eater.vel+eatee.mass*eatee.vel)/newMass
        newPos=(eater.mass*eater.pos+eatee.mass*eatee.pos)/newMass

        self.massList.remove(eatee)
        self.numMasses-=1
        eater.mass=newMass
        eater.color=newColor
        eater.secondColor=newSecondColor
        eater.radius=newRadius
        eater.vel=newVel
        eater.pos=newPos
        
    def overflowProtection(self,screen):
        print("overflow protection called")
        for mass in self.massList:
            if mass!=self.plr:
                mass.pos-=self.plr.pos
                if abs(mass.pos.real)>100000 or abs(mass.pos.imag)>100000:
                    self.massesToRemove.append(mass)
                    self.numMasses-=1
        self.plr.pos=0
        screen.pos=0
        for mass in self.massesToRemove:
            self.massList.remove(mass)
            print("removing distant object")
        self.massesToRemove.clear()



    def handler(self,screen,tickNumber,deltaT):
        if tickNumber%5000==0:
            self.overflowProtection(screen)
        self.applyGravAndCheckCol(deltaT)
        for mass in self.massList:
            mass.handler(screen,tickNumber)






class Mass:
    def __init__(self,mass,initalPos,radius,color,secondColor,surfaceFeat,initalVel=0+0j):
        self.mass=mass
        self.pos=initalPos
        self.vel=initalVel
        self.radius=radius
        self.color=color
        self.secondColor=secondColor
        self.surfaceFeatAsset=surfaceFeat
        self.surfaceFeatDisplay=np.array(surfaceFeat[:][:])
        
    
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

    
    def handler(self,screen,tickNumber):
        self.applyMotion()
        self.render(screen)
    



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
