import pygame as pg
from random import uniform

class Button:
    def __init__(self,center,width,height,symbols,color,rollOverColor,displaySquare):
        self.center=center
        self.posistion=(round(self.center[0]-width/2),round(self.center[1]-height/2))
        self.width=width
        self.height=height
        self.displaySquare=displaySquare
        for symbol in symbols:
            for point in symbol:
                point[0]+=center[0]
                point[1]+=center[1]
        self.symbols=symbols

        self.widthChangeOnHover=25
        self.heightChangeOnHover=25

        self.color=color
        self.rollOverColor=rollOverColor
        self.points=[(self.posistion[0],self.posistion[1]),(self.posistion[0]+width,self.posistion[1]),(self.posistion[0]+width,self.posistion[1]+height),(self.posistion[0],self.posistion[1]+height)]
        self.wasPressed=False

    def displayAndGetClicked(self,mousePos,mousePressed,gameDisplay):
        self.wasPressed=False
        mouseIsOnButton=False
        if mousePos[0]>self.posistion[0] and mousePos[0]<(self.posistion[0]+self.width):
            if mousePos[1]>self.posistion[1] and mousePos[1]<(self.posistion[1]+self.height):
                mouseIsOnButton=True

        #square display
        if self.displaySquare:
            if mouseIsOnButton:
                width=self.width+self.widthChangeOnHover
                height=self.height+self.heightChangeOnHover
                points=[(self.center[0]-width/2,self.center[1]-height/2),(self.center[0]-width/2,self.center[1]+height/2),(self.center[0]+width/2,self.center[1]+height/2),(self.center[0]+width/2,self.center[1]-height/2)]
                pg.draw.aalines(gameDisplay,self.rollOverColor,True,points)

            else:
                pg.draw.aalines(gameDisplay,self.color,True,self.points)
        
        #symbols display
        if mouseIsOnButton:
            for symbol in self.symbols:
                    pg.draw.aalines(gameDisplay,self.rollOverColor,True,symbol)
        else:
            for symbol in self.symbols:
                pg.draw.aalines(gameDisplay,self.color,True,symbol)

        
        if mouseIsOnButton and mousePressed[0]:
            self.wasPressed=True
        return(mouseIsOnButton)


