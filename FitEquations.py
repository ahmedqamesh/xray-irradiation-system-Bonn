from analysis import plottingCalibration, analysis , analysis_utils
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
def linear(x, m, c):
    return m * x + c
    
def inv_linear(y, m, c):
    return (y-c)/np.float(m)

def Inverse_square(x, a, b, c):
    return a / (x + b)**2 - c

def opening_angle(h=None, r=None):
    #The function will return  radius if h is given 
    #The function will return  height if r is given
    #r = hx+c
    #m=0.072+/-0.002
    #c=0.0451+/-0.030    
    if h is not None:
        result = linear(h,0.072,0.451)
    if r is not None:
        result = inv_linear(r,0.072,0.451)
    return result

def dose_current(I=None, d= None, depth ="3cm", filter= "without"):
    #The function will return  dose if I is given 
    #The function will return  current if d is given
    if I is not None:
        if filter == "without":
            if depth == "3cm":
                result=linear(I,0.29,-0.14)
            
            if depth == "5cm":
                print("Not yet")
                
            if depth == "8cm":
                result=linear(I,0.15,-0.01)
                    
        if filter == "Al":
            if depth == "3cm":
                result=linear(I,0.08,0)
                
            if depth == "5cm":
                print("Not yet")
            
            if depth == "8cm":
                result=linear(I,0.04,-0.05)
                
    if d is not None:
        if filter == "without":
            if depth == "3cm":
                result=inv_linear(d,0.29,-0.14)
            
            if depth == "5cm":
                print("Not yet")

            if depth == "8cm":
                result=inv_linear(d,0.15,-0.01)
                    
        if filter == "Al":
            if depth == "3cm":
                result=inv_linear(d,0.08,0)
    
            if depth == "5cm":
                print("Not yet")

            if depth == "8cm":
                result=inv_linear(d,0.04,-0.05)
    return result            
if __name__ == '__main__':
    r = opening_angle(h = 60)
    h = opening_angle(r = 5)
    d = dose_current(I = 40, filter = "Al", depth ="3cm")
    print (r, h, d)