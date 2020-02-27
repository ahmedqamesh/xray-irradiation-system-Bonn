from __future__ import division
import numpy as np
from kafe import *
from kafe.function_library import quadratic_3par
from numpy import loadtxt, arange
import csv
from scipy.optimize import curve_fit
import tables as tb
from mpl_toolkits.mplot3d import Axes3D
import itertools
from mpl_toolkits.mplot3d import Axes3D  # @UnusedImport
from math import pi, cos, sin
from scipy.linalg import norm
import os
import seaborn as sns
sns.set(style="white", color_codes=True)
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from matplotlib.pyplot import *
import pylab as P
import matplotlib as mpl
import matplotlib.ticker as ticker
import matplotlib.transforms as mtransforms
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
from matplotlib.colors import LogNorm
from matplotlib.patches import Circle
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredDrawingArea
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import NullFormatter
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from analysis import analysis , logger
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.animation as animation
from graphics_Utils import mainWindow
from typing import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from matplotlib.figure import Figure

colors = ['black', 'red', '#006381', "blue", '#33D1FF', '#F5A9BC', 'grey', '#7e0044', 'orange', "maroon", 'green', "magenta", '#33D1FF', '#7e0044', "yellow"]
an = analysis.Analysis()
class PlottingCanvas(FigureCanvas):     

    def __init__(self,tests = None , test_file=None,name_prefix = None, plot_prefix =None):
        self.log = logger.setup_derived_logger('Plotting')
        self.log.info('Plotting initialized')
        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)
        #self.figure.clear()
        self.fig.add_subplot(111)
        self.ax = self.figure.add_subplot(111)
        if plot_prefix == "opening_angle":
            self.opening_angle(tests = tests , test_file=test_file)
        if plot_prefix =="opening_angle_cone":
            self.opening_angle_cone(tests = tests , test_file=test_file)
        
        if plot_prefix =="diode_calibration":
            self.diode_calibration(tests = tests , test_file=test_file)

        if plot_prefix =="IV_test":
            self.IV_test(tests = tests , test_file=test_file)
        
        if plot_prefix =="dose_current":
            self.dose_current(tests = tests , test_file=test_file, voltages = ["30kV", "40kV"])

        if plot_prefix =="dose_voltage":
            self.dose_voltage(tests = tests , test_file=test_file, currents = ["10mA", "20mA", "30mA", "40mA"])

        if plot_prefix =="dose_depth":
            self.dose_depth(tests = tests , test_file=test_file)
            
        if plot_prefix =="beamspot":
            self.Plot_Beam_profile_2d(tests = tests , test_file=test_file, depth = tests)
                                      
        self.draw()
    
               
    def diode_calibration(self, test_file=None, tests=[0]):
        '''
        The function plots the calibration results for the PN diodes
        Input Directory = Directory + diode_calibration/cern_calibration/
        diodes is an array of strings represents the diodes name A, B and C.
        '''
        self.log.info('Calibration results for the diodes')
        subdirectory = "diode_calibration/cern_calibration/"
        factor_row = []
        for test in tests:
            dep = []
            dose = []
            bkg = []
            current = []
            factor_test = mainWindow.MainWindow().get_calibration_factor(diode = test)
            with open(test_file, 'r')as data:
                reader = csv.reader(data)
                next(reader)
                for row in reader:
                    dep = np.append(dep, np.float(row[0]))  # Distance from the source
                    dose = np.append(dose, np.float(row[4]))  # Dose rate
                    current = np.append(current, np.float(row[2]))  # current
                    bkg = np.append(bkg, np.float(row[1]))
            self.ax.errorbar(dose, current, xerr=0.0, yerr=0.0, fmt='o', color=colors[tests.index(test)], markersize=3)  # plot points
            sig = [0.4 * current[k] for k in range(len(current))]
            popt, pcov = curve_fit(an.linear, dose, current, sigma=sig, absolute_sigma=True, maxfev=5000, p0=(1, 1))
            chisq = an.red_chisquare(np.array(current), an.linear(dose, *popt), np.array(sig), popt)
            line_fit_legend_entry = "Diode " + test + ':%.4fx+%.4f' % (popt[0], popt[1])
            self.ax.text(0.9, 0.4, 'Calibration factor =%s'%str(factor_test),
                    horizontalalignment='right', verticalalignment='top', transform=self.ax.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))
            self.ax.plot(dose, an.linear(dose, *popt), linestyle="--",
                color=colors[tests.index(test)], label=line_fit_legend_entry)
        self.ax.set_ylabel('Dose rate [$Mrad(sio_2)/hr$]')
        self.ax.set_xlabel(r'Current [$\mu$ A]')
        self.ax.set_title('(Diode calibration at %s and %s)' % ("40kV", "50mA"), fontsize=11)
        self.ax.grid(True)
        self.ax.legend()



    def IV_test(self, tests=["A"], test_file=False, h5=None):
        self.log.info('Plotting IV curves for diodes %s'%tests)
        subdirectory = "diode_calibration/"
        name_prefix = "IV_test_"
        conversion = 10**9
        for test in tests:
            if h5 is not None:
                with tb.open_file(test_file[:-4]+".h5", 'r') as in_file:
                    IV_results = in_file.root.IV_results[:]
                    v=IV_results['voltage']
                    mean = IV_results['mean_current']*conversion
                    std =IV_results['std_current']*conversion
                    self.ax.set_ylim(-3.,15)
                    self.ax.set_xlim(0,52)
                    self.ax.set_xscale('log')
                    print(hi)
            else:
                v = []
                mean = []
                std = []
                with open(test_file,'r')as data:
                    reader = csv.reader(data)
                    next(reader)
                    for row in reader:
                        v = np.append(v, float(row[2]))
                        mean = np.append(mean, float(row[1])*conversion)
                        std = np.append(std, float(row[3])*conversion)*1.04
                        self.ax.set_ylim(-1.5,0)
                        self.ax.set_xlim(-52,0)
            self.ax.errorbar(v,mean,yerr=std, fmt='o', color=colors[tests.index(test)], markersize=5, 
                        ecolor="black",label=("Diode %s " % test))
            self.ax.plot(v,mean,color='black')
        self.ax.set_xlabel("Reverse Voltage [V]")
        self.ax.set_ylabel("Current [nA]")
        self.ax.set_title('IV Curve')
        self.ax.grid(True)
        self.ax.legend(loc = "upper right")
        
                        
    def calibration_temperature(self, data=None, PdfPages=False, Directory=False):
        '''
        The function will plot the temperature effect on the diode calibration within 250 seconds of radiation, the data collected without any filter in the tube
        '''
        self.log.info('plot the temperature effect on the diode calibration within 250 seconds of radiation')
        subdirectory = 'without_Al_Filter/temperature/'
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax2 = ax.twinx()
        plot_lines = []
        with tb.open_file(Directory + subdirectory + data) as in_file:
            temprature_dose = in_file.root.temprature_dose[:]
            time = temprature_dose["time"]
            current = temprature_dose["current"] * 10 ** 6
            temperature = temprature_dose["temprature"]
        temp = ax2.errorbar(time, temperature, yerr=0.0, color=colors[0], fmt='-')
        curr = ax.errorbar(time[1:], current[1:], fmt='-', color=colors[1])
        ax2.set_ylabel('temperature[$^oC$]')
        ax.set_ylabel('Current [$\mu$ A]')
        ax.set_xlabel('Time [Seconds]')
        ax.grid(True)
        ax.set_ylim([0, 1])
        plot_lines.append([temp, curr])
        plt.legend(plot_lines[0], ["temperature", "mean current=%0.2f $\mu$ A" % np.mean(current)])
        plt.tight_layout()
        plt.savefig(Directory + subdirectory + 'temprature_dose_WithoutFilter.png')
        PdfPages.savefig()
        
    def opening_angle(self, test_file=None, tests=[0]):
        '''
        To get the estimated beam diameter relative to the depth
        '''
        self.log.info('Estimating the beam diameter relative to the depth')
        r = []
        h = []
        std = []
        with open(test_file, 'r')as data:
            reader = csv.reader(data)
            next(reader)
            for row in reader:
                h = np.append(h, float(row[0]))  # Distance from the source
                r = np.append(r, float(row[1]))  # Diameter of the beam
                std = np.append(std, float(row[2]))  # std on the reading of the beam diameter
        self.ax.errorbar(h, r, xerr=0.0, yerr=std, fmt='o', color='black', markersize=3, ecolor='black')  # plot points
        
        popt, pcov = curve_fit(an.linear, h, r, sigma=std, absolute_sigma=True, maxfev=5000, p0=(1, 1))
        chisq2 = an.red_chisquare(np.array(r), an.linear(h, *popt), np.array(std), popt)
        line_fit_legend_entry = 'line fit: mh + c\n m=$%.3f\pm%.3f$\nc=$%.3f\pm%.3f$' % (popt[0], np.absolute(pcov[0][0]) ** 0.5, popt[1], np.absolute(pcov[1][1]) ** 0.5)
        self.ax.plot(h, an.linear(h, *popt), '-', lw=1, label=line_fit_legend_entry, markersize=9)  # plot fitted function
        self.ax.set_title('Radius covered by beam spot %s (40 kV and 50 mA)' % (tests[0]), fontsize=12)
        self.ax.grid(True)
        self.ax.legend()
        self.ax.set_ylabel('Radius (r) [cm]')
        self.ax.set_xlabel('Distance from the  collimator holder(h) [cm]')

    def opening_angle_cone(self, test_file=None, tests=[0]):
        '''
        Draw the cone shape of the opening angle
        '''
        self.log.info('Estimating the beam diameter relative to the depth')
        for j in range(len(tests)):
            r = []
            h = []
            std = []
            with open(test_file, 'r')as data:
                reader = csv.reader(data)
                next(reader)
                for row in reader:
                    h = np.append(h, float(row[0]))  # Distance from the source
                    r = np.append(r, float(row[1]))  # Diameter of the beam
                    std = np.append(std, float(row[2]))  # std on the reading of the beam diameter
                    
            # Plot a cone represents the beam spot radius
            popt, pcov = curve_fit(an.linear, h, r, sigma=std, absolute_sigma=True, maxfev=5000, p0=(1, 1))
            h_space = np.linspace(h[0], h[-1], 50)
            r_space = an.linear(h_space, m=popt[0], c=popt[1])
            for i in range(len(r_space)):
                x, y = np.linspace(-r_space[i], r_space[i], 2), [h_space[i] for _ in np.arange(2)]
                self.ax.plot(x, y, linestyle="solid")
            self.ax.text(0.95, 0.90, "$\Theta^{rad}$ = %.3f$\pm$ %.3f\n $h_{0}$=%.3f$\pm$ %.3f" % (2 * popt[0], 2 * np.absolute(pcov[0][0]) ** 0.5, popt[1] / (popt[0]), np.absolute(pcov[1][1]) ** 0.5 / popt[0]),
                    horizontalalignment='right', verticalalignment='top', transform=self.ax.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
            self.ax.set_title('Diameter covered by beam spot %s' % (tests[j]), fontsize=12)
            self.ax.invert_yaxis()
            self.ax.set_xlabel('Diameter (d) [cm]')
            self.ax.set_ylabel('Height from the the collimator holder(h) [cm]')
            self.ax.grid(True)

    def dose_voltage(self, tests =None, test_file =None, currents = [0]):
        '''
        Effect of tube Voltage on the Dose, the available data is only without Filter
        '''
        self.log.info('Effect of tube Voltage at %s on the Dose' % (tests[0]))
        y1 = []
        x1 = []
        stdev = 0.06
        Dataset = []
        col_row = plt.cm.BuPu(np.linspace(0.3, 0.9, len(currents)))
        for i in range(len(currents)):
            x = []
            y = []
            Background = [0.00801e-06]
            Factor = [9.76]
            with open(test_file[:-7]+currents[i] + ".csv", 'r')as data1:
                reader = csv.reader(data1)
                next(reader)
                for row in reader:
                    x = np.append(x, float(row[0]))
                    y = np.append(y, (float(row[1]) - Background[0]) * Factor[0])
            x1.append(x)
            y1.append(y)
            sig = [stdev * y1[i][k] for k in range(len(y1[i]))]
            #Dataset = np.append(Dataset, build_dataset(x1[i], y1[i], yabserr=sig, title='I=%s' % currents[i], axis_labels=['Voltage (kV)', '$Dose rate [Mrad(sio_2)/hr]$']))
            popt, pcov = curve_fit(an.quadratic, x1[i], y1[i], sigma=sig, absolute_sigma=True, maxfev=5000, p0=(1, 1, 1))
            xfine = np.linspace(0., max(x1[i]), 100)
            self.ax.plot(xfine, an.quadratic(xfine, *popt), color=col_row[i])
            chisq = an.red_chisquare(np.array(y1[i]), an.quadratic(x1[i], *popt), np.array(sig), popt)
            self.ax.errorbar(x1[i], y1[i], yerr=sig, color=col_row[i], fmt='o',
                        label='I=%s' % (currents[i]))
            self.ax.text(0.95, 0.90, "y[$Mrad(sio_2)/hr$]= a$\mathrm{x}^2$ + bx+c",
                    horizontalalignment='right', verticalalignment='top', transform=self.ax.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
        self.ax.set_title('Effect of the tube voltage at ' + tests[0], fontsize=12)
        self.ax.set_ylabel('Dose rate [$Mrad(sio_2)/hr$]')
        self.ax.set_xlabel('Voltage (kV)')
        self.ax.grid(True)
        self.ax.legend()
        self.ax.ticklabel_format(useOffset=False)
        self.ax.set_xlim(xmin=5)
        self.ax.set_ylim(ymin=0)
           
    def dose_current(self, test_file=False, tests=[0], voltages=[0]):
        '''
        To get the calibration curves for each current
        For each Measurement you make you need to replace the numbers 0 in Background, Factor, .....by your measurement
        Background =  array of background estimated for each depth
         '''
        self.log.info('Get the calibration curves for each current')
        y1 = []
        x1 = []
        stdev = 0.06
        col_row = plt.cm.BuPu(np.linspace(0.3, 0.9, len(voltages)))
        for i in range(len(voltages)):
            x = []
            y = []
            Factor = [9.76]
            with open(test_file[:-7]+voltages[i] + ".csv", 'r')as data:  # Get Data for the first current
                reader = csv.reader(data)
                next(reader)
                for row in reader:
                    x = np.append(x, float(row[0]))
                    y = np.append(y, (float(row[1]) - float(row[2])) * Factor[0])
            x1.append(x)
            y1.append(y)
            sig = [stdev * y1[i][k] for k in range(len(y1[i]))]
            popt, pcov = curve_fit(an.linear, x1[i], y1[i], sigma=sig, absolute_sigma=True, maxfev=5000, p0=(1, 1))
            self.ax.errorbar(x1[i], y1[i], yerr=sig, color=col_row[i], fmt='o', label='V = %s' % (voltages[i]))
            xfine = np.linspace(0., max(x1[i]), 100)
            self.ax.plot(xfine, an.linear(xfine, *popt), color=col_row[i])           
            self.ax.text(0.95, 0.90, "y[$Mrad(sio_2)/hr$]= m$x$+c",
                    horizontalalignment='right', verticalalignment='top', transform=self.ax.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
            self.ax.ticklabel_format(useOffset=False)
            self.ax.set_title('Effect of the tube current at ' + tests[0], fontsize=12)
            self.ax.set_ylabel('Dose rate [$Mrad(sio_2)/hr$]')
            self.ax.set_xlabel('Tube current [mA]')
            self.ax.grid(True)
            self.ax.legend()
            self.ax.ticklabel_format(useOffset=False)
            self.ax.set_xlim(xmin=0)
            #self.ax.set_ylim(ymin=0)
            
    def dose_depth(self,tests = False , test_file=False, voltage="40 kV", current="50 mA", stdev=0.2, theta=0.16):
        '''
        Relation between the depth and  the Dose rate
        '''
        self.log.info('Relation between the depth and  the Dose rate')
        Factor = 9.81  # Calibration Factor
        height = []
        y1 = []
        b1 = []
        with open(test_file, 'r')as data:
            reader = csv.reader(data)
            next(reader)
            for row in reader:
                height = np.append(height, float(row[0]))  # Distance from the source
                y1 = np.append(y1, (float(row[1])))  # Dose rate
                b1 = np.append(b1, (float(row[2])))  # Background
        y1 = [y1[k] - b1[k] for k in range(len(y1))]  # Subtract Background
        y1 = [y1[k] * Factor for k in range(len(y1))]  # Multiply by the factor to get the dose rate
        sig = [stdev * y1[k] for k in range(len(y1))]
        popt1, pcov = curve_fit(an.Inverse_square, height, y1, sigma=sig, absolute_sigma=True, maxfev=500, p0=(300, 6, 0))
        # chisq1 = an.red_chisquare(np.array(y1), an.Inverse_square(np.array(height), *popt1), sig, popt1)
        self.ax.errorbar(height, y1, yerr=sig, color=colors[1], fmt='o', label=tests[0], markersize='4')
        xfine = np.linspace(height[0], height[-1], 100)  # define values to plot the function
        a, b, c = popt1[0], popt1[1], popt1[2]
        a_err, b_err, c_err = np.absolute(pcov[0][0]) ** 0.5, np.absolute(pcov[1][1]) ** 0.5, np.absolute(pcov[2][2]) ** 0.5
        self.ax.plot(xfine, an.Inverse_square(xfine, *popt1), colors[1], label='Fit parameters:\n a=%.2f$\pm$ %.2f\n b=%.2f$\pm$ %.2f\n c=%.2f$\pm$ %.2f\n' % (a, a_err, b, b_err, c, c_err))
        
        self.ax.text(0.9, 0.56, r'$R= \frac{a}{(h+b)^2}-c$',
                horizontalalignment='right', verticalalignment='top', transform=self.ax.transAxes,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))
        # print "The dose rate at %.2f cm depth is " %(45) + str(popt1[0]/(45+popt1[1])**2)+" Mrad/hr "+tests[i]
        self.ax.set_xlabel('Distance from the collimator holder(h) [cm]')
        self.ax.set_title('Dose rate vs distance %s at  (%s and %s)' % (tests[0], voltage, current), fontsize=11)
        self.ax.set_ylabel('Dose rate (R) [$Mrad(sio_2)/hr$]')
        self.ax.set_xlim([0, max(height) + 8])
        self.ax.grid(True)
        self.ax.legend(loc="upper right")
        self.ax.ticklabel_format(useOffset=False)
        cmap = plt.cm.get_cmap('viridis', 15)
        sc = self.ax.scatter(xfine, an.Inverse_square(xfine, *popt1), c=an.Inverse_square(xfine, a=a, b=b, c=c), cmap=cmap, s=50,)
        return a, b, c
    

    def dose_drop(self, Directory=False, PdfPages=False, stdev=0.06, depth=[0], Voltages=[0]):
        '''
        Dose drop after Al filter at two Voltages.
        '''
        self.log.info('Dose drop after filters')
        for i in range(len(depth)):
            fig = plt.figure()
            fig.add_subplot(111)
            ax = plt.gca()
            volt_row = []
            fit_para = []
            subdirectory = "dose_current/" + depth[i] + "/"
            for volt in Voltages:
                x1 = []
                y1 = []
                y2 = []
                bkg_y1 = []
                bkg_y2 = []
                Factor = []
                difference = []
                with open(Directory + subdirectory + volt + ".csv", 'r')as data:  # Get Data for the first Voltage
                    reader = csv.reader(data)
                    next(reader)
                    for row in reader:
                        x1 = np.append(x1, float(row[0]))  # Voltage
                        y1 = np.append(y1, (float(row[1]) - float(row[2])) * float(row[5]))  # Data with Al filter
                        y2 = np.append(y2, (float(row[3]) - float(row[4])) * float(row[5]))  # Data without Al filter
                        Factor = np.append(Factor, float(row[5]))
                        difference = np.append(difference, ((float(row[6])) * 100 / float(row[3])))  # (with-bkg) -(without-bkg)
                        
                ax.errorbar(x1, difference, yerr=0.0, color=colors[Voltages.index(volt)], fmt='--', label="%s" % volt)
            ax.set_title('Dose drop after Al filter at ' + depth[i], fontsize=12)
            ax.set_ylabel('Dose rate drop [%]')
            ax.set_xlabel('Tube current [mA]')
            ax.legend(prop={'size': 10})
            ax.grid(True)
            plt.savefig(Directory + subdirectory + 'dose_current_drop' + depth[i] + ".png", bbox_inches='tight')
            PdfPages.savefig()


                          
    def power_2d(self, Directory=False, PdfPages=False, size_I=50, size_V=60, V_limit=50, I_limit=50):
        '''
        Calculate the power in each point of I and V
        '''
        self.log.info("Calculate the power in each point of I and V")
        Power = np.zeros(shape=(size_I, size_V), dtype=float)
        power_max = np.zeros(shape=(size_I, size_V), dtype=float)
        p_max = V_limit * I_limit
        V = np.arange(0, size_V, 1)
        for i in range(size_I):
            for v in range(len(V)):
                Power[i, v] = i * v
                if (i * v == p_max):
                    power_max[i, v] = i * v
        fig, ax = plt.subplots()
        im = ax.imshow(Power, aspect='auto', origin='lower', interpolation='gaussian', cmap=plt.get_cmap('tab20c'))
        cb = fig.colorbar(im, ax=ax, fraction=0.0594)
        cb.set_label("Power [W]")
        ax.set_xlabel('Voltage [kV]')
        ax.set_ylabel('Current [mA]')
        ax.set_xlim([0, len(V)])
        ax.set_ylim([0, size_I])
        ax.set_title('Power of x-ray tube ', fontsize=12)
        ax.grid()
        ax2 = ax.twinx()
        x, y = np.where(power_max)
        ax2.axis('off')
        ax2.set_ylim([0, size_I])
        plt.axhline(y=I_limit, linewidth=2, color='#d62728', linestyle='solid')
        plt.axvline(x=V_limit, linewidth=2, color='#d62728', linestyle='solid')
        plt.tight_layout()
        plt.savefig(Directory + 'Power.png')
        PdfPages.savefig()

    def Plot_Beam_profile_2d(self, tests=[0], test_file =  False, filters = [0], depth=None):
        '''
        Make a 2d scan at specific depth
        '''
        self.log.info("Make a 2d scan at specific depth")
        Factor = 9.847  # diode A
        # Factor = 9.817  # diode B
        Background = 5.7 * 10 ** (-9)  # convert from A to nA
        binwidth = 1
        subdirectory = "beamspot/"
        filter = filters[0]
        for d in range(len(depth)):
            with tb.open_file(test_file, 'r') as in_file:
                beamspot = in_file.root.beamspot[:]
                beamspot = (beamspot - Background) * 1000000 * Factor
                mid_z, mid_x = np.int(beamspot.shape[0] / 2), np.int(beamspot.shape[1] / 2)
            # These are the exact radii as measured
            if (depth[d] == "3cm") or (depth[d] == "3cm_V") or (depth[d] == "3cm_Zr"):
                radius, r = r'$r=6.5 \pm 0.5$ mm', 1 * 6.5  # 1 mm step * radius
                # l,w= 13, 6.5 # in mm
            if depth[d] == "3cm_collimator":
                radius, r = '$r=3.75 \pm 0.05$ mm\n$r_{collimator}$ =6 mm', 1 * 3.75
            if depth[d] == "8cm":
                radius, r = r'$r=10 \pm 0.5$ mm', 1 * 10.5  # 1 mm step * radius
                l, w = 20, 11.5  # in mm
            if depth[d] == "51cm":
                radius, r = r'$r=40 \pm 0.5$ mm', 5 * 40  # 5 mm step * radius
            if depth[d] == "60cm":
                radius, r = r'$r=48 \pm 4$ mm', 48.4 / 5  # 5 mm step * radius
            cmap = plt.cm.get_cmap('viridis', 30)
            im = self.ax.imshow(beamspot, aspect='auto', interpolation='gaussian', cmap=cmap)  # ,extent=extent)
            cb = self.fig.colorbar(im, ax=self.ax, fraction=0.0594)
            
            self.ax.axhline(y=mid_z, linewidth=0.5, color='#d62728', linestyle='dashed')
            self.ax.axvline(x=mid_x, linewidth=0.5, color='#d62728', linestyle='dashed')
                        
            # create new axes on the right and on the top of the current axes
            divider = make_axes_locatable(self.ax)
            axHistx = divider.append_axes("top", 1.2, pad=0.2, sharex=self.ax)
            axHisty = divider.append_axes("right", 1.2, pad=0.2, sharey=self.ax)
            axHistx.bar(x=range(beamspot.shape[0]), height=np.ma.sum(beamspot, axis=0), align='center',
                        linewidth=1, color=(0.2, 0.4, 0.6, 0.6), edgecolor='black')
            axHistx.plot(range(beamspot.shape[0]), np.ma.sum(beamspot, axis=0), "black")
            # make some labels invisible
            plt.setp(axHistx.get_xticklabels() + axHisty.get_yticklabels(), visible=False)
            axHistx.set_ylabel('Dose [$Mrad/hr$]', fontsize=10)
            axHisty.set_xlabel('Dose [$Mrad/hr$]', fontsize=10)
            axHisty.barh(y=range(beamspot.shape[1]), width=np.ma.sum(beamspot, axis=1), align='center',
                         linewidth=1, color=(0.2, 0.4, 0.6, 0.6), edgecolor='black')
            axHisty.plot(np.ma.sum(beamspot, axis=1), range(beamspot.shape[1]), "black")

            
            cb.set_label("Dose rate [$Mrad/hr$]")
            self.ax.text(1.5, 1.3, radius,
                    horizontalalignment='right', verticalalignment='top', transform=self.ax.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=10) 
            self.ax.set_xlabel('x [mm]')
            self.ax.set_ylabel('y[mm]')


    def Plot_Beam_profile_3d(self, Directory=False, PdfPages=False, depth=[0]):
        '''
        Make a 3d scan at specific depth (The function is under updates)
        '''
        self.log.info("Make a 3d scan at specific depth")
        subdirectory = "beamspot/"

        def f(x, y, Factor=9.62, Background=0.012, beamspot=None):
            return (beamspot[y, x] * 1000000 - Background) * Factor

        for d in range(len(depth)):
            with tb.open_file(Directory + subdirectory + depth[d] + "/beamspot_" + depth[d] + ".h5", 'r') as in_file:
                beamspot = in_file.root.beamspot[:]
            y = np.linspace(0, beamspot.shape[0] - 1, 100, dtype=int)
            x = np.linspace(0, beamspot.shape[1] - 1, 100, dtype=int)
            X, Y = np.meshgrid(x, y)
            Z = f(X, Y, beamspot=beamspot)

            fig = plt.figure()
            self.ax = fig.gca(projection='3d')
            plot = self.ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
            plt.axhline(y=25, linewidth=2, color='#d62728', linestyle='dashed')
            plt.axvline(x=16, linewidth=2, color='#d62728', linestyle='dashed')
            cb = fig.colorbar(plot, ax=ax, fraction=0.046)
            cb.set_label("Dose rate [$Mrad/hr$]")
            ax.set_xlabel('x [mm]')
            ax.set_ylabel('y[mm]')
            plt.axis('off')
            ax.set_title("Beam profile at " + depth[d] + "without collimator support", fontsize=12)
            plt.savefig(Directory + subdirectory + depth[d] + "/beamspot_" + depth[d] + "_3d.png")
            PdfPages.savefig()

    def plot_beamspot(self, Directory=None, depth=["60cm"], PdfPages=False):
        self.log.info('plot the beamspot The function is alternative to the function Plot_Beam_profile_2d')
        subdirectory = "beamspot/"
        for d in depth:
            filename = Directory + subdirectory + d + "/beamspot_" + d + ".h5"
            with tb.open_file(filename, 'r') as in_file:
                data = in_file.root.beamspot[:]
                            
            # Calibration Factor
            Factor = 9.81  # diode B
            #  Factor = 9.76 # diode A
            Background = 5.7 * 10 ** (-9)  # 5 nA
            data = (data - Background) * Factor * 10 ** 9
            
            # OF module
            mod_length = 84.975 / 10.0
            mod_width = 15.4 / 10.0
            
            # DHP
            dhp_length = 4.2 / 10.0
            dhp_width = 3.28 / 10.0
            
            # DCD
            dcd_length = 5.13 / 10.0
            dcd_width = 3.41 / 10.0
            
            # Switcher
            sw_length = 3.6 / 10.0
            sw_width = 1.89 / 10.0
            sw_locs = [8.96, 9.92, 10.88, 10.88, 10.88, 9.235, 19.338]
            
            # module collection
            mod_color = "black"
            # module outline
            mod_patches = [Rectangle((0, 0), mod_length, mod_width, fill=False, color=mod_color, linewidth=2)]
            # dhps
            for i in range(4):
                mod_patches.append(Rectangle((mod_length - 1.3494 - dhp_length / 2, mod_width - 0.2759 - dhp_width / 2 - 0.35 * i), dhp_length, dhp_width, fill=False, color=mod_color, linewidth=1.5))
            # dcds
            for i in range(4):
                mod_patches.append(
                    Rectangle((mod_length - 1.9338 - sw_length / 2, mod_width - 0.2759 - dcd_width / 2 - 0.35 * i), dcd_length,
                              dcd_width, fill=False, color=mod_color, linewidth=1.5))
            # switchers
            for i in range(6):
                mod_patches.append(
                    Rectangle((mod_length - sum(sw_locs[:-i - 3:-1]) / 10.0 - sw_length / 2, mod_width - 0.1278 - sw_width / 2), sw_length,
                              sw_width, fill=False, color=mod_color, linewidth=1.5))
            a_x1 = -mod_length / 2 - 1.0 + 1.3494 - dhp_length / 2
            a_x2 = +mod_length / 2 - 1.0
            a_y1 = -mod_width / 2  # - 1.0
            a_y2 = +mod_width / 2  # - 1.0
            mod_trans_a = mpl.transforms.Affine2D().translate(-mod_length / 2, -mod_width / 2) + mpl.transforms.Affine2D().rotate_deg(180) + mpl.transforms.Affine2D().translate(-1.0, 0)
            p_mod = PatchCollection(mod_patches, match_original=True)
            
            nullfmt = NullFormatter()  # no labels
            
            # definitions for the axes
            left, width = 0.1, 0.60
            bottom, height = 0.1, 0.60
            bottom_p = bottom + height + 0.02
            left_p = left + width + 0.02
            
            rect_spot = [left, bottom, width, height]
            rect_projx = [left, bottom_p, width, 0.2]
            rect_projy = [left_p, bottom, 0.2, height]
            
            # start with a rectangular Figure
            plt.figure()  # 1, figsize=(8, 8))
            
            axSpot = plt.axes(rect_spot)
            axProjx = plt.axes(rect_projx)
            axProjy = plt.axes(rect_projy)
            
            # no labels
            axProjx.xaxis.set_major_formatter(nullfmt)
            axProjy.yaxis.set_major_formatter(nullfmt)
            
            # the scatter plot:
            im_spot = axSpot.imshow(data, origin="upper", interpolation="None", aspect="auto", extent=(-6.5, +6.5, +6.5, -6.5))
            
            axSpot.plot((-6.5, +6.5), (0, 0), color="white", lw=1)
            axSpot.plot((0, 0), (-6.5, +6.5), color="white", lw=1)
            p_mod.set_transform(mod_trans_a + axSpot.transData)
            axSpot.add_collection(p_mod)
            axSpot.set_xlabel("x [cm]")
            axSpot.set_ylabel("z [cm]")
            axrange = np.arange(-6, +6.5, 0.5)
            
            axProjx.bar(x=axrange, height=data[12, :].astype(np.float), width=0.3)
            axProjx.set_ylabel("dose rate [krad/h]")
            axProjx.axvline(a_x1, color=mod_color)
            axProjx.axvline(a_x2, color=mod_color)
            
            axProjy.barh(y=axrange, width=data[:, 12].astype(np.float), height=0.3)
            axProjy.axhline(a_y1, color=mod_color)
            axProjy.axhline(a_y2, color=mod_color)
            axProjy.set_xlabel("dose rate [krad/h]")
            
            axProjx.set_xlim(axSpot.get_xlim())
            axProjy.set_ylim(axSpot.get_ylim())
            
            axProjy.set_xlim(axProjx.get_ylim())
            
            textleft = 'PXD outer forward module'
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            axSpot.text(0.05, 0.95, textleft, transform=axSpot.transAxes, fontsize=8, verticalalignment='top', bbox=props)
            
            cbar = plt.colorbar(im_spot)
            cbar.set_label("dose rate [krad/h]")
            
            plt.suptitle("beamspot at distance 60 cm, tube parameter: 40 kV, 50 mA, no filter")
            
            plt.savefig(filename[:-3] + ".png")
            plt.savefig(filename[:-3] + ".pdf")                       
            PdfPages.savefig()
       
    def close(self, PdfPages=False):
            PdfPages.close()


def main():
    """Wrapper function for using the server as a command line tool

    The command line tool accepts arguments for configuring the server which
    are tranferred to the :class:`DCSControllerServer` class.
    """
    # Parse arguments
    parser = ArgumentParser(description='Calibration results for Xray radiation system'
                            'Controller',
                            epilog='For more information contact '
                            'ahmed.qamesh@cern.ch',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.set_defaults(interface='data')
    
    # CAN interface
    CGroup = parser.add_argument_group('interface')
    iGroup = CGroup.add_mutually_exclusive_group()
    iGroup.add_argument('-d', '--data', action='store_const', const='data',
                        dest='interface',
                        help='Use data interface (default). When no '
                        'data file interface is found or connected a data files will be used')
    iGroup.add_argument('-s', '--sim', action='store_const',
                        const='sim', dest='interface',
                        help='Use simulated data')
