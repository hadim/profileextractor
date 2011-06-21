#-*- coding: utf-8 -*-

# mainwindow.py

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

from ui_mainwindow import *

from ui.profiler.mainprofilerwidget import *
from ui.extractdatawidget import *
from ui.correlate.correlationwidget import *
from about import *

class MainWindow(QtGui.QWidget):

    def __init__(self, parent = None):
        """
        """
        
        super(MainWindow, self).__init__(parent)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.version = 'v2.9'

        self.setWindowTitle("Profile extractor (%s)" % self.version)

        self.extracterWidget = ExtractDataWidget()
        self.ui.tabWidget.addTab(self.extracterWidget, "Extract data from CellProfiler")

        self.profilerWidget = MainProfilerWidget()
        self.ui.tabWidget.addTab(self.profilerWidget, "Profile Visualizer")

        self.mainCorrelWidget = QTabWidget()
        self.ui.tabWidget.addTab(self.mainCorrelWidget, "Correlation Analyzer")
        
        self.correlParametersWidget = CorrelationWidget('parameters')
        self.correlWellsWidget = CorrelationWidget('wells')
        self.mainCorrelWidget.addTab(self.correlParametersWidget, "by parameters")
        self.mainCorrelWidget.addTab(self.correlWellsWidget, "by wells")

        self.extracterWidget.buildProfileSignal.connect(self.buildProfiler)
        self.extracterWidget.correlateDataSignal.connect(self.correlateData)

        self.ui.aboutButton.clicked.connect(self.showAbout)

        # Connect correlation and profiler widget
        self.correlWellsWidget.importWells.connect(self.profilerWidget.importWells)
        self.profilerWidget.pushControls.connect(self.correlWellsWidget.receiveControls)

        ## Uncomment for debug mode
        self.ui.tabWidget.setCurrentWidget(self.profilerWidget)

    def buildProfiler(self, filename):
        """
        """

        self.ui.tabWidget.setCurrentWidget(self.profilerWidget)
        self.profilerWidget.loadFile(filename)

    def correlateData(self,filename):
        """
        """

        self.ui.tabWidget.setCurrentWidget(self.mainCorrelWidget)
        self.correlParametersWidget.loadFile(filename)
        self.correlWellsWidget.loadFile(filename)


    def showAbout(self):
        """
        """

        self.about = AboutWidget(self.version)
        self.about.show()
        
        
