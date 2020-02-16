from analysis import plottingCalibration, analysis , analysis_utils
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
def linear(x, m, c):
    return m * x + c
    
def inv_linear(y, m, c):
    return (y-c)/np.float(m)

def opening_angle(h=None, r=None):
    #r = hx+c
    #m=0.072+/-0.002
    #c=0.0451+/-0.030    
    if h is not None:
        result = linear(h,0.072,0.451)
    if r is not None:
        result = inv_linear(r,0.072,0.451)
    return result
if __name__ == '__main__':
    r = opening_angle(h = 60)
    h = opening_angle(r = 5)
    print (r, h)