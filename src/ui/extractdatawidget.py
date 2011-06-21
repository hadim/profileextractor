#-*- coding: utf-8 -*-

# extractdatawidget.py

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

from ui_extractdatawidget import *

import config as cfg
from lib.utils import *
from lib.stats import *
from lib.extracter import *

import os, csv, sys

class ExtractDataWidget(QtGui.QWidget, Ui_ExtractDataWidget):
    """
    """

    buildProfileSignal = QtCore.Signal(str)
    correlateDataSignal = QtCore.Signal(str)
    
    def __init__(self, parent = None):
        super(ExtractDataWidget, self).__init__(parent)
        
        self.setupUi(self)
        
        self.ok = False
        self.resultsFolder = None
        self.verbose = cfg.verbose
        self.fullExtractedFile = None

        self.progressBar.hide()
        self.fillConfigDefault()
        
        # Connect button and other events
        self.openFolderButton.clicked.connect(self.openFolder)
        self.extractButton.clicked.connect(self.extractData)
        self.profileButton.clicked.connect(self.buildProfile)
        self.correlateButton.clicked.connect(self.correlateData)
        self.resetButton.clicked.connect(self.cleanWidget)

        self.salMinValue.editingFinished.connect(self.salMinValueChange)
        self.cytMinValue.editingFinished.connect(self.cytMinValueChange)
        self.salMaxValue.editingFinished.connect(self.salMaxValueChange)
        self.cytMaxValue.editingFinished.connect(self.cytMaxValueChange)

        #self.validFolder("/data/results/resultsAll")

    def openFolder(self):
        """
        """
        
        fname= QFileDialog.getExistingDirectory(self,
                                                "Select folder",
                                                QDir.homePath())

        if fname:
            self.validFolder(fname)

    def validFolder(self, name):
        """
        """

        self.urlLabel.setText(name)

        self.ok = True
        for f in cfg.files:
            if not os.path.isfile(os.path.join(name, cfg.files[f])):
                self.ok = False

        if self.ok:
            self.resultsFolder = name
            self.folderStatusLabel.setText("<font color=\"green\">This is a valid folder !</font>")
            self.extractButton.setEnabled(True)
        else:
            self.folderStatusLabel.setText("<font color=\"red\">This folder is not valid!</font>")
        
    def buildProfile(self,):
        """
        """

        self.buildProfileSignal.emit(os.path.join(self.resultsFolder, cfg.extractedDataFile))

    def correlateData(self,):
        """
        """

        self.correlateDataSignal.emit(os.path.join(self.resultsFolder, cfg.extractedDataFile))
        
    def extractData(self):
        """
        """

        self.progressBar.show()

        # Get option
        cellsDiameter = { 'min' : self.cytMinValue.value(),
                          'max': self.cytMaxValue.value() }
        salDiameter = { 'min' : self.salMinValue.value(),
                        'max': self.salMaxValue.value() }

        self.extract = DataExtracter(self.resultsFolder, cellsDiameter, salDiameter)
        self.extract.start()

        self.extract.message.connect(self.setStatus)
        self.extract.progression.connect(self.updateProgression)
        self.extract.done.connect(self.extractionDone)

        self.resetButton.setEnabled(False)
        self.extractButton.setEnabled(False)
        self.groupConf.setEnabled(False)
        self.groupFolder.setEnabled(False)

    def updateProgression(self, p):
        """
        """

        self.progressBar.setValue(p)

    def setStatus(self, message):
        """
        """

        self.status.setText("<font style = \"font-weight:600;\">Extraction status : </font>" + message)

    def extractionDone(self):
        """
        """

        self.progressBar.hide()
        self.progressBar.setValue(0)

        ratioExcludeCells = 100.0 * self.extract.excludeCells / self.extract.totalCells
        ratioExcludeSal = 100.0 * self.extract.excludeSal / self.extract.totalSal
        
        text = """<p><font color=\"green\">Data have been successfully extracted.</font></p>"""
        text += """<p>%i cells have been excluded on %i cells (%.1f%%)</p>""" % (self.extract.excludeCells, self.extract.totalCells, ratioExcludeCells)
        text += """<p>%i salmonella have been excluded on %i salmonella (%.1f%%)</p>""" % (self.extract.excludeSal, self.extract.totalSal, ratioExcludeSal)
        text += """<p>Extracted data filename is <font color=\"red\">%s</font> and performance filename is <font color=\"red\">%s</font>.</p>""" % (cfg.extractedDataFile, cfg.performanceFile)
        text += """<p>Both files are located in the same folder as above.</p>"""

        self.extractionStatusLabel.setText(text)

        self.profileButton.setEnabled(True)
        self.correlateButton.setEnabled(True)

        self.resetButton.setEnabled(True)
        self.extractButton.setEnabled(True)
        self.groupConf.setEnabled(True)
        self.groupFolder.setEnabled(True)

    def cleanWidget(self):
        """
        """

        self.urlLabel.setText("")
        self.extractionStatusLabel.setText("")
        self.folderStatusLabel.setText("")

        self.extractButton.setEnabled(False)
        self.profileButton.setEnabled(False)
        self.correlateButton.setEnabled(False)

        self.fillConfigDefault()

    def fillConfigDefault(self,):
        """
        """

        self.salMinValue.setValue(cfg.salMinDiameter)
        self.salMaxValue.setValue(cfg.salMaxDiameter)
        self.cytMinValue.setValue(cfg.cytMinDiameter)
        self.cytMaxValue.setValue(cfg.cytMaxDiameter)

    def salMinValueChange(self):
        """
        """

        if int(self.salMinValue.value()) >= int(self.salMaxValue.value()):
            self.salMinValue.setValue(int(self.salMaxValue.value() - 1))

    def cytMinValueChange(self):
        """
        """

        if int(self.cytMinValue.value()) >= int(self.cytMaxValue.value()):
            self.cytMinValue.setValue(int(self.cytMaxValue.value() - 1))

    def salMaxValueChange(self):
        """
        """

        if int(self.salMaxValue.value()) <= int(self.salMinValue.value()):
            self.salMaxValue.setValue(int(self.salMinValue.value() + 1))

    def cytMaxValueChange(self):
        """
        """

        if int(self.cytMaxValue.value()) <= int(self.cytMinValue.value()):
            self.cytMaxValue.setValue(int(self.cytMinValue.value() + 1))
