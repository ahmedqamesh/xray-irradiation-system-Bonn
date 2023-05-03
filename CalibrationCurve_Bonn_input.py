from analysis import plotting_calibration
from analysis import analysis
#from analysis import gui
from matplotlib.backends.backend_pdf import PdfPages

if __name__ == '__main__':
    global PdfPages
    directory = "tests/"
    pdf_file = 'output_data/CalibrationCurve_Bonn.pdf'
    tests = ["without_Al_filter", "with_Al_filter"]
    depth = ["3cm", "5cm", "8cm", "51cm"]
    PdfPages = PdfPages(pdf_file)
    filename = "/home/silab62/git/XrayMachine_Bonn/tests/without_Al_Filter/beamspot/60cm/beamspot_60cm.h5"
    p =plotting_calibration.PlottingCalibration()
    #g =gui.GraphicalInterface()
    
    #g.Application()
    
    p.opening_angle(directory=directory, tests=tests,PdfPages=PdfPages)
    print("All the results are saved in the directory %s" %(directory))
    print ("The whole plots are saved into the  file %s"%(pdf_file))
