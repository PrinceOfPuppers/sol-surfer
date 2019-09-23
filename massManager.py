import numpy as np
from math import sin,cos,pi,sqrt

from helperFuncs import rotateVecs,sortByRadius,cmplxCross,cmplxDot,angleUnsigned,sortById
from mass import Mass
from player import Player

class MassManager:
    def __init__(self,config,screen):
        self.gravConst=config.gravConst
        self.massList=[]
        self.inactiveMassList=[]
        #temp storage for distant object despawning
        self.massesToRemove=[]
        self.levels=config.levels
        self.initalizeBodies(config)

    def initalizeBodies(self,config):
        level=config.levels[0]
        for i in range(1,len(config.colors)):
            surfFeat=config.featureDict[config.featureTypes[i]]

            self.inactiveMassList.append(
                Mass(i,level["pos"][i],level["radii"][i],config.colors[i],config.secondColors[i],surfFeat,level["vels"][i])
            )
        plrSurfFeat=config.featureDict[config.featureTypes[0]]
        print(level["pos"][0],level["radii"][0])
        plr=Player(config,0,level["pos"][0],level["radii"][0],config.colors[0],config.secondColors[0],plrSurfFeat,level["vels"][0])
        self.inactiveMassList.append(plr)
        self.totalMasses=len(self.inactiveMassList)
        self.plr=plr
        

    def constructBodies(self,screen,levelNum):
        
        #removes all masses from masslist and adds them to inactive mass list
        for i in range(0,len(self.massList)):
            self.inactiveMassList.append(self.massList.pop(0))

        level=self.levels[levelNum]

        #adds all masses to mass list and calls their constructor to load the inital values
        #must be sorted so the correct stats go with the correct body
        self.inactiveMassList.sort(key=sortById)
        for i in range(0,self.totalMasses):
            self.massList.append(self.inactiveMassList.pop(0))
            self.massList[i].constructor(level["pos"][i],level["radii"][i],level["vels"][i])

        
        #sorts mass list by radius so they render in the smallest to biggest
        self.massList.sort(key=sortByRadius)

        #ensures player is always at front of list
        self.massList.remove(self.plr)
        self.massList.insert(0,self.plr)

        self.numActiveMasses=len(self.massList)
        
        self.overflowProtection(screen)

    
    def applyGravAndCheckCol(self,deltaT):
        for i in range(0,self.numActiveMasses):
            for j in range(i+1,self.numActiveMasses):
                #number of masses can change during this loop due to absorbtion
                if i>self.numActiveMasses-1 or j>self.numActiveMasses-1:
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
                            displacementMag=abs(displacement)
                            depth=mass2.radius-displacementMag

                            
                            if depth>0:
                                #point is in planet
                                
                                relVel=pointVel-mass2.vel
                                pointMomentum=self.plr.mass*relVel
                                relVelNorm=cmplxDot(unitVec,relVel)

                                if relVelNorm<0:
                                    #point is moving in 
                                    impulse=-pointMomentum   
                                    plrDirectionVec= cos(self.plr.rot)+sin(self.plr.rot)*1j

                                    if abs(impulse)>self.plr.maxImpulse or angleUnsigned(unitVec,plrDirectionVec)>self.plr.maxLandingAngle:
                                        self.absorb(self.plr,mass2)
                                    else:
                                        self.plr.applyImpulse(impulse)
                                        mass2.applyImpulse(-impulse)
                                    
                                self.plr.pos=mass2.pos+unitVec*mass2.radius-(point[0]+point[1]*1j)
                                break
                    
                    #all other collision
                    else:
                        #checks if masses should absorb eachother
                        if depth<-min(mass1.radius,mass2.radius):
                            self.absorb(mass1,mass2)


    
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
        self.inactiveMassList.append(eatee)
        self.numActiveMasses-=1
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
                mass.pos-=screen.pos
                if abs(mass.pos.real)>100000 or abs(mass.pos.imag)>100000:
                    self.massesToRemove.append(mass)
                    self.numActiveMasses-=1
        self.plr.pos-=screen.pos
        screen.pos=0
        for mass in self.massesToRemove:
            self.massList.remove(mass)
            self.inactiveMassList.append(mass)
            print("removing distant object")
        self.massesToRemove.clear()



    def handler(self,screen,tickNumber,deltaT):
        if tickNumber%5000==0:
            self.overflowProtection(screen)
        self.applyGravAndCheckCol(deltaT)
        for mass in self.massList:
            mass.handler(screen,deltaT,tickNumber)




