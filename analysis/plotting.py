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
from analysis import analysis
from analysis import logger
colors = ['black', 'red', '#006381', "blue", '#33D1FF', '#F5A9BC', 'grey', '#7e0044', 'orange', "maroon", 'green', "magenta", '#33D1FF', '#7e0044', "yellow"]

# matplotlib.rc('text', usetex=True)
# params = {'text.latex.preamble': [r'\usepackage{siunitx}']}
# plt.rcParams.update(params)

an =analysis.Analysis()

class Plotting(object):     

    def __init__(self):
        self.log = logger.setup_derived_logger('Plotting')
        self.log.info('Plotting initialized')
        
    def plot_linear(self, Directory=False, colors=colors, PdfPages=False, text=False, txt="Text",
                     x=np.arange(1, 10), x_label="Supply current I_s [A]", y=np.arange(1, 10), y_label="Needed Voltage U_S [V]",
                     map=False, z=np.arange(1, 10), z_label="Transferred Efficiency", test="DCConverter", title="powerSupply_Voltage", p=[1, 2, 3],
                     line=None, data_line=[0], data_label='Power loss in the cable $P_c$ [W]'):
        '''
        PLot a relation between two variables 
        '''
        fig = plt.figure()
        ax = fig.add_subplot(111)
        if map:
            cmap = plt.cm.get_cmap('viridis', 15)
            sc = ax.scatter(x, y, c=z, cmap=cmap, s=8)
            cbar = fig.colorbar(sc, ax=ax, orientation='horizontal')
            cbar.ax.invert_xaxis()
            cbar.set_label(z_label, labelpad=1, fontsize=10)
            plt.axvline(x=4, linewidth=0.8, color=colors[1], linestyle='dashed')
            plt.axhline(y=22.5, linewidth=0.8, color=colors[1], linestyle='dashed')
        else:
            sc = ax.errorbar(x, y, xerr=0.0, yerr=0.0, fmt='o', color=colors[1], markersize=3, ecolor='black')
            ax.plot(x, y, linestyle="-", color=colors[0], label="Fit", markersize=1)       
            # ax.legend(loc="upper right")
            # ax.set_ylim(ymin=min(y)-10)
        ax.set_xlabel(x_label, fontsize=10)
        ax.set_title(title, fontsize=8)
        ax.set_ylabel(y_label, fontsize=10)
        ax.ticklabel_format(useOffset=False)
        ax.grid(True)
        if text:
            ax.text(0.95, 0.45, txt, fontsize=8,
                    horizontalalignment='right', verticalalignment='top', transform=ax.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.2))
                            
        if line:
            # Create axes for loss and voltage 
            ax2 = ax.twinx()
            line = ax2.errorbar(x, data_line, xerr=0.0, yerr=0.0, fmt='o', color=colors[3], markersize=1, ecolor='black')  # plot power loss
            ax2.yaxis.label.set_color(colors[3])
            ax2.tick_params(axis='y', colors=colors[3])
            ax2.spines['right'].set_position(('outward', 3))  # adjust the position of the second axis 
            ax2.set_ylabel(data_label, rotation=90, fontsize=10)
            
        fig.savefig(Directory + "/output/" + test + ".png", bbox_inches='tight')
        plt.tight_layout()
        PdfPages.savefig()

    def diode_calibration(self, diodes=["A"], Directory=False, PdfPages=False):
        '''
        The function plots the calibration results for the PN diodes
        Input Directory = Dirctory + diode_calibration/cern_calibration/
        diodes is an array of strings represents the diodes name A, B and C.
        '''
        self.log.info('Calibration results for the diodes')
        fig = plt.figure()
        gs = gridspec.GridSpec(2, 1, height_ratios=[3.9, 2])
        ax = plt.subplot(gs[0])
        ax2 = plt.subplot(gs[1])
        factor_row = []
        for d in diodes:
            dep = []
            dose = []
            bkg = []
            current = []
            factor = []
            with open(Directory + "diode_calibration/cern_calibration/" + d + ".csv", 'r')as data:
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
            ax.errorbar(dose, current, xerr=0.0, yerr=0.0, fmt='o', color=colors[diodes.index(d)], markersize=3)  # plot points
            sig2 = [0.4 * current[k] for k in range(len(current))]
            
            popt2, pcov = curve_fit(an.linear, dose, current, sigma=sig2, absolute_sigma=True, maxfev=5000, p0=(1, 1))
            chisq2 = an.red_chisquare(np.array(current), an.linear(dose, *popt2), np.array(sig2), popt2)
            line_fit_legend_entry = "Diode " + d + ':%.4fx + %.4f' % (popt2[0], popt2[1])
            ax.plot(dose, an.linear(dose, *popt2), linestyle="--",
                    color=colors[diodes.index(d)], label=line_fit_legend_entry)
        ax.set_ylabel('Dose rate [$Mrad(sio_2)/hr$]')
        ax.set_xlabel(r'Current [$\mu$ A]')
        ax.set_title('(Diode calibration at %s and %s)' % ("40Kv", "50mA"), fontsize=11)
        rows = ["Diode A", "Diode B", "Diode C"]
        columns = ["3 cm", "5 cm", "8 cm", "Mean factor"]
        ax2.table(cellText=[np.round(factor_row[0:4], 3), np.round(factor_row[4:8], 3),
                            np.round(factor_row[8:12], 3)],
                  rowLabels=rows,
                  rowColours=colors[0:3],
                  colColours=["lightgray", "lightgray", "lightgray", "lightgray"],
                  colLabels=columns, cellLoc='center', rowLoc='center', loc='center', fontsize=7)
        plt.subplots_adjust(bottom=0.1)
        ax2.set_xlabel(r'Calibration factors')
        ax2.set_axis_off()
        ax.grid(True)
        ax.legend()
        fig.savefig(Directory + "/diode_calibration/cern_calibration/diode_calibration.png", bbox_inches='tight')
        plt.tight_layout()
        PdfPages.savefig()

    def calibration_temprature(self, data=None, PdfPages=False, Directory=False):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax2 = ax.twinx()
        Factor = 9.62  # Calibration Factor
        plot_lines = []
        with tb.open_file(data) as in_file:
            temprature_dose = in_file.root.temprature_dose[:]
            time = temprature_dose["time"]
            current = temprature_dose["current"] * 10**6
            temprature = temprature_dose["temprature"]
        temp = ax2.errorbar(time, temprature, yerr=0.0, color=colors[0], fmt='-')
        curr = ax.errorbar(time[1:], current[1:], fmt='-', color=colors[1])
        ax2.set_ylabel('Temprature[$^oC$]')
        ax.set_ylabel('Current [$\mu$ A]')
        ax.set_xlabel('Time [Seconds]')
        ax.grid(True)
        ax.set_ylim([0, 1])
        plot_lines.append([temp, curr])
        plt.legend(plot_lines[0], ["temprature", "mean current=%0.2f $\mu$ A" % np.mean(current)])
        plt.savefig(Directory + 'without_Al_Filter/temprature/temprature_dose.png')
        plt.tight_layout()
        PdfPages.savefig()
                
    def opening_angle(self, Directory=False, Unknown_diameter=np.linspace(3, 10, 20), PdfPages=PdfPages, tests=["without_Al_Filter"]):
        '''
        To get the estimated beam diameter relative to the depth
        '''
        self.log.info('Estimate the beam diameter relative to the depth')
        for j in range(len(tests)):
            r = []
            h = []
            std = []
            with open(Directory + tests[j] + "/opening_angle/opening_angle_" + tests[j] + ".csv", 'r')as data:
                reader = csv.reader(data)
                next(reader)
                for row in reader:
                    h = np.append(h, float(row[0]))  # Distance from the source
                    r = np.append(r, float(row[1]))  # Diameter of the beam
                    std = np.append(std, float(row[2]))  # Diameter of the beam
            fig2 = plt.figure()
            fig2.add_subplot(111)
            ax2 = plt.gca()
            ax2.errorbar(h, r, xerr=0.0, yerr=std, fmt='o', color='black', markersize=1, ecolor='black')  # plot points

            popt, pcov = curve_fit(an.linear, h, r, sigma=std, absolute_sigma=True, maxfev=5000, p0=(1, 1))
            chisq2 = an.red_chisquare(np.array(r), an.linear(h, *popt), np.array(std), popt)
            line_fit_legend_entry = 'line fit: mh + c\n m=$%.3f\pm%.3f$\nc=$%.3f\pm%.3f$' % (popt[0], np.absolute(pcov[0][0]) ** 0.5, popt[1], np.absolute(pcov[1][1]) ** 0.5)

            ax2.plot(h, an.linear(h, *popt), '-', lw=1, label=line_fit_legend_entry, markersize=9)
            cmap = plt.cm.get_cmap('viridis', 15)
            h_space = np.linspace(h[0], h[-1], 50)
            # the function uses the fit parameters in dose_depth_scan
            a, b, c = self.dose_depth(tests=[tests[j]], Directory=Directory, PdfPages=PdfPages)
