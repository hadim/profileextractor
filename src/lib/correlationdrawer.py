#-*- coding: utf-8 -*-

# correlationdrawer.py

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

from PySide import QtCore, QtGui
from PySide.QtCore import *
from PySide.QtGui import *

from table import *
from normalizer import *

import config as cfg

class CorrelationDrawer(QThread):
    """
    """

    done = QtCore.Signal(str, str)

    def __init__(self, vec1, vec2, name1, name2, coef, parent = None):
        """
        """
        super(CorrelationDrawer, self).__init__(parent) 

        self.vec1 = vec1
        self.vec2 = vec2
        self.name1 = name1
        self.name2 = name2
        self.coef = coef

        self.fname = QDir.tempPath() + QDir.separator() + "tmp_ProfileWidget.png"

        self.draw()

    def run(self):
        """
        """

        self.draw()

    def draw(self, mode = 'correlation'):
        """
        """
	
        fig = Figure()#figsize = (20, 8))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        for v1, v2 in zip(self.vec1, self.vec2):
            ax.scatter(float(v1), float(v2))

        ax.set_xlabel(self.name1)
        ax.set_ylabel(self.name2)

        if mode == 'correlation':
            ax.set_title('Pearson correlation coefficient = %.2f' % float(self.coef))
        elif mode == 'distance':
            ax.set_title('Euclidian distance = %.2f' % float(self.coef))
        # plt.subplots_adjust(bottom = 0.45, wspace = 0, hspace = 0)

        #show()
        canvas.print_figure(self.fname, dpi = 140)
        self.done.emit(self.fname, self.coef)


