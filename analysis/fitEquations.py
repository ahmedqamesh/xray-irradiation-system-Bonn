
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import os
import yaml
from decimal import Decimal
import math
import logging
from logging.handlers import RotatingFileHandler
import verboselogs
import coloredlogs as cl

rootdir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(rootdir[:-8], "Xray_irradiation_conf.yaml")
nan = Decimal('nan')
logger = logging.getLogger("Fit Equations")
with open(filename, 'r') as ymlfile:
    conf = yaml.load(ymlfile, Loader=yaml.FullLoader)

def linear(x, m, c):
    return m * x + c
    
def inv_linear(y, m, c):
    return (y-c)/np.float(m)

def Inverse_square(x, a, b, c):
    return a / (x + b)**2 - c

def quadratic(x, a, b, c):
    return a*x**2+b*x+c

def opening_angle(depth=None, r=None, conf = conf,filter= "without"):
    #The function will return  radius if depth is given 
    #The function will return  height if r is given
    try:
        opening_angle = conf["FitFunctions"]["opening_angle"][filter] 
        if depth is not None:
            result = linear(depth,opening_angle["a"],opening_angle["b"])
        if r is not None:
            result = inv_linear(r,opening_angle["a"],opening_angle["b"])
    except Exception:
        logger.error('Test is not available')
        result =  nan
    return result

def dose_current(I=None, dose= None, depth ="3cm", filter= "without", voltage = "40kV", conf = conf):
    #The function will return  dose if I is given 
    #The function will return  current if d is given
    dose_current = conf["FitFunctions"]["dose_current"][filter][depth][voltage]
    if I is not None:
        result=linear(I,dose_current["a"],dose_current["b"])
    if dose is not None:
        result=inv_linear(dose,dose_current["a"],dose_current["b"])
    return result            

def dose_voltage(V=None, current ="10mA", filter= "without",  depth ="8cm", conf = conf):
    dose_voltage =conf["FitFunctions"]["dose_voltage"][filter][depth][current]
    #The function will return  dose if V is given 
    if filter == "without":
        result=quadratic(V,dose_voltage["a"],dose_voltage["b"],dose_voltage["c"])
    else:   print("Not yet")
    return result 

def dose_depth(depth = None, dose = None, filter = "without", conf = conf, current ="50mA",voltage = "40kV" ):
    try:
        dose_voltage =conf["FitFunctions"]["dose_depth"][filter][voltage][current]
        if depth is not None:
            result = Inverse_square(depth,dose_voltage["a"],dose_voltage["b"],dose_voltage["c"])
        if depth is None: 
            result = np.sqrt(dose_voltage["a"]*(dose+dose_voltage["c"])**(-1))-dose_voltage["b"]
    except Exception:
        logger.error('Test is not available')
        result =  nan
    return result
if __name__ == '__main__':
    r = opening_angle(depth = 60)
    h = opening_angle(r = 5)
    dC = dose_current(I = 40, filter = "without", depth ="3cm",voltage = "40kV")
    dose = dose_current(d = 11.4, filter = "without", depth ="3cm",voltage = "40kV")
    dV = dose_voltage(V = 30, filter = "without", depth ="8cm")
    dD = dose_depth(depth = 40, filter = "without")
    dD2 = dose_depth(dose = 0.522053934521467, filter = "without",current ="50mA",voltage = "40kV")
    print (r, h,dC,dV, dD, dose, dD2)