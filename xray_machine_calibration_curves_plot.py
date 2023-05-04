from analysis import plotting_calibration, analysis , analysis_utils
from matplotlib.backends.backend_pdf import PdfPages
import os
rootdir = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':
    global PdfPages  
    conf = analysis_utils.open_yaml_file(file ="Xray_irradiation_conf.yaml",directory =rootdir)
    test_directory = conf['Tests']['test_directory'] 
    pdf_file = 'output_data/CalibrationCurve_Bonn.pdf'
    #Filters list
    _filtersList = conf['Tests']["filters"]
    _depthList = conf['Tests']["depth"]
    _currentList = conf['Tests']["current"]
    #Diodes list
    dictionary = dict(conf['Tests']['photodiodes'])
    _diodesList = list(dictionary.keys())
   
   #Get conversion factor 
    A_array =[dictionary[i] for i in ["A"] if i in dictionary]
    B_array =[dictionary[i] for i in ["B"] if i in dictionary]
    C_array =[dictionary[i] for i in ["C"] if i in dictionary]
    _A_factor  =   A_array[0]["factor"]
    _B_factor  =   B_array[0]["factor"]
    _C_factor  =   C_array[0]["factor"]
    tests = conf['Tests']["filters"]#["without_Al_filter", "with_Al_filter","V"]
    depth = conf['Tests']["depth"] #["3cm", "5cm", "8cm", "51cm", "60cm"]
    currents =conf['Tests']["current"]#["10mA", "20mA", "30mA", "40mA"]
    voltages = conf['Tests']["voltage"]#["30kV","40kV"]
    beamspot_filters = ["without_Al_filter", "V", "Zr"]
    depth_filters = ["3cm", "8cm", "51cm", "60cm"]

    PdfPages = PdfPages(pdf_file)
    p =plotting_calibration.PlottingCalibration()
    p.diode_calibration(PdfPages=PdfPages, directory=test_directory, tests=["A","B","C"])
    p.IV_test(PdfPages=PdfPages, directory=test_directory, tests=["A","B","C"])
    p.power_2d(PdfPages=PdfPages, directory=test_directory, V_limit=50, I_limit=50)
    p.calibration_temperature(tests=["A"],directory=test_directory, PdfPages=PdfPages)
    
    p.opening_angle(directory = test_directory, tests=tests[0:2],PdfPages=PdfPages)
    p.opening_angle_cone(directory = test_directory, tests=tests[0:2],PdfPages=PdfPages)
    p.dose_depth(directory=test_directory, tests=tests[0:2], PdfPages=PdfPages, factor = _B_factor)
    p.dose_current(stdev=0.04, PdfPages=PdfPages, directory=test_directory, tests=tests[0:2], depths= depth[0:3], factor = _C_factor, table=True, voltages=voltages)
    p.dose_drop( PdfPages=PdfPages,tests = tests[1:2], directory=test_directory,depth= depth[0:3], voltages=voltages,factor = _C_factor)
    p.dose_voltage(PdfPages=PdfPages, directory=test_directory ,tests=tests[0:1], kafe_Fit=False, table=True, currents = currents[:-1],factor = _C_factor) 
    p.Plot_Beam_profile_3d(directory=test_directory, PdfPages=PdfPages, depth=depth_filters, filters = beamspot_filters, factor = _A_factor)  #diode A
    p.Plot_Beam_profile_2d(directory=test_directory, PdfPages=PdfPages, depth=depth_filters, filters = beamspot_filters, factor = _A_factor)  #diode A
    p.plot_beamspot(directory= test_directory, filters = beamspot_filters[0:1], depth =["60cm"], PdfPages=PdfPages, factor = _B_factor)
    p.close(PdfPages=PdfPages)
    print("All the results are saved in the directory %s" %(test_directory))
    print ("The whole plots are saved into the  file %s"%(pdf_file))
