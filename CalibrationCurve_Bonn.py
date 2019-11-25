from __future__ import division
from kafe import *
from kafe.function_library import quadratic_3par
from numpy import loadtxt, arange
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.backends.backend_pdf import PdfPages
import csv
from scipy.optimize import curve_fit
import tables as tb
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker
import itertools
from matplotlib.colors import LogNorm
from matplotlib import pyplot as p
from mpl_toolkits.mplot3d import Axes3D    # @UnusedImport
from math import pi, cos, sin
import logging
from scipy.linalg import norm
import os
import matplotlib as mpl
from matplotlib import gridspec
import seaborn as sns
sns.set(style="white", color_codes=True)
from matplotlib.patches import Circle
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredDrawingArea
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import matplotlib.transforms as mtransforms
from matplotlib.ticker import NullFormatter
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.patches as patches
import pylab as P

from analysis import plotting
from analysis import analysis

loglevel = logging.getLogger('').getEffectiveLevel()
from analysis import logger
np.warnings.filterwarnings('ignore')
log = logger.setup_derived_logger('Plotting results')


class Calibration_Curves():


    def Plot_Beam_profile_2d(self, Directory=False, PdfPages=False, depth=None):
        '''
        Make a 2d scan at specific depth
        '''
        Factor = 9.847  # diode A
        # Factor = 9.817  # diode B
        Background = 5.7 * 10**(-9)  # nA
        binwidth = 1
        for d in range(len(depth)):
            with tb.open_file(Directory + "without_Al_Filter/beamspot/" + depth[d] + "/beamspot_" + depth[d] + ".h5", 'r') as in_file:
                beamspot = in_file.root.beamspot[:]
                beamspot = (beamspot - Background) * 1000000 * Factor
                mid_z, mid_x = np.int(beamspot.shape[0] / 2), np.int(beamspot.shape[1] / 2)
            if (depth[d] == "3cm") or (depth[d] == "3cm_Vfilter") or (depth[d] == "3cm_Zrfilter"):
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
            # put the mean value for each quad
#             mean1 = np.round(np.mean(beamspot[np.int(beamspot.shape[0]/2-r):np.int(beamspot.shape[0]/2),np.int(beamspot.shape[1]/2):np.int(beamspot.shape[1]/2)+r]),3)
#             mean2 = np.round(np.mean(beamspot[np.int(beamspot.shape[0]/2-r):np.int(beamspot.shape[0]/2),np.int(beamspot.shape[1]/2-r):np.int(beamspot.shape[1]/2)]),3)
#             mean3 = np.round(np.mean(beamspot[np.int(beamspot.shape[0]/2):np.int(beamspot.shape[0]/2+r),np.int(beamspot.shape[1]/2-r):np.int(beamspot.shape[1]/2)]),3)
#             mean4 = np.round(np.mean(beamspot[np.int(beamspot.shape[0]/2):np.int(beamspot.shape[0]/2+r),np.int(beamspot.shape[1]/2):np.int(beamspot.shape[1]/2+r)]),3)
#             mean=[mean2,mean3,mean1,mean4]
#
#             y_offset = [np.int(beamspot.shape[0]/2-r),np.int(beamspot.shape[0]/2+r),np.int(beamspot.shape[0]/2-r),np.int(beamspot.shape[0]/2+r)]
#             x_offset = [np.int(beamspot.shape[1]/2-r),np.int(beamspot.shape[1]/2-r),np.int(beamspot.shape[1]/2+r),np.int(beamspot.shape[1]/2+r)]
#
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
            plt.title("Beam profile at " + depth[d] + " from the collimator holder (%s and %s)" % ("40 kV", "50mA"), fontsize=12, y=1.7, x=-0.6)
            ax.set_xlabel('x [mm]')
            ax.set_ylabel('y[mm]')
            plt.savefig(Directory + "without_Al_Filter/beamspot/" + depth[d] + "/beamspot_" + depth[d] + "_2d.png")
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
            plt.savefig(Directory + "without_Al_Filter/beamspot/" + depth[d] + "/beamspot_percentile" + depth[d] + "_2d.png")

            PdfPages.savefig()

    def Plot_Beam_profile_3d(self, Directory=False, PdfPages=False, depth=[0]):
        '''
        Make a 3d scan at specific depth (The function is under updates)
        '''
        def f(x, y, Factor=9.62, Background=0.012, beamspot=None):
            return (beamspot[y, x] * 1000000 - Background) * Factor
        for d in range(len(depth)):
            with tb.open_file(Directory + "without_Al_Filter/beamspot/" + depth[d] + "/beamspot_" + depth[d] + ".h5", 'r') as in_file:
                beamspot = in_file.root.beamspot[:]
            y = np.linspace(0, beamspot.shape[0] - 1, 100, dtype=int)
            x = np.linspace(0, beamspot.shape[1] - 1, 100, dtype=int)
            X, Y = np.meshgrid(x, y)
            Z = f(X, Y, beamspot=beamspot)

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
            plt.savefig(Directory + "without_Al_Filter/beamspot/" + depth[d] + "/beamspot_" + depth[d] + "_3d.png")
            PdfPages.savefig()

    def power_2d(self, Directory=False, PdfPages=False, size_I=50, size_V=60, V_limit=50, I_limit=50):
        '''
        Calculate the power in each point of I and V
        '''

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

if __name__ == '__main__':
    global PdfPages
    Directory = "Calibration_Curves/"
    tests = ["without_Al_Filter", "with_Al_Filter"]
    depth = ["3cm", "5cm", "8cm", "51cm"]
    Voltages = ["40kV", "30kV"]
    PdfPages = PdfPages('output_data/CalibrationCurve_Bonn' + '.pdf')
    p =plotting.Plotting()
    p.diode_calibration(PdfPages=PdfPages, Directory=Directory, diodes=["A","B","C"])
    #p.calibration_temprature(data=Directory + "without_Al_Filter/temprature/temprature_dose.h5", Directory=Directory, PdfPages=PdfPages)
    p.opening_angle(Directory=Directory, tests=tests,PdfPages=PdfPages)
    p.dose_current(stdev=0.04, PdfPages=PdfPages, Directory=Directory, depth=depth, table=True,Voltages=Voltages)
    p.dose_drop(stdev=0.04, PdfPages=PdfPages, Directory=Directory,depth=depth)
    p.dose_voltage(PdfPages=PdfPages, Directory=Directory, test="without_Al_Filter", kafe_Fit=False, table=False)
    #scan.dose_depth(tests=tests, Directory=Directory, PdfPages=PdfPages, colors=colors)
#     scan.power_2d(PdfPages=PdfPages, Directory=Directory, V_limit=50, I_limit=50)
#     scan.Plot_Beam_profile_3d(Directory=Directory, PdfPages=PdfPages, depth=["3cm", "8cm", "51cm","60cm"])
    #scan.Plot_Beam_profile_2d(Directory=Directory, PdfPages=PdfPages, depth=["3cm", "3cm_Vfilter", "3cm_Zrfilter", "3cm_collimator", "8cm", "60cm"])
    p.close(PdfPages=PdfPages)
