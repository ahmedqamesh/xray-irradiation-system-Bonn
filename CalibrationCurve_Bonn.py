from analysis import plotting
from analysis import analysis
from matplotlib.backends.backend_pdf import PdfPages
if __name__ == '__main__':
    global PdfPages
    Directory = "Calibration_Curves/"
    tests = ["without_Al_Filter", "with_Al_Filter"]
    depth = ["3cm", "5cm", "8cm", "51cm"]
    PdfPages = PdfPages('output_data/CalibrationCurve_Bonn' + '.pdf')
    filename = "/home/silab62/git/XrayMachine_Bonn/Calibration_Curves/without_Al_Filter/beamspot/60cm/beamspot_60cm.h5"
    p =plotting.Plotting()
    p.plot_beamspot(filename =Directory+"/without_Al_Filter/beamspot/60cm/beamspot_60cm.h5", PdfPages=PdfPages)
    p.dose_depth(tests=tests, Directory=Directory, PdfPages=PdfPages)
    p.power_2d(PdfPages=PdfPages, Directory=Directory, V_limit=50, I_limit=50)
    p.Plot_Beam_profile_3d(Directory=Directory, PdfPages=PdfPages, depth=["3cm", "8cm", "51cm","60cm"])
    p.Plot_Beam_profile_2d(Directory=Directory, PdfPages=PdfPages, depth=["3cm", "3cm_Vfilter", "3cm_Zrfilter", "3cm_collimator", "8cm", "60cm"])
    p.diode_calibration(PdfPages=PdfPages, Directory=Directory, diodes=["A","B","C"])
    p.calibration_temprature(data=Directory + "without_Al_Filter/temprature/temprature_dose.h5", Directory=Directory, PdfPages=PdfPages)
    p.opening_angle(Directory=Directory, tests=tests,PdfPages=PdfPages)
    p.dose_current(stdev=0.04, PdfPages=PdfPages, Directory=Directory, depth= ["3cm", "5cm", "8cm", "51cm"], table=True,Voltages=["40kV", "30kV"])
    p.dose_drop(stdev=0.04, PdfPages=PdfPages, Directory=Directory,depth= ["3cm", "5cm", "8cm", "51cm"])
    p.dose_voltage(PdfPages=PdfPages, Directory=Directory, test="without_Al_Filter", kafe_Fit=False, table=False)
    p.close(PdfPages=PdfPages)
