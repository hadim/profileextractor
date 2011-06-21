#-*- coding: utf-8 -*-

# mainprofilerwidget.py

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

from ui_mainprofilerwidget import *

from profilewidget import *
from wellswidget import *
from legendwidget import * 

from lib.table import *
from lib.profiler import *
from lib.normalizer import *
from lib.controlsMerger import *

import config as cfg
import re, os, sys, shutil

class MainProfilerWidget(QtGui.QWidget):
    """
    """

    pushControls = Signal(list, object)
    
    def __init__(self, parent = None):
        """
        """
        super(MainProfilerWidget, self).__init__(parent)
        
        self.ui = Ui_MainProfilerWidget()
        self.ui.setupUi(self)

        # Open .csv file and remove useless column
        self.table = Table()

        # Create widget to select wells
        self.containerWellsWidget = QWidget()
        self.layout = QVBoxLayout()
        self.containerWellsWidget.setLayout(self.layout)
        self.ui.splitter.insertWidget(0, self.containerWellsWidget)

        self.wellsWidget = WellsWidget()
        self.wellsWidget.refreshProfile.connect(self.updateProfile)

        self.updateButton = QPushButton("Update profile")
        self.updateButton.clicked.connect(self.updateProfile)
        
        self.layout.addWidget(self.wellsWidget)
        self.layout.addWidget(self.updateButton)

        # Create widget to display profile
        self.profileWidget = ProfileWidget()
        self.ui.splitter.insertWidget(0, self.profileWidget)

        # Connect button and other events
        self.ui.saveButton.clicked.connect(self.saveCurrentProfile)
        self.ui.saveCsvButton.clicked.connect(self.saveCurrentProfileCsv)
        self.ui.legendButton.clicked.connect(self.switchLegend)
        self.ui.loadButton.clicked.connect(self.openFile)
        self.ui.mergeButton.clicked.connect(self.mergeControls)

        self.selectedWells = []
        self.mergedControlsName = []
        self.controls = []
        self.legendWidget = None
        self.controlsMerged = False

        #self.loadFile("/data/results/shRNA-130411/extractedData.csv")
        self.loadFile("/data/fakeResults/resultsMedium/extractedData.csv")

    def openFile(self):
        """
        """

        fname, filterExt = QFileDialog.getOpenFileName(self,
                                                       "Load .csv file",
                                                       QDir.homePath(),
                                                       "All (*)")

        if fname:
            self.loadFile(fname)

    def loadFile(self, fname):
        """
        """
        # Open .csv file and remove useless column
        self.table = Table(fname)

        # Remove useless column and merge metadata columns
        self.table.remove_column_by_regex([cfg.displayed_column, cfg.metadata_column])
        self.table.merge_column_by_regex([cfg.metadata_column], "Experiment ID")

        # Normalize data
        self.table = Normalizer(self.table).normalize()

        # Set colors and thickness for each lines
        self.set_colors()
        self.set_thickness()

        self.wellsWidget.load(self.table)
        self.profileWidget.drawProfile(blank = True)
        

    def updateProfile(self):
        """
        Update current Table object with selected wells
        """

        self.selectedWells = self.wellsWidget.toDisplay
        self.controls = self.wellsWidget.controlWells

        self.wellsWidget.setEnabled(False)

        self.currentTable = Table()
        self.currentTable.headers = self.table.headers
        self.currentTable.colors = []
        self.currentTable.thickness = []

        # Build new table with selected wells
        i = 0
        for l in self.table:
            header = self.table.lineHeaders[i]
            if header in self.selectedWells:
                self.currentTable.data.append(l)
                self.currentTable.lineHeaders.append(header)
                self.currentTable.colors.append(self.table.colors[i])
                if header in self.controls:
                    self.currentTable.thickness.append(5)
                else:
                    self.currentTable.thickness.append(self.table.thickness[i])
            i += 1

        if self.profileWidget.isProfile:
            self.ui.saveButton.setEnabled(True)
            self.ui.saveCsvButton.setEnabled(True)
            self.ui.legendButton.setEnabled(True)
        else:
            self.ui.saveButton.setEnabled(False)
            self.ui.saveCsvButton.setEnabled(False)
            self.ui.legendButton.setEnabled(False)

        # Draw new table
        self.profileWidget.updateDone.connect(self.updateDone)
        self.profileWidget.drawProfile(self.currentTable)

    def updateDone(self,):
        """
        """

        self.wellsWidget.setEnabled(True)

        self.ui.saveButton.setEnabled(True)
        self.ui.saveCsvButton.setEnabled(True)
        self.ui.legendButton.setEnabled(True)

    def saveCurrentProfile(self):
        """
        """

        dest, filterExt = QFileDialog.getSaveFileName(self,
                                                      "Save File (png format)",
                                                      QDir.homePath(),
                                                      "Images (*.png)")

        if dest:
            src = self.profileWidget.tmpFile

            if ".png" not in dest:
                dest += ".png"

            if os.path.isfile(dest):
                os.remove(dest)
            shutil.copy2(src, dest)

            self.ui.statusBar.setText("Current profile has been successfully saved.")

    def saveCurrentProfileCsv(self):
        """
        """

        dest, filterExt = QFileDialog.getSaveFileName(self,
                                                      "Save File (csv format)",
                                                      QDir.homePath(),
                                                      "CSV files (*.csv)")

        if dest:
            src = QDir.currentPath() + QDir.separator() + self.profileWidget.tmpFile

            self.currentTable.write(dest)

            self.ui.statusBar.setText("Current profile has been successfully saved.")
            

    def switchLegend(self,):
        """
        """

        self.profileWidget.legend = not self.profileWidget.legend

        self.legendWidget = LegendWidget()
        self.legendWidget.populate(self.currentTable.lineHeaders, self.currentTable.colors)
        self.legendWidget.show()

    def set_colors(self):
        """
        """

        import colorsys

        N = len(self.table)
        HSV_tuples = []
        for x in range(N):
            col = (x*1.0/N, 1, 1)
            HSV_tuples.append(col)

        RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)

        self.table.colors = []
        for line, color in zip(self.table, RGB_tuples):
            self.table.colors.append(color)

    def set_thickness(self):
        """
        """

        self.table.thickness = []
        for line in self.table:
            self.table.thickness.append(1)

        
    def importWells(self):
        """
        """

        self.pushControls.emit(self.wellsWidget.controlWells, self.table)

    def mergeControls(self):
        """
        """

        self.controlsMerged = not self.controlsMerged

        if self.controlsMerged:
            self.ui.mergeButton.setText("Unmerge controls")
        else:
            self.ui.mergeButton.setText("Merge controls")

        controls = self.wellsWidget.controlWells

        if self.controlsMerged:

            merger = ControlsMerger(self.table, controls)
            self.table = merger.merge()

            # Save selected wells and controls wells
            selected = self.wellsWidget.toDisplay
            controls = self.controls
            controls += merger.controlsName

            self.wellsWidget.load(self.table)

            for c in controls:
                self.wellsWidget.itemSignal(c, 'singleClick')
                self.wellsWidget.itemSignal(c, 'doubleClick')
                
            for s in selected:
                self.wellsWidget.itemSignal(s, 'singleClick')
            
            self.updateProfile()

            self.mergedControlsName = merger.controlsName

        else:

            self.table.remove_lines_by_name(self.mergedControlsName)
            self.wellsWidget.load(self.table)
            self.updateProfile()
            
        
