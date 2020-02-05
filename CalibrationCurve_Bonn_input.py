from analysis import plotting_Calibration
from analysis import analysis
from analysis import gui
from matplotlib.backends.backend_pdf import PdfPages

if __name__ == '__main__':
    global PdfPages
    Directory = "Calibration_Curves/"
    pdf_file = 'output_data/CalibrationCurve_Bonn.pdf'
    tests = ["without_Al_Filter", "with_Al_Filter"]
    depth = ["3cm", "5cm", "8cm", "51cm"]
    PdfPages = PdfPages(pdf_file)
    filename = "/home/silab62/git/XrayMachine_Bonn/Calibration_Curves/without_Al_Filter/beamspot/60cm/beamspot_60cm.h5"
    p =plotting_Calibration.PlottingCalibration()
    g =gui.GraphicalInterface()
    
    g.Application()
    
    #p.opening_angle(Directory=Directory, tests=tests,PdfPages=PdfPages)
   
   
   
   
   
    print("All the results are saved in the directory %s" %(Directory))
    print ("The whole plots are saved into the  file %s"%(pdf_file))