#             sc = ax2.scatter(h_space, self.linear(h_space, *popt), c=self.Inverse_square(h_space, a=a, b=b, c=c),
#                              cmap=cmap, s=50,)
#             cb = fig2.colorbar(sc, ax=ax2, orientation='horizontal')
#             cb.ax.invert_xaxis()
#             cb.set_label("Dose rate [$Mrad/hr$]")
            ax2.set_title('Radius covered by beam spot %s (40 kV and 50 mA)' % (tests[j]), fontsize=12)
            ax2.grid(True)
            ax2.legend()
            ax2.set_ylabel('Radius (r) [cm]')
            ax2.set_xlabel('Distance from the  collimator holder(h) [cm]')
            fig2.savefig(Directory + tests[j] + '/opening_angle/depth_radius_linear_' + tests[j] + '.png', bbox_inches='tight')
            PdfPages.savefig()

            r_space = an.linear(h_space, m=popt[0], c=popt[1])
            fig = plt.figure()
            fig.add_subplot(111)
            ax = plt.gca()
            for i in range(len(r_space)):
                x, y = np.linspace(-r_space[i], r_space[i], 2), [h_space[i] for _ in np.arange(2)]
                plt.plot(x, y, linestyle="solid")
            ax.text(0.95, 0.90, "$\Theta^{rad}$ = %.3f$\pm$ %.3f\n $h_{0}$=%.3f$\pm$ %.3f" % (2 * popt[0], 2 * np.absolute(pcov[0][0]) ** 0.5, popt[1] / (popt[0]), np.absolute(pcov[1][1]) ** 0.5 / popt[0]),
                    horizontalalignment='right', verticalalignment='top', transform=ax.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
            ax.set_title('Diameter covered by beam spot %s' % (tests[j]), fontsize=12)
            ax.invert_yaxis()
            ax.set_xlabel('Diameter (d) [cm]')
            ax.set_ylabel('Height from the the collimator holder(h) [cm]')
            ax.grid(True)
            fig.savefig(Directory + tests[j] + '/opening_angle/opening_angle_' + tests[j] + '.png', bbox_inches='tight')
            PdfPages.savefig()        

    def dose_depth(self, Directory=False, PdfPages=False, Voltage="40 kV", current="50 mA", stdev=0.2, tests=["without_Al_Filter"], theta=0.16):
        '''
        Relation between the depth and  the Dose rate
        '''
        self.log.info('Relation between the depth and  the Dose rate')
        for i in range(len(tests)):
            fig = plt.figure()
            ax = fig.add_subplot(111)
            Factor = 9.81  # Calibration Factor
            height = []
            y1 = []
            b1 = []
            with open(Directory + tests[i] + "/dose_depth/dose_depth_" + tests[i] + ".csv", 'r')as data:
                reader = csv.reader(data)
                next(reader)
                for row in reader:
                    height = np.append(height, float(row[0]))  # Distance from the source
                    y1 = np.append(y1, (float(row[1])))  # Dose rate
                    b1 = np.append(b1, (float(row[2])))  # Background
            y1 = [y1[k] - b1[k] for k in range(len(y1))]  # Subtract Background

            sig = [stdev * y1[k] for k in range(len(y1))]
            y1 = [y1[k] * Factor for k in range(len(y1))]
            popt1, pcov = curve_fit(an.Inverse_square, height, y1, sigma=sig, absolute_sigma=True, maxfev=500, p0=(300, 6, 0))
            chisq1 = an.red_chisquare(np.array(y1), an.Inverse_square(np.array(height), *popt1), sig, popt1)
            ax.errorbar(height, y1, yerr=sig, color=colors[i + 1], fmt='o', label=tests[i], markersize='4')
            xfine = np.linspace(height[0], height[-1], 100)  # define values to plot the function
            a, b, c = popt1[0], popt1[1], popt1[2]

            a_err, b_err, c_err = np.absolute(pcov[0][0]) ** 0.5, np.absolute(pcov[1][1]) ** 0.5, np.absolute(pcov[2][2]) ** 0.5
            #ax.plot(xfine, self.Inverse_square(xfine, *popt1), colors[i + 1], label='Fit parameters:\n a=%.2f$\pm$ %.2f\n b=%.2f$\pm$ %.2f\n c=%.2f$\pm$ %.2f\n' % (a, a_err, b, b_err, c, c_err))
            ax.text(0.9, 0.56, r'$R= \frac{a}{(h+b)^2}-c$',
                    horizontalalignment='right', verticalalignment='top', transform=ax.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))
            # print "The dose rate at %.2f cm depth is " %(45) + str(popt1[0]/(45+popt1[1])**2)+" Mrad/hr "+tests[i]
            ax.set_xlabel('Distance from the collimator holder(h) [cm]')
            ax.set_title('Dose rate vs distance %s at  (%s and %s)' % (tests[i], Voltage, current), fontsize=11)
            ax.set_ylabel('Dose rate (R) [$Mrad(sio_2)/hr$]')
            ax.set_xlim([0, max(height) + 8])
            ax.grid(True)
            ax.legend(loc="upper right")
            ax.ticklabel_format(useOffset=False)
            fig.savefig(Directory + tests[i] + "/dose_depth/dose_depth_" + tests[i] + ".png", bbox_inches='tight')  # 1.542
            plt.tight_layout()
            PdfPages.savefig()
            cmap = plt.cm.get_cmap('viridis', 15)
            sc = ax.scatter(xfine, an.Inverse_square(xfine, *popt1), c=an.Inverse_square(xfine, a=a, b=b, c=c), cmap=cmap, s=50,)
            fig.savefig(Directory + tests[i] + "/dose_depth/dose_depth_color_" + tests[i] + ".png", bbox_inches='tight')

  # check the fit
            fig = plt.figure()
            ax2 = fig.add_subplot(111)
            inverse = an.Inverse_square(height, *popt1)
            ax.errorbar(inverse, y1, xerr=0.0, yerr=0.0, fmt='o', color='black', markersize=3)  # plot points
            line_fit, pcov = np.polyfit(inverse, y1, 1, full=False, cov=True)
            fit_fn = np.poly1d(line_fit)
            line_fit_legend_entry = 'line fit: ax + b\n a=$%.2f\pm%.2f$\nb=$%.2f\pm%.2f$' % (line_fit[0], np.absolute(pcov[0][0]) ** 0.5, line_fit[1], np.absolute(pcov[1][1]) ** 0.5)
            ax2.plot(inverse, fit_fn(inverse), '-', lw=2, color=colors[i + 1], label=tests[i])
            ax2.set_ylabel('Dose rate (R) [$Mrad(sio_2)/hr$]', fontsize=9)
            ax2.set_xlabel(r'$R= \frac{a}{(h+b)^2}-c$', fontsize=9)
            ax2.set_title('(%s and %s)' % (Voltage, current), fontsize=11)
            ax2.grid(True)
            ax2.legend(loc="upper right")
            fig.savefig(Directory + tests[i] + "/dose_depth/dose_depth_inverse_" + tests[i] + ".png", bbox_inches='tight')
            plt.tight_layout()
            PdfPages.savefig()
        return a, b, c

    def dose_current(self, Directory=False, PdfPages=False, stdev=0.06, depth=[0], table=True,Voltages=["40kV"]):
        ''', 
        To get the calibration curves for each current
        For each Measurement you make you need to replace the numbers 0 in Background, Factor, .....by your measurement
        Background =  array of background estimated for each depth
#         '''
        self.log.info('get the calibration curves for each current')
        styles = ['-', '--']
        for i in range(len(depth)):
            if table:
                gs = gridspec.GridSpec(2, 1, height_ratios=[3.9, 2])
                ax = plt.subplot(gs[0])
                ax2 = plt.subplot(gs[1])
            else: 
                fig = plt.figure()
                ax = fig.add_subplot(111)
            volt_row = []
            fit_para = []
            for volt in Voltages:
                x1 = []
                y1 = []
                y2 = []
                bkg_y1 = []
                bkg_y2 = []
                Factor = []
                difference = []
                with open(Directory + "dose_current/" + depth[i] + "/" + volt + ".csv", 'r')as data:  # Get Data for the first Voltage
                    reader = csv.reader(data)
                    next(reader)
                    for row in reader:
                        x1 = np.append(x1, float(row[0]))
                        y1 = np.append(y1, (float(row[1]) - float(row[2])) * float(row[5]))
                        bkg_y1 = np.append(bkg_y1, float(row[2]))

                        y2 = np.append(y2, (float(row[3]) - float(row[4])) * float(row[5]))  # Data with Al filter
                        bkg_y2 = np.append(bkg_y2, float(row[4]))
                        Factor = np.append(Factor, float(row[5]))
                        difference = np.append(difference, (float(row[3]) - float(row[1])) / float(row[3]) * 100)
                    logging.info("Start Plotting %s cm" % (depth[i]))
                    # Calibrating data with Filter
                    sig1 = [stdev * y1[k] for k in range(len(y1))]
                    popt1, pcov = curve_fit(an.linear, x1, y1, sigma=sig1, absolute_sigma=True, maxfev=5000, p0=(1, 1))
                    chisq1 = an.red_chisquare(np.array(y1), an.linear(x1, *popt1), np.array(sig1), popt1)
                    ax.errorbar(x1, y1, yerr=sig1, color=colors[Voltages.index(volt)], fmt='o')
                    label1 = "%s,%s" % (volt, "Al Filter")
                    ax.plot(x1, an.linear(x1, *popt1), linestyle=styles[1],
                            color=colors[Voltages.index(volt)], label=label1)
                    # Calibrating data without Filter
                    sig2 = [stdev * y2[k] for k in range(len(y2))]
                    popt2, pcov = curve_fit(an.linear, x1, y2, sigma=sig2, absolute_sigma=True, maxfev=5000, p0=(1, 1))
                    chisq2 = an.red_chisquare(np.array(y2), an.linear(x1, *popt2), np.array(sig2), popt2)
                    ax.errorbar(x1, y2, yerr=sig2, color=colors[Voltages.index(volt)], fmt='o')
                    label2 = "%s,%s" % (volt, "No Filter")
                    ax.plot(x1, an.linear(x1, *popt2), linestyle=styles[0],
                            color=colors[Voltages.index(volt)], label=label2)
                    filter = [volt + ", Filter", volt + ", No Filter"]
                    for f in arange(0, 2):
                        volt_row = np.append(volt_row, filter[f])
                    fit_para = np.append(fit_para, (popt1, popt2))
            ax.text(0.95, 0.90, "y[$Mrad(sio_2)/hr$]= m$x$+c",
                    horizontalalignment='right', verticalalignment='top', transform=ax.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
            plt.ticklabel_format(useOffset=False)
            plt.xlim(0, 60)
            ax.set_title('Calibration curve for ' + depth[i], fontsize=12)
            ax.set_ylabel('Dose rate [$Mrad(sio_2)/hr$]')
            ax.grid(True)
            if table:
                rows = volt_row
                columns = ['a', 'b']
                ax2.table(cellText=[np.round(fit_para[0:2], 2), np.round(fit_para[2:4], 2), np.round(fit_para[4:6], 2), np.round(fit_para[6:8], 2)],
                          rowLabels=rows,
                          colColours=["lightgray", "lightgray", "lightgray"],
                          colLabels=columns, cellLoc='center', rowLoc='center', loc='center', fontsize=8)
                plt.subplots_adjust(bottom=0.1)
                ax2.set_axis_off()
            ax.legend()  # prop={'size': 8}
            ax.set_xlabel('Tube current [mA]')
            plt.tight_layout()
            plt.savefig(Directory + "dose_current/" + depth[i] + '/dose_current_' + depth[i] + ".png", bbox_inches='tight')
            PdfPages.savefig()

    def dose_drop(self, Directory=False, PdfPages=False, stdev=0.06, depth=[0]):
        '''
        Dose drop after Al filter at
        '''
        self.log.info('Dose drop after filters')
        
        Voltages = ["40KV", "30KV"]
        styles = ['-', '--']
        for i in range(len(depth)):
            fig = plt.figure()
            fig.add_subplot(111)
            ax = plt.gca()
            volt_row = []
            fit_para = []
            for volt in Voltages:
                x1 = []
                y1 = []
                y2 = []
                bkg_y1 = []
                bkg_y2 = []
                Factor = []
                difference = []
                with open(Directory + "dose_current/" + depth[i] + "/" + volt + ".csv", 'r')as data:  # Get Data for the first Voltage
                    reader = csv.reader(data)
                    next(reader)
                    for row in reader:
                        x1 = np.append(x1, float(row[0]))  # Voltage
                        y1 = np.append(y1, (float(row[1]) - float(row[2])) * float(row[5]))  # Data with Al filter
                        y2 = np.append(y2, (float(row[3]) - float(row[4])) * float(row[5]))  # Data without Al filter
                        Factor = np.append(Factor, float(row[5]))
                        difference = np.append(difference, ((float(row[6])) * 100 / float(row[3])))  # (with-bkg) -(without-bkg)
                ax.errorbar(x1, difference, yerr=0.0, color=colors[Voltages.index(volt)], fmt='o', label="%s" % volt)
            ax.set_title('Dose drop after Al filter at ' + depth[i], fontsize=12)
            ax.set_ylabel('Dose rate drop [%]')
            ax.set_xlabel('Tube current [mA]')
            ax.legend(prop={'size': 10})
            ax.grid(True)
            plt.savefig(Directory + "dose_current/" + depth[i] + '/dose_current_drop' + depth[i] + ".png", bbox_inches='tight')
            PdfPages.savefig()

    def dose_voltage(self, Directory=False, PdfPages=False, Depth="8cm", test="without_Al_Filter", kafe_Fit=False, table=True):
        '''
        Effect of tube Voltage on the Dose
        '''
        y1 = []
        x1 = []
        Dataset = []
        kafe_Fit = []

        if table:
            gs = gridspec.GridSpec(2, 1, height_ratios=[3.5, 2])
            ax = plt.subplot(gs[0])
            ax2 = plt.subplot(gs[1])
        else:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        Current = ["10mA", "20mA", "30mA", "40mA"]
        col_row = plt.cm.BuPu(np.linspace(0.3, 0.9, len(Current)))
        fit_para = []
        for i in range(len(Current)):
            x = []
            y = []
            Background = [0.00801e-06]
            Factor = [9.76]
            with open(Directory + test + "/dose_voltage/" + Depth + "/" + Current[i] + ".csv", 'r')as data1:
                reader = csv.reader(data1)
                next(reader)
                for row in reader:
                    x = np.append(x, float(row[0]))
                    y = np.append(y, (float(row[1]) - Background[0]) * Factor[0])
            x1.append(x)
            y1.append(y)
            stdev = 0.06
            sig = [stdev * y1[i][k] for k in range(len(y1[i]))]
            Dataset = np.append(Dataset, build_dataset(x1[i], y1[i], yabserr=sig, title='I=%s' % Current[i], axis_labels=['Voltage (kV)', '$Dose rate [Mrad(sio_2)/hr]$']))
            popt, pcov = curve_fit(an.quadratic, x1[i], y1[i], sigma=sig, absolute_sigma=True, maxfev=5000, p0=(1, 1, 1))
            xfine = np.linspace(0., 60., 100)
            ax.plot(xfine, an.quadratic(xfine, *popt), color=col_row[i])
            chisq = an.red_chisquare(np.array(y1[i]), an.quadratic(x1[i], *popt), np.array(sig), popt)
            ax.errorbar(x1[i], y1[i], yerr=sig, color=col_row[i], fmt='o',
                        label='I=%s' % (Current[i]))
            for par in popt:
                fit_para = np.append(fit_para, par)
            ax.text(0.95, 0.90, "y[$Mrad(sio_2)/hr$]= a$\mathrm{x}^2$ + bx+c",
                    horizontalalignment='right', verticalalignment='top', transform=ax.transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
        ax.set_title('Effect of the tube voltage at ' + Depth + " " + "for unfiltered beam", fontsize=12)
        ax.set_ylabel('Dose rate [$Mrad(sio_2)/hr$]')
        ax.set_xlabel('Voltage (kV)')
        ax.grid(True)
        ax.legend()
        plt.ticklabel_format(useOffset=False)
        ax.set_xlim(xmin=5)
        ax.set_ylim(ymin=0)
        rows = Current
        columns = ['a', 'b', 'c']
        col = plt.cm.BuPu(np.linspace(0.1, 0.5, len(columns)))
        if table:
            ax2.table(cellText=[np.round(fit_para[0:3], 3), np.round(fit_para[3:6], 3), np.round(fit_para[6:9], 3), np.round(fit_para[9:12], 3)],
                      rowLabels=rows,
                      rowColours=col_row,  # colors[0:4],
                      colColours=["lightgray", "lightgray", "lightgray"],
                      animated=True,
                      colLabels=columns, cellLoc='center', rowLoc='center', loc='center', fontsize=12)
            plt.subplots_adjust(bottom=0.1)
            ax2.set_axis_off()
        plt.savefig(Directory + test + "/dose_voltage/" + Depth + "/dose_voltage_" + Depth + ".png", bbox_inches='tight')
        PdfPages.savefig()

        if kafe_Fit:
            # Another fitting using Kafe fit
            for Data in Dataset:
                kafe_Fit = np.append(kafe_Fit, Fit(Data, quadratic_3par))
            for fit in kafe_Fit:
                fit.do_fit()
            kafe_plot = Plot(kafe_Fit[2], kafe_Fit[3])
            kafe_plot.plot_all(show_data_for='all', show_band_for=0)
            kafe_plot.save(Directory + test + "/dose_voltage/" + Depth + "/dose_voltage_" + Depth + "_kafe_Fit.png")
            PdfPages.savefig()
            
       
    def close(self, PdfPages=False):
            PdfPages.close()


# A special class to plot the attenuation coefficient for several materials
class Attenuation(object):
     
    def __init__(self):
        print("Plotting Attenuation class initialized")
    
    def mass_attenuation_coeff(self, Directory=False, PdfPages=False, targets=False):
        for target in targets:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            data = loadtxt(Directory + target + 
                           "/mass_attenuation_coeff_in_detail_" + target + ".dat")
            x = data[:, 0]  # Energy in Kev
            # total mass attenuation coeff with coherent scattering
            y = data[:, 6]
            # mass attenuation coeff due to photoelectric effect
            p = data[:, 3]
            # mass attenuation coeff due to compton (incoherent) scattering
            i = data[:, 2]
            # mass attenuation coeff due to rayleigh (coherent) scattering
            r = data[:, 1]
            # mass attenuation coeff due to pair production in nuclei field
            ppn = data[:, 4]
            # mass attenuation coeff due to pair production in electron field
            ppe = data[:, 5]            
            plt.plot(x * 10 ** 3, ppe, ':', color='orange',
                     label='Pair production (electron)')
            plt.plot(x * 10 ** 3, ppn, ':', color='grey',
                     label='Pair production (nuclei)')
            # plt.plot(x*10**3, r, '--', color='green', label='Coherent scattering')
            plt.plot(x * 10 ** 3, i, '--', color='#006381',
                     label='Compton scattering')
            plt.plot(x * 10 ** 3, p, '-.', color='#7e0044',
                     label='Photoelectric effect')
            plt.plot(x * 10 ** 3, y, '-', color='black', label='Total')
            
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xlabel('Photon energy [keV]')
            ax.grid(True)
            ax.set_ylabel('Mass attenuation coefficient [cm$^2$/g]')
            ax.set_title(r'Mass attenuation coefficient for %s ' % 
                         target, fontsize=11)
            ax.legend(loc="upper right")
            plt.xlim(1, 1000000)
            plt.tight_layout()
            plt.savefig(Directory + target + "/mass_attenuation_coeff_" + 
                        target + ".png", bbox_inches='tight')
            PdfPages.savefig()

    def attenuation_thickness(self, Directory=False, PdfPages=False, targets=False, logx=True, logy=True, color=colors):

        for target in targets:
            Density = []
            Mu = []
            Energy = []
            x = np.arange(0, 20, 0.001)
            y = []
            with open(Directory + target + "/Attenuation_Energy_" + target + ".csv", 'r')as parameters:
                fig = plt.figure()
                ax = fig.add_subplot(111)
                reader = csv.reader(parameters)
                next(reader)
                for row in reader:
                    Density = np.append(Density, float(row[0]))
                    Mu = np.append(Mu, float(row[1]))
                    Energy = np.append(Energy, float(row[2]))
                for i in np.arange(len(Energy)):
                    y = np.exp((-1) * Mu[i] * Density[0] * x)
                    ax.plot(x, y, ':', label=str(Energy[i]) + 'Kev')
                    if ((Energy[i] == 60.0) and (target != "Be")):
                        l = np.log(10 ** (-9)) / ((-1) * Mu[i] * Density[0])
                        print ("to get 10e-9 of the initial intensity in %s  %5.3f cm shielding is needed" % (target, l))
                        ax.annotate("%5.3f cm" % l, xy=(l, 10 ** (-9)), xytext=(l + 1, 10 ** (-8)),
                                    arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.5", relpos=(.6, 0.), fc="w"))
                        # Define the shielding thickness
                        ax.axvline(x=l, linewidth=2,
                                   color='#d62728', linestyle='solid')
                    # ax.axhline(y=10**(-9), linewidth=2, color='#d62728', linestyle='solid')# Define the shielding thickness
                    ax.set_ylim(bottom=10 ** (-10))
                    ax.set_xlim(0.001, 150)
                    # ax.set_yscale('log')
            if target == "Be":
                ax.axvline(x=0.03, linewidth=2,
                           color='#d62728', linestyle='solid')
                ax.annotate("%5.3f cm" % 0.03, xy=(0.03, 0), xytext=(0.03 + 0.1, 0.2),
                            arrowprops=dict(arrowstyle="-|>",
                                            connectionstyle="arc3,rad=-0.5", relpos=(.2, 0.), fc="w"))
                ax.set_xlim(0.001, 10)
            if logx:
                ax.set_xscale('log')

            ax.grid(True)
            ax.set_xlabel(target + ' Thickness (cm)')
            ax.set_ylabel('Transmission $I$/$I_0$ ')
            ax.legend(loc='upper right')
            ax.set_title(r'Transmission of x rays through %s Filter' % 
                         target, fontsize=11)
            plt.tight_layout()
            plt.savefig(Directory + target + "/Thickness_" + 
                        target + ".png", bbox_inches='tight')
            PdfPages.savefig()

    def attenuation_Energy(self, Directory=False, PdfPages=False, targets=False, logx=True, logy=True, n=False, x_offset=False, y_offset=False, color=colors):

        fig = plt.figure()
        ax = fig.add_subplot(111)
        for i in np.arange(len(targets)):
            data = loadtxt(
                Directory + targets[i] + "/mass_attenuation_coeff_in_detail_" + targets[i] + ".dat")
            x = data[:, 0]  # Energy in Kev
            # total mass attenuation coeff with coherent scattering
            y = data[:, 6]

            ax.plot(x * 10 ** 3, y, '-', color=color[i], label=targets[i])
        ax = plt.gca()  # .invert_xaxis()
        for j, txt in enumerate(n):
            ax.annotate(
                txt, xy=(x_offset[j], y_offset[j]), color=color[j], size=6)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Photon energy [keV]')
        ax.grid(True)
        ax.set_ylabel('Mass attenuation coefficient [cm$^2$/g]')
        # ax.set_title(r"Mass attenuation coefficients as a function of Energy", fontsize=10)
        plt.ylim(1, 10000)
        plt.xlim(1, 60)
        ax.legend()
        plt.tight_layout()
        plt.savefig(Directory + "/attenuation_Energy_relation.png",
                    bbox_inches='tight')
        PdfPages.savefig()
        
    def close(self, PdfPages=False):
            PdfPages.close()
        
