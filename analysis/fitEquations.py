
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import os
import yaml
rootdir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(rootdir[:-8], "Xray_irradiation_conf.yaml")
with open(filename, 'r') as ymlfile:
    conf = yaml.load(ymlfile, Loader=yaml.FullLoader)
dose_c = conf["FitFunctions"]["dose_current"]
c_array =[dose_c[i] for i in ["with"] if i in dose_c]

c = c_array[0]["3cm"]
print(c)
cv_array =[c[i] for i in ["30kV"] if i in c]
print(cv_array[0])

        

def linear(x, m, c):
    return m * x + c
    
def inv_linear(y, m, c):
    return (y-c)/np.float(m)

def Inverse_square(x, a, b, c):
    return a / (x + b)**2 - c

def quadratic(x, a, b, c):
    return a*x**2+b*x+c

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

def dose_current(I=None, d= None, depth ="3cm", filter= "without", voltage = "40kV"):
    #The function will return  dose if I is given 
    #The function will return  current if d is given
    if I is not None:
        if filter == "without":
            if depth == "3cm":
                if voltage == "40kV":
                    result=linear(I,0.29,-0.14)
                if voltage == "30kV":
                    result=linear(I,0.24,-0.12)
                             
            if depth == "5cm":
                if voltage == "40kV":
                   result=linear(I,0.22,-0.06)
                if voltage == "30kV":
                   result=linear(I,0.18,-0.09)
                
            if depth == "8cm":
                if voltage == "40kV":
                    result=linear(I,0.14,-0.05)
                if voltage == "30kV":
                    result=linear(I,0.11,-0.03)
                                        
        if filter == "Al":
            if depth == "3cm":
                if voltage == "40kV":
                   result=linear(I,0.08,0)
                if voltage == "30kV":
                   result=linear(I,0.06,-0.01)
                    
            if depth == "5cm":
                if voltage == "40kV":
                   result=linear(I,0.06,-0.02)
                if voltage == "30kV":
                   result=linear(I,0.05,0.0)
            
            if depth == "8cm":
                if voltage == "40kV":
                    result=linear(I,0.04,-0.01)
                if voltage == "30kV":
                    result=linear(I,0.03,-0.01)
                
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


def dose_voltage(V=None, d= None, current ="10A", filter= "without",  depth ="8cm"):
    #The function will return  dose if V is given 
    if filter == "without":
        if current == "10A":
            result=quadratic(V,-0.001,0.068,-0.404)

        if current == "20A":
            result=quadratic(V,-0.001,0.139,-0.919)
        
        if current == "30A":
            result=quadratic(V,-0.002,0.208,-1.423)
                            
        if current == "40A":
            result=quadratic(V,-0.002,0.279,-1.932)                            
        else: print("Not yet")  
    else:   print("Not yet")
        
    return result 

def dose_depth(h = None, filter = "without"):
    if h is not None:
        if filter == "without":
            result = Inverse_square(h,1391.77,6.20,0.13)
        
        if filter == "Al":
            result = Inverse_square(h,431.19,6.75,0.03)
    if h is None: 
        if filter == "without":
            R2 = 1 
            h2 = 2
            result = R2*((h2-6.75)/(h-6.75))**2
        if filter == "Al":
            R2 = 1 
            h2 = 2
            result = R2*((h-6.75)/(h2-6.75))**2
                    
    return result
if __name__ == '__main__':
    r = opening_angle(h = 60)
    h = opening_angle(r = 5)
    dC = dose_current(I = 40, filter = "Al", depth ="3cm")
    dose = dose_current(d = 15, filter = "Al", depth ="3cm")
    dV = dose_voltage(V = 30, filter = "without", depth ="8cm")
    dD = dose_depth(h = 30, filter = "without")
    print (r, h,dC,dV, dD, dose)