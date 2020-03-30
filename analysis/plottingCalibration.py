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
#matplotlib.rcParams['text.usetex'] = True
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
from analysis import analysis
from analysis import logger
from scipy import interpolate
colors = ['black', 'red', '#006381', "blue", '#33D1FF', '#F5A9BC', 'grey', '#7e0044', 'orange', "maroon", 'green', "magenta", '#33D1FF', '#7e0044', "yellow"]
an = analysis.Analysis()
class PlottingCalibration(object):     

    def __init__(self, interface='data'):
        self.log = logger.setup_derived_logger('Plotting')
        self.log.info('Plotting initialized')
        
        # Initialize default arguments
        if interface is None:
            interface = 'data'
        elif interface not in ['data', 'sim']:
            raise ValueError(f'Possible interfaces are "data" or '
                             f'"sim" and not "{interface}".')

        
    @property
    def interface(self):
        """:obj:`str` : Type of the final plots. Possible values are
        ``'data'`` and ``'sim'``."""
        return self.__interface
               
    def diode_calibration(self, tests=["A"], directory=False, PdfPages=False):
        '''
        The function plots the calibration results for the PN diodes
        Input directory = directory + diode_calibration/cern_calibration/
        diodes is an array of strings represents the diodes name A, B and C.
        '''
        self.log.info('Calibration results for the diodes')
        subdirectory = "diode_calibration/"
        name_prefix = "diode_calibration_"
        
        fig = plt.figure()
        gs = gridspec.GridSpec(2, 1, height_ratios=[3.9, 2])
        ax = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        factor_row = []
        for test in tests:
            file = directory + subdirectory + test+"/" + name_prefix+test+".csv"
            dep = []
            dose = []
            bkg = []
            current = []
            factor = []
            with open(file, 'r')as data:
                reader = csv.reader(data)
                next(reader)
                for row in reader:
                    dep = np.append(dep, np.float(row[0]))  # Distance from the source
                    dose = np.append(dose, np.float(row[4]))  # Dose rate
                    current = np.append(current, np.float(row[2]))  # current
                    factor = np.append(factor, np.float(row[4]) / (np.float(row[2]) - np.float(row[1])))
                    bkg = np.append(bkg, np.float(row[1]))
                mean = np.mean(factor)
            factor_row = np.append(factor_row, factor)
            factor_row = np.append(factor_row, mean)
            ax.errorbar(dose, current, xerr=0.0, yerr=0.0, fmt='o', color=colors[tests.index(test)], markersize=3)  # plot points
            sig = [0.4 * current[k] for k in range(len(current))]
            
            popt, pcov = curve_fit(an.linear, dose, current, sigma=sig, absolute_sigma=True, maxfev=5000, p0=(1, 1))
            chisq = an.red_chisquare(np.array(current), an.linear(dose, *popt), np.array(sig), popt)
            line_fit_legend_entry = "Diode " + test + ':%.4fx+%.4f' % (popt[0], popt[1])
            ax.plot(dose, an.linear(dose, *popt), linestyle="--",
                    color=colors[tests.index(test)], label=line_fit_legend_entry)
        ax.set_ylabel('Dose rate [$Mrad(sio_2)/hr$]')
        ax.set_xlabel(r'Current [$\mu$ A]')
        ax.set_title('(Diode calibration at %s and %s)' % ("40kV", "50mA"), fontsize=11)
        # Draw a table of parameters under the plot
        rows = ["Diode A", "Diode B", "Diode C"]
        columns = ["3 cm", "5 cm", "8 cm", "Mean factor"]
        ax2.table(cellText=[np.round(factor_row[0:4], 3), np.round(factor_row[4:8], 3),
                            np.round(factor_row[8:12], 3)],
                  rowLabels=rows,
                  rowColours=colors[1:4],
                  colColours=["lightgray", "lightgray", "lightgray", "lightgray"],
                  colLabels=columns, cellLoc='center', rowLoc='center', loc='center', fontsize=7)
        plt.subplots_adjust(bottom=0.1)
        ax2.set_xlabel(r'Calibration factors')
        ax2.set_axis_off()
        ax.grid(True)
        ax.legend()
        fig.savefig(directory + subdirectory + name_prefix+"All.png", bbox_inches='tight')
        plt.tight_layout()
        PdfPages.savefig()

    def calibration_temperature(self, tests=[0], PdfPages=False, directory=False):
        '''
        The function will plot the temperature effect on the diode calibration within 250 seconds of radiation, the data collected without any filter in the tube
        '''
        self.log.info('plot the temperature effect on the diode calibration within 250 seconds of radiation')
        subdirectory = '/diode_temperature/'
        filter = "without_filter"
        plot_prefix = "diode_temperature"
        test_file = directory + subdirectory +filter+"/"+plot_prefix +".h5"
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax2 = ax.twinx()
        plot_lines = []
        with tb.open_file(test_file) as in_file:
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
        plt.savefig(test_file[:-3]+".png")
        PdfPages.savefig()
    
    def IV_test(self, tests=["A"], directory=False, PdfPages=False, h5 =True):
        self.log.info('Plotting IV curves for diodes %s'%tests)
        subdirectory = "diode_calibration/"
        name_prefix = "IV_test_"
        fig = plt.figure()
        fig.add_subplot(111)
        ax = plt.gca()
        conversion = 10**9
        for test in tests:
            if h5 is not None:
                test_file = directory + subdirectory + test+"/" + name_prefix+test+".h5"
                with tb.open_file(test_file, 'r') as in_file:
                    IV_results = in_file.root.IV_results[:]
                    v=IV_results['voltage']
                    mean = IV_results['mean_current']*conversion
                    std =IV_results['std_current']*conversion
                    ax.set_ylim(-3.,15)
                    ax.set_xlim(0,52)
                    ax.set_xscale('log')
            else:
                v = []
                mean = []
                std = []
                test_file = directory + subdirectory + test+"/" + name_prefix + test +".csv"
                with open(test_file,'r')as data:
                    reader = csv.reader(data)
                    next(reader)
                    for row in reader:
                        v = np.append(v, float(row[2]))
                        mean = np.append(mean, float(row[1])*conversion)
                        std = np.append(std, float(row[3])*conversion)*1.04
                        ax.set_ylim(-1.5,0)
                        ax.set_xlim(-52,0)
    
            ax.errorbar(v,mean,yerr=std, 
                        fmt='o', color=colors[tests.index(test)], markersize=5, 
                        ecolor="black",label=("Diode %s " % test))
            ax.plot(v,mean,color='black')
        ax.set_xlabel("Reverse Voltage [V]")
        ax.set_ylabel("Current [nA]")
        ax.set_title('IV Curve')
        ax.grid(True)
        ax.legend(loc = "upper right")
        plt.savefig(test_file[:-14]+"_" +name_prefix+"All.png", bbox_inches='tight')
          
    def opening_angle(self, directory=False, Unknown_diameter=np.linspace(3, 10, 20), PdfPages=PdfPages, tests=[0]):
        '''
        To get the estimated beam radius relative to the depth
        '''
        self.log.info('Estimating the beam radius relative to the depth')
        for j in range(len(tests)):
            subdirectory = "opening_angle/"+ tests[j]+"/"
            test_file = directory + subdirectory + "opening_angle_" + tests[j] + ".csv"
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
            fig1 = plt.figure()
            fig1.add_subplot(111)
            ax1 = plt.gca()
            ax1.errorbar(h, r, xerr=0.0, yerr=std, fmt='o', color='black', markersize=3, ecolor='black')  # plot points
            popt, pcov = curve_fit(an.linear, h, r, sigma=std, absolute_sigma=True, maxfev=5000, p0=(1, 1))
            chisq2 = an.red_chisquare(np.array(r), an.linear(h, *popt), np.array(std), popt)
            line_fit_legend_entry = 'line fit: mh + c\n m=$%.3f\pm%.3f$\nc=$%.3f\pm%.3f$' % (popt[0], np.absolute(pcov[0][0]) ** 0.5, popt[1], np.absolute(pcov[1][1]) ** 0.5)
            ax1.plot(h, an.linear(h, *popt), '-', lw=1, label=line_fit_legend_entry, markersize=9)  # plot fitted function
            ax1.set_title('Radius covered by beam spot %s (40 kV and 50 mA)' % (tests[j]), fontsize=12)
            ax1.grid(True)
            ax1.legend()
            ax1.set_ylabel('Radius (r) [cm]')
            ax1.set_xlabel('Distance from the  collimator holder(h) [cm]')
            fig1.savefig(directory + subdirectory + "depth_radius_linear_" + tests[j] + '.png', bbox_inches='tight')
            PdfPages.savefig()


    def opening_angle_cone(self, directory=None, tests=[0],PdfPages=PdfPages):
        '''
        Draw the cone shape of the opening angle
        '''
        self.log.info('Draw the cone shape of the opening angle')
        for j in range(len(tests)):
            subdirectory = "opening_angle/"+ tests[j]+"/"
            test_file = directory + subdirectory + "opening_angle_" + tests[j] + ".csv"
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
            fig2 = plt.figure()
            fig2.add_subplot(111)
            ax2 = plt.gca()
            for i in range(len(r_space)):
                x, y = np.linspace(-r_space[i], r_space[i], 2), [h_space[i] for _ in np.arange(2)]
                ax2.plot(x, y, linestyle="solid")
            ax2.text(0.95, 0.90, "$\Theta^{rad}$ = %.3f$\pm$ %.3f\n $h_{0}$=%.3f$\pm$ %.3f" % (2 * popt[0], 2 * np.absolute(pcov[0][0]) ** 0.5, popt[1] / (popt[0]), np.absolute(pcov[1][1]) ** 0.5 / popt[0]),
                    horizontalalignment='right', verticalalignment='top', transform=ax2.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
            ax2.set_title('Diameter covered by beam spot %s' % (tests[j]), fontsize=12)
            ax2.invert_yaxis()
            ax2.set_xlabel('Diameter (d) [cm]')
            ax2.set_ylabel('Height from the the collimator holder(h) [cm]')
            ax2.grid(True)
            fig2.savefig(test_file[:-4]+".png", bbox_inches='tight')
            PdfPages.savefig()      

    def dose_depth(self, directory=False, PdfPages=False,factor = None, voltage="40 kV", current="50 mA", stdev=0.2, tests=[0], theta=0.16):
        '''
        Relation between the depth and  the Dose rate
        '''
        self.log.info('Relation between the depth and  the Dose rate')
        for i in range(len(tests)):
            subdirectory = "dose_depth/"
            plot_prefix = "dose_depth_"
            test_file = directory +subdirectory+tests[i]+"/"+plot_prefix + tests[i] + ".csv"
            fig = plt.figure()
            ax = fig.add_subplot(111)

            height = []
            y1 = []
            b1 = []
            with open(test_file, 'r')as data:
                reader = csv.reader(data)
                next(reader)
                for row in reader:
                    height = np.append(height, float(row[0]))  # Distance from the source
                    y1 = np.append(y1, (float(row[1])*float(factor)))  # Dose rate
                    b1 = np.append(b1, (float(row[2])*float(factor)))  # Background
            y1 = [y1[k] - b1[k] for k in range(len(y1))]  # Subtract Background
            #y1 = [y1[k] * factor for k in range(len(y1))]  # Multiply by the factor to get the dose rate
            sig = [stdev * y1[k] for k in range(len(y1))]
            popt1, pcov = curve_fit(an.Inverse_square, height, y1, sigma=sig, absolute_sigma=True, maxfev=500, p0=(300, 6, 0))
            # chisq1 = an.red_chisquare(np.array(y1), an.Inverse_square(np.array(height), *popt1), sig, popt1)
            ax.errorbar(height, y1, yerr=sig, color=colors[i + 1], fmt='o', label=tests[i], markersize='4')
            xfine = np.linspace(height[0], height[-1], 100)  # define values to plot the function
            a, b, c = popt1[0], popt1[1], popt1[2]
            a_err, b_err, c_err = np.absolute(pcov[0][0]) ** 0.5, np.absolute(pcov[1][1]) ** 0.5, np.absolute(pcov[2][2]) ** 0.5
            ax.plot(xfine, an.Inverse_square(xfine, *popt1), colors[i + 1], label='Fit parameters:\n a=%.2f$\pm$ %.2f\n b=%.2f$\pm$ %.2f\n c=%.2f$\pm$ %.2f\n' % (a, a_err, b, b_err, c, c_err))
            
            ax.text(0.9, 0.56, r'$R= \frac{a}{(h+b)^2}-c$',
                    horizontalalignment='right', verticalalignment='top', transform=ax.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))
            # print "The dose rate at %.2f cm depth is " %(45) + str(popt1[0]/(45+popt1[1])**2)+" Mrad/hr "+tests[i]
            ax.set_xlabel('Distance from the collimator holder(h) [cm]')
            ax.set_title('Dose rate vs distance %s at  (%s and %s)' % (tests[i], voltage, current), fontsize=11)
            ax.set_ylabel('Dose rate (R) [$Mrad(sio_2)/hr$]')
            ax.set_xlim([0, max(height) + 8])
            ax.grid(True)
            ax.legend(loc="upper right")
            ax.ticklabel_format(useOffset=False)
            fig.savefig(test_file[:-4]+".png", bbox_inches='tight')  # 1.542
            plt.tight_layout()
            PdfPages.savefig()
            cmap = plt.cm.get_cmap('viridis', 15)
            sc = ax.scatter(xfine, an.Inverse_square(xfine, *popt1), c=an.Inverse_square(xfine, a=a, b=b, c=c), cmap=cmap, s=50,)
            # cbar = fig.colorbar(sc, ax=ax, orientation='horizontal')
            # cbar.ax.invert_xaxis()
            # cbar.set_label("Dose rate", labelpad=1, fontsize=10)
            
            fig.savefig(test_file[:-4] + "color.png", bbox_inches='tight')
        return a, b, c
    
    def dose_current(self, directory=False, PdfPages=False,tests=[0], stdev=0.06, depths=[0], table=True,factor = None, voltages=[0]):
        '''
        To get the calibration curves for each current
        For each Measurement you make you need to replace the numbers 0 in Background, factor, .....by your measurement
        Background =  array of background estimated for each depth
         '''
        for test in tests:
            self.log.info('Get the calibration curves for each current['+test+"]")
            col_row = plt.cm.BuPu(np.linspace(0.3, 0.9, len(voltages)))
            for depth in depths:
                self.log.info('Get the calibration curves for each current['+test+"] at "+depth)
                subdirectory = "dose_current/"+test+"/" + depth + "/" 
                plot_prefix = "dose_current_"
                test_file = directory+subdirectory+ plot_prefix+test+"_"
                stdev = 0.06
                y1 = []
                x1 = []
                Dataset = []
                kafe_Fit = []
                fit_para = []
                if table:
                    gs = gridspec.GridSpec(2, 1, height_ratios=[3.5, 2])
                    ax = plt.subplot(gs[0])
                    ax2 = plt.subplot(gs[1])
                else:
                    fig = plt.figure()
                    ax = fig.add_subplot(111)
                for i in range(len(voltages)):
                    x = []
                    y = []
                    Background = [0.00801e-06]
                    with open(test_file+voltages[i]+".csv", 'r')as data1:
                        reader = csv.reader(data1)
                        next(reader)
                        for row in reader:
                            x = np.append(x, float(row[0]))
                            y = np.append(y, (float(row[1]) - float(row[2])) * float(factor))
                            
                    x1.append(x)
                    y1.append(y)
                    sig = [stdev * y1[i][k] for k in range(len(y1[i]))]
                    ax.errorbar(x1[i], y1[i], yerr=sig, color=col_row[i], fmt='o',label='V=%s' % (voltages[i]))
                    Dataset = np.append(Dataset, build_dataset(x1[i], y1[i], yabserr=sig, title='I=%s' % voltages[i],
                                                                axis_labels=['Current (mA)', '$Dose rate [Mrad(sio_2)/hr]$']))
                    popt, pcov = curve_fit(an.linear, x1[i], y1[i], sigma=sig, absolute_sigma=True, maxfev=5000, p0=(1, 1))
                    xfine = np.linspace(0., max(x1[i]), 100)
                    ax.plot(xfine, an.linear(xfine, *popt), color=col_row[i])
                    chisq = an.red_chisquare(np.array(y1[i]), an.linear(x1[i], *popt), np.array(sig), popt)
                    ax.text(0.95, 0.90, "y[$Mrad(sio_2)/hr$]= m$x$+c",
                            horizontalalignment='right', verticalalignment='top', transform=ax.transAxes,
                            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
                    plt.ticklabel_format(useOffset=False)
                    plt.xlim(0, 60)
                    ax.set_title('Calibration curve at '+ depth+" "+test, fontsize=12)
                    ax.set_ylabel('Dose rate [$Mrad(sio_2)/hr$]')
                    ax.grid(True)
                    ax.legend()  # prop={'size': 8}
                    ax.set_xlabel('Tube current [mA]')
                    plt.tight_layout()
                    # List the fit parameters into a table
                    for par in popt:
                        fit_para = np.append(fit_para, par)
                if table:
                    rows = voltages
                    columns = ['m', 'c']
                    ax2.table(cellText=[np.round(fit_para[0:2], 2), np.round(fit_para[2:4], 2)],
                              rowLabels=rows,
                              rowColours=col_row,
                              colLabels=columns,
                              colColours=["lightgray", "lightgray"],
                              animated=True,
                              cellLoc='center', rowLoc='center', loc='center', fontsize=12)
                    plt.subplots_adjust(bottom=0.1)
                    ax2.set_axis_off()
                    
                plt.savefig(test_file+depth+".png", bbox_inches='tight')
                PdfPages.savefig()

    def dose_voltage(self, directory=False, PdfPages=False, factor =None,  depth=["8cm"], tests=["without_Al_Filter"],  currents = [0], kafe_Fit=False, table=True):
        '''
        Effect of tube Voltage on the Dose, the available data is only without Al Filter
        '''
        for test in tests:
            self.log.info('Effect of tube Voltage at %s on the Dose rate [%s]' % (depth[0], test)) 
            y1 = []
            x1 = []
            Dataset = []
            fit_para = []
            col_row = plt.cm.BuPu(np.linspace(0.3, 0.9, len(currents)))
            subdirectory = "dose_voltage/"+test+"/" + depth[0] + "/" 
            plot_prefix ="dose_voltage_"
            test_file = directory+subdirectory+plot_prefix+test+"_"
            if table:
                gs = gridspec.GridSpec(2, 1, height_ratios=[3.5, 2])
                ax = plt.subplot(gs[0])
                ax2 = plt.subplot(gs[1])
            else:
                fig = plt.figure()
                ax = fig.add_subplot(111)
    
            for i in range(len(currents)):
                x = []
                y = []
                Background = [0.00801e-06]
                with open(test_file+currents[i]+".csv", 'r')as data1:
                    reader = csv.reader(data1)
                    next(reader)
                    for row in reader:
                        x = np.append(x, float(row[0]))
                        y = np.append(y, (float(row[1]) - Background[0]) * float(factor))
                x1.append(x)
                y1.append(y)
                stdev = 0.06
                sig = [stdev * y1[i][k] for k in range(len(y1[i]))]
                Dataset = np.append(Dataset, build_dataset(x1[i], y1[i], yabserr=sig, title='I=%s' % currents[i], axis_labels=['Voltage (kV)', '$Dose rate [Mrad(sio_2)/hr]$']))
                popt, pcov = curve_fit(an.quadratic, x1[i], y1[i], sigma=sig, absolute_sigma=True, maxfev=5000, p0=(1, 1, 1))
                #xfine = np.linspace(0., max(x1[i]), 100)
                xfine = np.linspace(0., 130, 200)
                ax.plot(xfine, an.quadratic(xfine, *popt), color=col_row[i])
                chisq = an.red_chisquare(np.array(y1[i]), an.quadratic(x1[i], *popt), np.array(sig), popt)
                ax.errorbar(x1[i], y1[i], yerr=sig, color=col_row[i], fmt='o',
                            label='I=%s' % (currents[i]))
                for par in popt:
                    fit_para = np.append(fit_para, par)
                ax.text(0.95, 0.90, "y[$Mrad(sio_2)/hr$]= a$\mathrm{x}^2$ + bx+c",
                        horizontalalignment='right', verticalalignment='top', transform=ax.transAxes,
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
            ax.set_title('Effect of the tube voltage at ' + depth[0] + " "+test, fontsize=12)
            ax.set_ylabel('Dose rate [$Mrad(sio_2)/hr$]')
            ax.set_xlabel('Voltage (kV)')
            ax.grid(True)
            ax.legend()
            plt.ticklabel_format(useOffset=False)
            ax.set_xlim(xmin=5)
            ax.set_ylim(ymin=0)
            if table:
                rows = currents
                columns = ['a', 'b', 'c']
                ax2.table(cellText=[np.round(fit_para[0:3], 3), np.round(fit_para[3:6], 3),
                                     np.round(fit_para[6:9], 3), np.round(fit_para[9:12], 3)],
                          rowLabels=rows,
                          rowColours=col_row,  # colors[0:4],
                          colColours=["lightgray", "lightgray", "lightgray"],
                          animated=True,
                          colLabels=columns, cellLoc='center', rowLoc='center', loc='center', fontsize=12)
                plt.subplots_adjust(bottom=0.1)
                ax2.set_axis_off()
            plt.savefig(test_file+depth[0]+".png", bbox_inches='tight')
            PdfPages.savefig()
            if kafe_Fit:
                kafe_Fit = []
                # Another fitting using Kafe fit
                for Data in Dataset:
                    kafe_Fit = np.append(kafe_Fit, Fit(Data, quadratic_3par))
                    for fit in kafe_Fit:
                        fit.do_fit()
                kafe_plot = Plot(kafe_Fit[2], kafe_Fit[3])
                kafe_plot.plot_all(show_data_for='all', show_band_for=0)
                kafe_plot.save(test_file+depth[0]+"_kafe_Fit.png")
            PdfPages.savefig()
            
    def dose_drop(self, directory=False, tests = False, PdfPages=False, factor = None, depth=[0], voltages=[0]):
        '''
        Dose drop after Al filter at two Voltages.
        '''
        filter = tests[0]
        col_row = plt.cm.BuPu(np.linspace(0.3, 0.9, len(voltages)))
        for i in range(len(depth)):
            self.log.info('Dose drop at %s cm [%s]' %(depth[i],filter))
            fig = plt.figure()
            fig.add_subplot(111)
            ax = plt.gca()
            volt_row = []
            fit_para = []
            subdirectory = "dose_current/"+filter+"/" + depth[i] + "/" 
            plot_prefix = "dose_current_"
            test_file = directory+subdirectory+plot_prefix+filter+"_"
            for volt in voltages:
                x1 = []
                y1 = []
                y2 = []
                bkg_y1 = []
                bkg_y2 = []
                difference = []
                with open(test_file+ volt +".csv", 'r')as data:  # Get Data for the first Voltage
                    reader = csv.reader(data)
                    next(reader)
                    for row in reader:
                        x1 = np.append(x1, float(row[0]))  # Voltage
                        y1 = np.append(y1, (float(row[1]) - float(row[2])) * float(factor))  # Data with Al filter
                        y2 = np.append(y2, (float(row[3]) - float(row[4])) * float(factor))  # Data without Al filter
                difference = [(y2[i]-y1[i])*100/y2[i] for i in np.arange(len(y1))]
                spline = interpolate.splrep(x1,difference, s=10, k=2)  # create spline interpolation
                xnew = np.linspace(np.min(x1), np.max(x1), num = 50, endpoint = True)
                spline_eval = interpolate.splev(xnew, spline)  # evaluate spline
                plt.plot(xnew,spline_eval,"-", color=col_row[voltages.index(volt)])
                plt.plot(x1,difference,'o', color=col_row[voltages.index(volt)],label="%s" % volt)
            ax.set_title('Dose drop after Al filter at ' + depth[i], fontsize=12)
            ax.set_ylabel('Dose rate drop [%]')
            ax.set_xlabel('Tube current [mA]')
            ax.set_ylim(0,100)
            ax.legend(prop={'size': 10})
            ax.grid(True)
            plt.savefig(test_file[:-16]+'dose_current_drop_' + depth[i] + ".png", bbox_inches='tight')
            PdfPages.savefig()

                          
    def power_2d(self, directory=False, PdfPages=False, size_I=50, size_V=60, V_limit=50, I_limit=50):
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
        plt.savefig(directory + 'power/Power.png')
        PdfPages.savefig()

    def Plot_Beam_profile_2d(self, directory=False, factor = None , filters = [0], PdfPages=False, depth=None):
        '''
        Make a 2d plot at specific depth
        '''
     
        # factor = 9.817  # diode B
        Background = 5.7 * 10 ** (-9)  # convert from A to nA
        binwidth = 1
        subdirectory = "beamspot/"
        filter = filters[0]
        for d in range(len(depth)):
            self.log.info("Make a 2d plot at %s [%s]"%(depth[d],filter))
            test_file = directory + subdirectory +filter+"/"+ depth[d] + "/beamspot_" + depth[d] + ".h5"
            with tb.open_file(test_file, 'r') as in_file:
  
                beamspot = in_file.root.beamspot[:]
                beamspot = (beamspot - Background) * 1000000 * float(factor)
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
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            cmap = plt.cm.get_cmap('viridis', 30)
            im = ax.imshow(beamspot, aspect='auto', interpolation='gaussian', cmap=cmap)  # ,extent=extent)
            cb = fig.colorbar(im, ax=ax, fraction=0.0594)
            
            # create new axes on the right and on the top of the current axes
            divider = make_axes_locatable(ax)
            axHistx = divider.append_axes("top", 1.2, pad=0.2, sharex=ax)
            axHisty = divider.append_axes("right", 1.2, pad=0.2, sharey=ax)
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
            ax.text(1.5, 1.3, radius,
                    horizontalalignment='right', verticalalignment='top', transform=ax.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8), fontsize=10)
            ax.set_title("Beam profile at " + depth[d] + " from the collimator holder (%s and %s)" % ("40 kV", "50mA"), fontsize=12, y=1.7, x=-0.6)
            ax.set_xlabel('x [mm]')
            ax.set_ylabel('y[mm]')
            plt.savefig(test_file[:-4]+"_2d.png")
            PdfPages.savefig()

            fig, ax2 = plt.subplots()
            central_value = beamspot[mid_z, mid_x]
            for z in np.arange(beamspot.shape[0]):
                for x in np.arange(beamspot.shape[1]):
                    beamspot[z, x] = beamspot[z, x] / np.float(central_value) * 100
            cmap2 = plt.cm.get_cmap('viridis', 5)
            im2 = ax2.imshow(beamspot, aspect='auto', interpolation='gaussian', cmap=cmap2)
            cb2 = fig.colorbar(im2, ax=ax2, fraction=0.0594)

          #  for j, txt in enumerate(mean):
          #      ax2.annotate(txt,xy=(x_offset[j],y_offset[j]),color='#d62728', size=8)
            plt.axhline(y=mid_z, linewidth=0.5, color='#d62728', linestyle='dashed')
            plt.axvline(x=mid_x, linewidth=0.5, color='#d62728', linestyle='dashed')

            if (depth[d] == "8cm"):
                # Draw module details
                rec_position_x, rec_position_y = mid_z - w / 2, mid_x - l / 2
                rect2 = patches.Rectangle((rec_position_x, rec_position_y), w, l, linewidth=2, edgecolor='black', facecolor='none')
                ax2.add_patch(rect2)
                plt.annotate(s='', xy=(rec_position_x - 0.5, mid_x + l / 2), xytext=(rec_position_x - 0.5, rec_position_y), arrowprops=dict(arrowstyle='<->'))
                ax2.annotate(np.str(l) + "mm", xy=(rec_position_x - 5, rec_position_y + l / 2), color='white', size=10)

                plt.annotate(s='', xy=(rec_position_x, rec_position_y - 0.5), xytext=(rec_position_x + w, rec_position_y - 0.5), arrowprops=dict(arrowstyle='<->'))
                ax2.annotate(np.str(w) + "mm", xy=(rec_position_x + w / 2 - 1.5, rec_position_y - 1.0), color='white', size=10)

            # draw a circle represents the central position
            if depth[d] == "3cm_collimator":
                circle2 = plt.Circle((mid_z, mid_x), r, color='red', fill=False)
            else:
                circle2 = plt.Circle((mid_z, mid_x - 1), r, color='red', fill=False)
            ax2.add_artist(circle2)
            ax2.add_artist(plt.Circle((mid_z, 2 * mid_x), 1., color='red'))
            ax2.set_title("Beam profile at " + depth[d] + " from the collimator holder (%s and %s)" % ("40 kV", "50mA"),
                          fontsize=11)
            ax2.set_xlabel('x [mm]')
            ax2.set_ylabel('y[mm]')
            cb2.set_label("Relative intensity to central position [$\%$]")
            plt.savefig(test_file[:-3]+"_percentile_2d.png")
            PdfPages.savefig()

    def Plot_Beam_profile_3d(self, directory=False, factor=None, PdfPages=False, depth=[0], filters=[0]):
        '''
        Make a 3d plot at specific depth (The function is under updates)
        '''
        subdirectory = "beamspot/"
        filter = filters[0]
        def f(x, y, factor= None, Background=0.012, beamspot=None):
            return (beamspot[y, x] * 1000000 - Background) * float(factor)
        
        for d in range(len(depth)):
            self.log.info("Make a 3d plot at %s [%s]"%(depth[d],filter))
            test_file = directory + subdirectory +filter+"/"+ depth[d] + "/beamspot_" + depth[d] + ".h5"
            with tb.open_file(test_file, 'r') as in_file:
                beamspot = in_file.root.beamspot[:]
            y = np.linspace(0, beamspot.shape[0] - 1, 100, dtype=int)
            x = np.linspace(0, beamspot.shape[1] - 1, 100, dtype=int)
            X, Y = np.meshgrid(x, y)
            Z = f(X, Y, factor = factor, beamspot=beamspot)

            fig = plt.figure()
            ax = fig.gca(projection='3d')
            plot = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
            plt.axhline(y=25, linewidth=2, color='#d62728', linestyle='dashed')
            plt.axvline(x=16, linewidth=2, color='#d62728', linestyle='dashed')
            cb = fig.colorbar(plot, ax=ax, fraction=0.046)
            cb.set_label("Dose rate [$Mrad/hr$]")
            ax.set_xlabel('x [mm]')
            ax.set_ylabel('y[mm]')
            plt.axis('off')
            ax.set_title("Beam profile at " + depth[d] + "without collimator support", fontsize=12)
            plt.savefig(test_file[:-3]+ "_3d.png")
            PdfPages.savefig()

    def plot_beamspot(self, directory=None, depth=["60cm"], factor = 9.81, filters = [0], PdfPages=False):
        self.log.info('plot the beamspot The function is alternative to the function Plot_Beam_profile_2d')
        subdirectory = "beamspot/"
        filter = filters[0]
        for d in depth:
            test_file = directory + subdirectory +filter+"/"+ d + "/beamspot_" + d + ".h5"
            with tb.open_file(test_file, 'r') as in_file:
                data = in_file.root.beamspot[:]
                            
            # Calibration factor
              # diode B
            Background = 5.7 * 10 ** (-9)  # 5 nA
            data = (data - Background) * float(factor) * 10 ** 9
            
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
            plt.savefig(test_file[:-3] + "_New.png")
            plt.savefig(test_file[:-3] + "_New.pdf")                       
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
