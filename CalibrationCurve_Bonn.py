from analysis import plottingCalibration, analysis , analysis_utils
from matplotlib.backends.backend_pdf import PdfPages
import os
rootdir = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':
    global PdfPages  
    conf = analysis_utils.open_yaml_file(file ="BeamSpot_cfg.yaml",directory =rootdir)
    test_directory = conf['Tests']['test_directory']  
    pdf_file = 'output_data/CalibrationCurve_Bonn.pdf'
    tests = ["without_filter", "Al"]
    beamspot_depths = ["3cm", "8cm","51cm","60cm"]
    beamspot_filters = ["without_filter", "V", "Zr"]
    depth = ["3cm", "5cm", "8cm", "51cm"]
    currents =["10mA", "20mA", "30mA", "40mA"]
    voltages = ["30kV","40kV"]
    PdfPages = PdfPages(pdf_file)
    filename = "/tests/without_Al_Filter/beamspot/60cm/beamspot_60cm.h5"
    p =plottingCalibration.PlottingCalibration()
    #p.diode_calibration(PdfPages=PdfPages, directory=test_directory, tests=["A","B","C"])
    #p.IV_test(PdfPages=PdfPages, directory=test_directory, tests=["A","B","C"])
#   p.calibration_temperature(data="temperature_dose.h5", Directory=Directory, PdfPages=PdfPages)
    #p.opening_angle(directory = test_directory, tests=tests,PdfPages=PdfPages)
    #p.opening_angle_cone(directory = test_directory, tests=tests,PdfPages=PdfPages)
    #p.dose_depth(tests=tests, directory=test_directory, PdfPages=PdfPages)
    p.dose_current(stdev=0.04, PdfPages=PdfPages, directory=test_directory, tests=tests, depth= depth, table=True, voltages=voltages)
    #p.dose_drop(stdev=0.04, PdfPages=PdfPages, tests = tests, directory=test_directory,depth= depth,voltages=["40kV", "30kV"])
    #p.dose_voltage(PdfPages=PdfPages, directory=test_directory,currents = currents ,test=tests[0], kafe_Fit=True, table=False)
#     p.power_2d(PdfPages=PdfPages, Directory=Directory, V_limit=50, I_limit=50)
    #p.Plot_Beam_profile_3d(Directory=Directory, PdfPages=PdfPages, depth=beamspot_depths)
    #p.Plot_Beam_profile_2d(directory=test_directory, PdfPages=PdfPages, depth=beamspot_depths, filters = beamspot_filters)
#     p.plot_beamspot(Directory= Directory, depth =["60cm"], PdfPages=PdfPages)
    p.close(PdfPages=PdfPages)
    print("All the results are saved in the directory %s" %(test_directory))
    print ("The whole plots are saved into the  file %s"%(pdf_file))
