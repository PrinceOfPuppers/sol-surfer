import numpy as np
from math import sin,cos,acos

def cmplxCross(a,b):
    return(a.real*b.imag-b.real*a.imag)

def cmplxDot(a,b):
    return(a.real*b.real+a.imag*b.imag)

def angleUnsigned(a,b):
    return( acos((cmplxDot(a,b))/(abs(a)*abs(b))) )
def sortByRadius(mass):
    return(mass.radius)

def rotateVecs(matrixToRotate,matrixToWrite,angle,rotMatrix):
    #this is the transpose of the usual rotation matrix because
    #vecs are represented as row vectors
    rotMatrix[0][0]=round(cos(angle),5)
    rotMatrix[0][1]=round(sin(angle),5)
    rotMatrix[1][0]=round((-1)*sin(angle),5)
    rotMatrix[1][1]=round(cos(angle),5)

    #note vectors are rendered as row vectors, hence the order is reversed
    np.matmul(matrixToRotate,rotMatrix,matrixToWrite)