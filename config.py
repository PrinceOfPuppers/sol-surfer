import tkinter
import numpy as np
from math import pi,inf
class Config:
    def __init__(self):
        self.fps=60
        self.gravConst=5
        self.numStars=30
        self.starRadius=3
        self.starWidth=1
        self.starColor=(150,150,150)
        #starting data for all the bodies, player is 0th index
        #masses will be sorted by radius (except for player which will be index 0)

        #to spawn another object, just add its radius, posistion and velocity to the list
        #if you dont want to spawn a particular type, just set its pos to inf and it'll desapawn on startup (an example is at end of lists)

        #self.initalPos=[0,1000,-inf,inf,inf,inf,inf,inf,inf,inf]

        #self.initalPos=[0,1000,-1000,1000j,-1000j,2000,-2000,2000j,-2000j,inf]
        #self.initalVels=[0,5j,-5j,-5,5,1j,-1j,-1,1,inf]
        #self.radii=[25,300,300,300,300,100,100,100,100,inf]

        self.initalPos=[-1000j,0,3000j,3800j,inf,inf,inf,inf,inf,inf]
        self.initalVels=[8,0,-6,-12,inf,inf,inf,inf,inf,inf]
        self.radii=[25,500,300,80,300,100,100,100,100,inf]

        self.masses=[]
        for i in range(0,len(self.radii)):
            self.masses.append(pi*self.radii[i]**2)
        
        self.colors=[np.array([255,255,255]),#white
            np.array([250, 182, 88]),#yellow orange
            np.array([243, 106, 83]),#red orange
            np.array([237, 96, 126]),#pink
            np.array([112, 137, 234]),#blue
            np.array([225, 251, 255]),#blue white
            np.array([242, 132, 74]),#orange 
            np.array([179, 101, 227]),#magenta
            np.array([127, 207, 224]),#cyan
            np.array([154, 143, 134]),#grey

            np.array([129, 221, 134])#lime green
        ]

        self.secondColors=[np.array([255,255,255]),#white
            np.array([246,238,225]),#off white 
            np.array([255,255,255]),#white
            np.array([249, 169, 187]),#light pink
            np.array([40, 125, 117]),#dark green
            np.array([162, 223, 233]),#blue grey
            np.array([255,255,255]),#white
            np.array([216, 156, 243]),#light magenta
            np.array([83, 182, 98]),#grass green
            np.array([99, 103, 107]),#dark grey

            np.array([199, 248, 189]),#light green
        ]


        self.featureTypes=["player",
            "star",
            "martian",
            "clouds",
            "terran",
            "craters",
            "martian",
            "clouds",
            "terran",
            "craters",

            "clouds"]
        


        self.playerTurnSpeed=0.05
        self.playerBoostForce=30000
        self.playerMomentInertia=0.5*pi*self.radii[0]**4
        self.playerMaxImpulse=10000
        self.playerMaxLandingAngle=pi/2

        self.playerAsset=np.array([[-10.0, 15], [0.0, -15.0], [10.0, 15], [0.0, 5.0]])

        self.boosterAnimation=np.array([
            [[0.0, 10.0], [-5.0, 15.0], [0.0, 30.0], [5.0, 15.0]], 
            [[0.0, 10.0], [-5.0, 15.0], [0.0, 35.0], [5.0, 15.0]], 
            [[0.0, 10.0], [-5.0, 15.0], [0.0, 40.0], [5.0, 15.0]], 
            [[0.0, 10.0], [-5.0, 15.0], [0.0, 45.0], [5.0, 15.0]],
            [[0.0, 10.0], [-5.0, 15.0], [0.0, 40.0], [5.0, 15.0]],
            [[0.0, 10.0], [-5.0, 15.0], [0.0, 35.0], [5.0, 15.0]]
            ])


        self.featureDict={
            "player" : ((())),
            "craters" : (((-0.5, -0.2), (-0.2, -0.5), (0.1, -0.2), (-0.2, 0.1)), ((0.3, -0.5), (0.4, -0.6), (0.5, -0.5), (0.4, -0.4)), ((-0.6, 0.5), (-0.4, 0.3), (-0.2, 0.5), (-0.4, 0.7)), ((0.2, 0.3), (0.4, 0.1), (0.6, 0.3), (0.4, 0.5))),
            "clouds" : (((-0.7, 0.4), (-0.3, 0.3), (0.0, 0.4), (-0.3, 0.5)), ((-0.4, -0.1), (0.2, -0.3), (0.9, -0.1), (0.2, 0.1)), ((-0.6, -0.6), (-0.2, -0.7), (0.2, -0.6), (-0.2, -0.5))),
            "terran" : (((-0.5, -0.3), (-0.2, -0.8), (0.4, -0.7), (0.3, -0.2), (0.7, 0.4), (0.2, 0.7), (0.1, -0.1)), ((-0.6, 0.1), (-0.3, -0.1), (-0.1, 0.1), (-0.1, 0.6), (-0.3, 0.7), (-0.4, 0.3), (-0.7, 0.3))),
            "martian": (((0.0, -1.0), (-0.2, -0.975), (-0.3, -0.95), (-0.375, -0.925), (-0.475, -0.875), (-0.625, -0.775), (-0.375, -0.7), (-0.075, -0.8), (0.225, -0.6), (0.625, -0.775), (0.525, -0.85), (0.375, -0.925), (0.3, -0.95), (0.2, -0.975), (0.05, -1.0)), ((0.0, 1.0), (0.2, 0.975), (0.3, 0.95), (0.425, 0.9), (0.6, 0.8), (0.475, 0.7), (0.275, 0.775), (0.05, 0.6), (-0.15, 0.775), (-0.475, 0.65), (-0.675, 0.725), (-0.625, 0.775), (-0.475, 0.875), (-0.3, 0.95), (-0.2, 0.975))),
            "star" : (((0.0, -0.9), (-0.3, -0.3), (-0.9, 0.0), (-0.3, 0.3), (0.0, 0.9), (0.3, 0.3), (0.9, 0.0), (0.3, -0.3)),((0.0, -0.9), (-0.3, -0.3), (-0.9, 0.0), (-0.3, 0.3), (0.0, 0.9), (0.3, 0.3), (0.9, 0.0), (0.3, -0.3)))
        }



        self.screenZoomRate=0.1
        #margin is how far offscreen does somthing have to be before its not drawn
        self.screenMargin=100


        #screen dimensions and scaling
        root=tkinter.Tk()
        self.devScreenWidth=1500
        screenWidth=root.winfo_screenwidth()-100
        screenHeight=root.winfo_screenheight()-100
        self.screenSize=[screenWidth,screenHeight]

        self.widthRatio=screenWidth/self.devScreenWidth
        self.scaleToScreenWidth()

    def scaleToScreenWidth(self):
        pass