class TextBox:
    def __init__(self,text,color,center,characterWidth):
        self.alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',' ','1','2','3','4','5','6','7','8','9','0']
        #blocky font
        #self.font={'A': [[[0, 4], [1, 0]], [[1, 0], [2, 4]]], 'B': [[[0, 0], [2, 1]], [[2, 1], [0, 2]], [[0, 2], [2, 3]], [[2, 3], [0, 4]]], 'C': [[[2, 0], [0, 0]], [[0, 0], [0, 4]], [[0, 4], [2, 4]]], 'D': [[[0, 0], [2, 2]], [[2, 2], [0, 4]]], 'E': [[[2, 0], [0, 0]], [[2, 2], [0, 2]], [[2, 4], [0, 4]]], 'F': [[[0, 4], [0, 0]], [[0, 0], [2, 0]], [[0, 2], [2, 2]]], 'G': [[[2, 0], [0, 0]], [[0, 4],[2, 4]], [[2, 4], [2, 2]], [[2, 2], [1, 2]]], 'H': [[[0, 0], [0, 4]], [[0, 2], [2, 2]], [[2, 0], [2, 4]]], 'I': [[[0, 0], [2, 0]], [[1, 0], [1, 4]], [[0, 4], [2, 4]]], 'J': [[[2, 0], [2, 4]], [[2, 4], [0, 4]], [[0, 4], [0, 3]]], 'K': [[[2, 0], [0, 2]], [[0, 2], [2, 4]], [[0, 0], [0, 4]]], 'L': [[[0, 0], [0, 4]], [[0, 4], [2, 4]]], 'M': [[[0, 4], [0, 0]], [[0, 0], [1, 1]], [[1, 1], [2, 0]], [[2, 0], [2, 4]]], 'N': [[[0, 4], [0, 0]], [[0, 0], [2, 4]], [[2, 4], [2, 0]]], 'O': [[[0, 0], [2, 0]], [[2, 0], [2, 4]], [[2, 4], [0, 4]]], 'P': [[[0, 0], [2, 1]], [[2, 1], [0, 2]], [[0, 0], [0, 4]]], 'Q': [[[0, 4], [0, 0]], [[0, 0], [2, 0]], [[2, 0], [2, 4]], [[2, 4], [0, 4]], [[1, 3], [2, 4]]], 'R': [[[0, 0], [2, 1]], [[2, 1], [0, 2]], [[0, 2], [2, 4]]], 'S': [[[2, 0], [0, 1]], [[0, 1], [2, 2]], [[2, 2], [0, 4]]], 'T': [[[0, 0], [2, 0]], [[1, 0], [1, 4]]], 'U': [[[0, 0], [0, 4]], [[0, 4], [2, 4]], [[2, 4], [2, 0]]], 'V': [[[0, 0], [1,4]], [[1, 4], [2, 0]]], 'W': [[[0, 0], [0, 4]], [[0, 4], [1, 2]], [[1, 2], [2, 4]], [[2, 4], [2, 0]]], 'X': [[[0, 0], [2, 4]], [[2, 0], [0, 4]]], 'Y': [[[0, 0], [1, 2]], [[1, 2], [2, 0]], [[1, 2], [1, 4]]], 'Z': [[[0, 0], [2, 0]], [[2, 0], [0, 4]], [[0, 4], [2, 4]]], ' ': [], '1': [[[0, 1], [1, 0]], [[1, 0], [1, 4]]], '2': [[[0, 1], [1, 0]], [[1, 0], [2, 1]], [[2, 1], [0, 4]], [[0, 4], [2, 4]]]}
        
        #less blocky font
        self.font={'A': [[[0, 4], [1, 0]], [[1, 0], [2, 4]]], 'B': [[[0, 0], [2, 1]], [[2, 1], [0, 2]], [[0, 2], [2, 3]], [[2, 3], [0, 4]]], 'C': [[[2, 0], [0, 0]], [[0, 0], [0, 4]], [[0, 4], [2, 4]]], 'D': [[[0, 0], [2, 2]], [[2, 2], [0, 4]]], 'E': [[[2, 0], [0, 0]], [[2, 2], [0, 2]], [[2, 4], [0, 4]]], 'F': [[[0, 4], [0, 0]], [[0, 0], [2, 0]], [[0, 2], [2, 2]]], 'G': [[[2, 1], [1, 0]], [[1, 0], [0, 1]], [[0, 3], [1, 4]], [[1, 4], [2, 3]], [[2, 3], [2, 2]], [[2, 2], [1, 2]]], 'H': [[[0, 0], [0, 4]], [[0, 2], [2, 2]], [[2, 0], [2, 4]]], 'I': [[[0, 0], [2, 0]], [[1, 0], [1, 4]], [[0, 4], [2, 4]]], 'J': [[[2, 0], [2, 4]], [[2, 4], [0, 4]], [[0, 4], [0, 3]]], 'K': [[[2, 0], [0, 2]], [[0, 2], [2, 4]], [[0, 0], [0, 4]]], 'L': [[[0, 0], [0, 4]], [[0, 4], [2, 4]]], 'M': [[[0, 4], [0, 0]], [[0, 0], [1, 1]], [[1, 1], [2, 0]], [[2, 0], [2, 4]]], 'N': [[[0, 4], [0, 0]], [[0, 0], [2, 4]], [[2, 4], [2, 0]]], 'O': [[[0, 1], [1, 0]], [[1, 0], [2, 1]], [[0, 3], [1, 4]], [[1, 4], [2, 3]]], 'P': [[[0, 0], [2, 1]], [[2, 1], [0, 2]], [[0, 0], [0, 4]]], 'Q': [[[0, 4], [0, 0]], [[0, 0], [2, 0]], [[2, 0], [2, 4]], [[2, 4], [0, 4]], [[1, 3], [2, 4]]], 'R': [[[0, 0], [2, 1]], [[2, 1], [0, 2]], [[0, 2], [2, 4]]], 'S': [[[2, 0], [0, 1]], [[0, 1], [2, 2]], [[2, 2], [0, 4]]], 'T': [[[0, 0], [2, 0]], [[1, 0], [1, 4]]], 'U': [[[0, 0], [0, 4]], [[0, 4], [2, 4]], [[2, 4], [2, 0]]], 'V': [[[0, 0], [1,4]], [[1, 4], [2, 0]]], 'W': [[[0, 0], [0, 4]], [[0, 4], [1, 2]], [[1, 2], [2, 4]], [[2, 4], [2, 0]]], 'X': [[[0, 0], [2, 4]], [[2, 0], [0, 4]]], 'Y': [[[0, 0], [1, 2]], [[1, 2], [2, 0]], [[1, 2], [1, 4]]], 'Z': [[[0, 0], [2, 0]], [[2, 0], [0, 4]], [[0, 4], [2, 4]]], ' ': [], '1': [[[0, 1], [1, 0]], [[1, 0], [1, 4]]], '2': [[[0, 1], [1, 0]], [[1, 0], [2, 1]], [[2, 1], [0, 4]], [[0, 4], [2, 4]]],'3': [[[0, 0], [2, 1]], [[2, 1], [0, 2]], [[0, 2], [2, 3]], [[2, 3], [0, 4]]], '4': [[[0, 0], [0, 2]], [[0, 2], [2, 2]], [[2, 0], [2, 4]]], '5': [[[2, 0], [0, 0]], [[0, 1], [2, 2]], [[2, 2], [0, 4]]], '6': [[[2, 0], [0, 0]], [[0, 0], [0, 4]], [[0, 4], [2, 4]], [[2, 4], [2, 2]], [[2, 2], [0, 2]]], '7': [[[0, 0], [2, 0]], [[2, 0], [0, 4]]], '8': [[[2, 0], [0, 0]], [[0, 0], [0, 4]], [[0, 4], [2, 4]], [[2, 4], [2, 0]], [[0, 2], [2, 2]]], '9': [[[0, 0], [0, 2]], [[0, 2], [2, 2]], [[0, 0], [2, 0]], [[2, 0], [2, 4]]],'0':[[[0, 0], [2, 0]], [[2, 0], [2, 4]], [[2, 4], [0, 4]], [[0, 4], [0, 0]], [[0, 0], [2, 4]]]}
        
        self.characters={}
        self.fontSpacing=1
        self.fontWidth=2
        self.fontHeight=4
        self.characterWidth=characterWidth
        self.center=center
        self.text=text
        self.textLength=len(text)
        self.color=color
        self.allLinesActivated=False
        self.allLinesInactive=True

        #calculated in initalizeTextBox
        self.position=[0,0]
        self.letterScaling=0
        self.characterHeight=0
        self.boxWidth=0
        self.topLeftCorner=0
        self.boxWidth=0
        self.boxHeight=0
        self.characterSpacing=0
        #inactive is for lines not being displayed, active for lines that are being displayed
        self.lineListInactive=[]
        self.lineListActive=[]
    
    def initalizeTextBox(self):
        #scales letters to desired size
        self.letterScaling=self.characterWidth/self.fontWidth
        self.characterHeight=self.letterScaling*self.fontHeight
        self.characterSpacing=self.letterScaling*self.fontSpacing
        for letter in self.alphabet:
            character=[]
            for line in self.font[letter]:
                newLine=((self.letterScaling*line[0][0],self.letterScaling*line[0][1]),(self.letterScaling*line[1][0],self.letterScaling*line[1][1]))
                character.append(newLine)
            self.characters[letter]=character

        
        #text box dimensions
        self.boxWidth=self.textLength*(self.characterWidth+self.characterSpacing)
        self.boxHeight=self.characterHeight

        #calculates posisiton of text box (top left corner)
        positionX=self.center[0]-self.boxWidth/2
        positionY=self.center[1]-self.boxHeight/2
        self.posisiton=[positionX,positionY]

        #creates lineList
        for i in range(0,self.textLength):
            letter=self.text[i]
            letterLines=self.characters[letter]
            for line in letterLines:
                offsetX=self.posisiton[0]+i*(self.characterWidth+self.characterSpacing)
                offsetY=self.posisiton[1]
                displayLine=[[line[0][0]+offsetX,line[0][1]+offsetY],[line[1][0]+offsetX,line[1][1]+offsetY]]
                self.lineListInactive.append(displayLine)
    
    def changeText(self,text,DisplayAll=False):
        #display all sets all line to active as soon as text is changed
        self.allLinesActivated=DisplayAll
        self.allLinesInactive=not DisplayAll
        self.text=text
        self.textLength=len(text)
        #needs to be recalculated because potenntial changes to text length
        self.boxWidth=self.textLength*(self.characterWidth+self.characterSpacing)

        #calculates posisiton of text box (top left corner)
        positionX=self.center[0]-self.boxWidth/2
        positionY=self.center[1]-self.boxHeight/2
        self.posisiton=[positionX,positionY]
        
        self.lineListInactive.clear()
        self.lineListActive.clear()

        #creates lineList
        for i in range(0,self.textLength):
            letter=self.text[i]
            letterLines=self.characters[letter]
            for line in letterLines:
                offsetX=self.posisiton[0]+i*(self.characterWidth+self.characterSpacing)
                offsetY=self.posisiton[1]
                displayLine=[[line[0][0]+offsetX,line[0][1]+offsetY],[line[1][0]+offsetX,line[1][1]+offsetY]]

                if DisplayAll:
                    self.lineListActive.append(displayLine)
                else:
                    self.lineListInactive.append(displayLine)
    
    def moveText(self,traslation):
        for line in self.lineListActive:
            line[0][0]+=traslation[0]
            line[0][1]+=traslation[1]
            line[1][0]+=traslation[0]
            line[1][1]+=traslation[1]
        
        for line in self.lineListInactive:
            line[0][0]+=traslation[0]
            line[0][1]+=traslation[1]
            line[1][0]+=traslation[0]
            line[1][1]+=traslation[1]
            
    def displayActiveLines(self,gameDisplay):
        for line in self.lineListActive:
            pg.draw.aaline(gameDisplay,self.color,line[0],line[1])

    #will scramble the order of both lists
    def activateRandomLine(self):
        self.allLinesInactive=False
        randomIndex=int(round(uniform(0,len(self.lineListInactive)-1)))
        lineToActivate=self.lineListInactive.pop(randomIndex)
        self.lineListActive.append(lineToActivate)
        if len(self.lineListInactive)==0:
            self.allLinesActivated=True
        else:
            self.allLinesActivated=False
    
    def deactivateRandomLine(self):
        self.allLinesActivated=False
        randomIndex=int(round(uniform(0,len(self.lineListActive)-1)))
        lineToDeactivate=self.lineListActive.pop(randomIndex)
        self.lineListInactive.append(lineToDeactivate)

        if len(self.lineListActive)==0:
            self.allLinesInactive=True
        else:
            self.allLinesInactive=False

