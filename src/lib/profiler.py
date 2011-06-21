#-*- coding: utf-8 -*-

# profiler.py

# Copyright (c) 2011, see AUTHORS
# All rights reserved.

# This file is part of ProfileExtractor.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# Neither the name of the ProfileExtractor nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#-*- coding: utf-8 -*-

import matplotlib as mp
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.colors as cols

from PySide import QtCore, QtGui
from PySide.QtCore import *

from table import *
from normalizer import *

class Profiler(QThread):
    """
    """

    done = QtCore.Signal(str)

    def __init__(self, table, fname, verbose = False, legend = False, parent = None):
        """
        """
        super(Profiler, self).__init__(parent) 

        self.verbose = verbose
        self.legend = legend

        self.table = table
        self.table.zipIter = False

        self.fname = fname

    def run(self):
        """
        """

        self.drawProfile()

    def drawProfile(self):
        """
        """

        #self.table.invertAxis()
        
        fig = Figure(figsize = (20, 8))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        thickerLine = []

        for header, l, color, thickness in zip(self.table.lineHeaders, self.table,
                                               self.table.colors, self.table.thickness):
            if thickness == 1:
                ax.plot(l, label = header, color = color, lw = thickness, alpha = 1)
            else:
                thickerLine.append({ 'header' : header,
                                     'l' : l,
                                     'color' : color,
                                     'thickness' : thickness })

        for dic in thickerLine:
            ax.plot(dic['l'], label = dic['header'], color = dic['color'], lw = dic['thickness'], alpha = 0.8)

        ax.set_xticks(range(len(self.table.headers)))
        ax.set_xticklabels(self.table.headers)
        fig.autofmt_xdate()

        ax.set_xlabel('Parameters')
        ax.set_ylabel('Normalized z-value')
        ax.set_title('Profile')
        fig.subplots_adjust(bottom = 0.45, wspace = 0, hspace = 0)

        # Setup the grid
        ax.xaxis.set_major_locator(mp.ticker.MultipleLocator(1))
        ax.xaxis.set_view_interval(ax.xaxis.get_data_interval()[0],
                                   ax.xaxis.get_data_interval()[1], ignore = True)
        #ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
        # #ax.xaxis.set_minor_locator(MultipleLocator(5))
        # ax.yaxis.set_major_locator(mp.ticker.MultipleLocator(1))
        # #ax.yaxis.set_minor_locator(MultipleLocator(0.1))
        ax.grid(color = 'black', linestyle='-.', linewidth=0.5)

        # # Setup the legend
        # if self.legend and len(self.table) != 0:
        #     #fig.legend((ax, ax), ('Line 1', 'Line 2'), 'upper left')
        #     leg = ax.legend(fancybox = True, loc = 'right',
        #                     shadow = True, title = 'Legend',
        #                     bbox_to_anchor=(1.05, 0.5), borderaxespad=0.)
        #     leg.get_frame().set_alpha(0.5)

        #show()
        canvas.print_figure(self.fname, dpi = 140)

        self.done.emit(self.fname)
        
