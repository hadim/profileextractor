#-*- coding: utf-8 -*-

# correlationwidget.py

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

from PySide import QtCore, QtGui
from PySide.QtCore import *
from PySide.QtGui import *

from ui_correlationwidget import *

from lib.table import *
from lib.correlator import *
from lib.distanceCalculator import *
from lib.correlationdrawer import *
from lib.normalizer import *
from displaycorrelationwidget import *

import config as cfg
import re, os, sys, copy

class CorrelationWidget(QtGui.QWidget, Ui_CorrelationWidget):
    """
    """

    importWells = Signal()
    
    def __init__(self, mode, parent = None):
        """
        """
        super(CorrelationWidget, self).__init__(parent)
        self.setupUi(self)

        self.mode = mode
        self.computeMode = 'correlation'

        self.loadButton.clicked.connect(self.openFile)
        self.saveButton.clicked.connect(self.saveTable)
        self.drawButton.clicked.connect(self.drawCorrel)
        self.tightButton.clicked.connect(self.toggleTightMode)
        self.toggleSelectedButton.clicked.connect(self.toggleSelectionItem)
        self.switchModeButton.clicked.connect(self.switchCalculator)
        
        self.selectAll = True

        self.displayers = []
        self.tight_headers = True

        self.saveButton.setEnabled(False)
        self.toggleSelectedButton.setEnabled(False)
        self.tightButton.setEnabled(False)
        self.drawButton.setEnabled(False)
        self.switchModeButton.setEnabled(False)
        self.importWellsButton.setEnabled(False)

        if self.mode == 'parameters':
            self.importWellsButton.setVisible(False)
        else:
            self.importWellsButton.clicked.connect(self.importWells)
            self.controls = []
            
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

        self.load(self.table)

    def load(self, table = None):
        """
        """

        if table:
            self.table = table

        # Normalize values
        self.table = Normalizer(self.table).normalize()
        
        # Rotate table if we works we wells instead of parameters
        if self.mode == 'wells':
            self.table = self.table.rotate()

        self.populateFilterWidget()
        self.makeCorrelation()

        self.saveButton.setEnabled(True)
        self.toggleSelectedButton.setEnabled(True)
        self.tightButton.setEnabled(True)
        self.drawButton.setEnabled(True)
        self.switchModeButton.setEnabled(True)
        self.importWellsButton.setEnabled(True)

    def makeCorrelation(self, mode = 'display', remove_lines = [], fname = ""):
        """
        Compute correlation with Correlator object or distance with
        DistanceCalculator object
        """

        tmpTable = copy.deepcopy(self.table)
        tmpTable.remove_lines_by_name(remove_lines)

        if len(tmpTable) > 1:

            if self.computeMode == 'correlation':
                self.correlTable = Correlator(tmpTable).build_matrix()
            elif self.computeMode == 'distance':
                self.correlTable = DistanceCalculator(tmpTable).build_matrix()

            if mode == 'display':
                self.fillTableWidget()
                self.tableWidget.resizeRowsToContents()
                self.tableWidget.resizeColumnsToContents()
            elif mode == 'write':
                self.correlTable.write(fname)

        else:
            self.filterWidget.setEnabled(True)

    def fillTableWidget(self, colored = True):
        """
        """
        
        headers = self.correlTable.headers

        self.tableWidget.setRowCount(len(headers))
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

        # Set table headers
        for i in range(len(headers)):
            if self.tight_headers:
                newItem1 = QTableWidgetItem(str(i))
                newItem2 = QTableWidgetItem(str(i))
            else:
                newItem1 = QTableWidgetItem(str(i))
                newItem2 = QTableWidgetItem(str(i) + ' - ' + headers[i])
            
            self.tableWidget.setHorizontalHeaderItem(i, newItem1)
            self.tableWidget.setVerticalHeaderItem(i, newItem2)
        
        # Fill table
        for i in range(len(headers)):
            for j in range(len(headers)):

                # Get data
                data = self.correlTable.data[i][j]

                if self.computeMode == 'correlation':
                    dataColor = float(data)
                elif self.computeMode == 'distance':
                    dataColor = float(float(data) / self.correlTable.mmax()) * 2.0 - 1.0

                # Get color
                if colored:
                    color = QColor(255, 255, 255)
                    for r in cfg.color:
                        if dataColor > r[0] and dataColor < r[1]:
                            color = QColor(cfg.color[r]['r'],
                                           cfg.color[r]['g'],
                                           cfg.color[r]['b'])

                # Create or update item
                item = self.tableWidget.item(i, j)
                if item:
                    item.setText("%.2f" % float(data))
                else:
                    item = QTableWidgetItem("%.2f" % float(data))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tableWidget.setItem(i, j, item)

                if self.mode == 'wells':
                    if headers[i] in self.controls or headers[j] in self.controls:
                        color.setHsv(color.hue(), color.saturation(), 150)
                
                item.setBackground(QBrush(color))

        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

        self.splitter.setStretchFactor(0, 1)

        self.filterWidget.setEnabled(True)

    def drawCorrel(self):
        """
        """

        if self.tableWidget.currentItem():
            row = self.tableWidget.currentItem().row()
            column = self.tableWidget.currentItem().column()
            coef = self.tableWidget.currentItem().text()
        
            param1 = self.correlTable.headers[row]
            param2 = self.correlTable.headers[column]

            if param1 != param2:

                index1 = self.correlTable.headers.index(param1)
                index2 = self.correlTable.headers.index(param2)

                vec1 = []
                vec2 = []

                self.table.zipIter = False
                for line in self.table:
                    vec1.append(float(line[index1]))
                    vec2.append(float(line[index2]))

                self.drawer = CorrelationDrawer(vec1, vec2,
                                                param1, param2, coef)
                self.drawer.done.connect(self.displayCorrelation)
                self.drawer.draw(self.computeMode)
                

    def displayCorrelation(self, fname, coef):
        """
        """

        self.displayers.append(DisplayCorrelationWidget(fname, coef))
        self.displayers[-1].show()
        

    def toggleTightMode(self,):
        """
        """

        self.tight_headers = not self.tight_headers
        self.fillTableWidget()

    def populateFilterWidget(self):
        """
        """

        # Create widget
        self.container = QDialog()
        self.layout = QVBoxLayout()

        # Add widget on the splitter
        if self.splitter.count() == 2:
            self.splitter.widget(1).setParent(None)
        self.container.setLayout(self.layout)
        self.splitter.addWidget(self.container)
        self.filterWidget = QTreeWidget()
        
        # Add tree or list widget according to the data
        if self.mode == 'parameters':
            
            self.filterWidget = QTreeWidget()
            self.filterWidget.setHeaderHidden(True)

            tree = {}
            self.table.zipIter = False
            for l in self.table.lineHeaders:

                l = l.split(" -- ")
                exp = l[0]
                date = l[1]
                well = l[2]

                if exp not in tree.keys():
                    tree[exp] = {}
                if date not in tree[exp]:
                    tree[exp][date] = []

                tree[exp][date].append(well)

            for exp in tree:
                expItem = QTreeWidgetItem(None)
                expItem.setText(0, exp)
                expItem.setCheckState(0, Qt.Checked)
                self.filterWidget.addTopLevelItem(expItem)

                for date in tree[exp]:
                    dateItem = QTreeWidgetItem(expItem)
                    dateItem.setCheckState(0, Qt.Checked)
                    dateItem.setText(0, date)
                    self.filterWidget.addTopLevelItem(dateItem)

                    for well in tree[exp][date]:
                        label = well
                        wellItem = QTreeWidgetItem(dateItem)
                        wellItem.setText(0, label)
                        self.filterWidget.addTopLevelItem(wellItem)
                        wellItem.setCheckState(0, Qt.Checked)

            self.filterWidget.sortItems(0, Qt.AscendingOrder)
            
        elif self.mode == 'wells':
            
            self.filterWidget = QListWidget()
            self.filterWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
            
            for label in self.table.lineHeaders:
                item = QListWidgetItem(label, self.filterWidget)
                item.setCheckState(Qt.Checked)

        self.setStatus()

        self.layout.addWidget(self.filterWidget)
        self.filterWidget.itemClicked.connect(self.selectItem)

        # Add update button
        self.updateButton = QPushButton("Update table")
        self.layout.addWidget(self.updateButton)
        self.updateButton.clicked.connect(self.updateTable)

    def selectItem(self, item = None, index = 0):
        """
        """

        self.repaint()

        self.itemToRemove = []

        if self.mode == 'wells':
            
            for i in range(self.filterWidget.count()):
                item = self.filterWidget.item(i)
                if item.checkState() == Qt.Unchecked and item.text() in self.table.lineHeaders:
                    self.itemToRemove.append(item.text())

        elif self.mode == 'parameters':

            if item:
                newState = item.checkState(0)

                for i in range(item.childCount()):
                    child = item.child(i)
                    child.setCheckState(0, newState)
                    if child.childCount() != 0:
                        for j in range(child.childCount()):
                            child.child(j).setCheckState(0, newState)

            for i in range(self.filterWidget.topLevelItemCount()):
                exp = self.filterWidget.topLevelItem(i)
                
                for j in range(exp.childCount()):
                    date = exp.child(j)
                    
                    for k in range(date.childCount()):
                        well = date.child(k)
                        label = exp.text(0) + " -- "
                        label += date.text(0) + " -- "
                        label += well.text(0)
                        if well.checkState(0) == Qt.Unchecked and label in self.table.lineHeaders:
                            self.itemToRemove.append(label)

        return self.itemToRemove

    def updateTable(self, ):
        """
        """

        self.makeCorrelation(remove_lines = self.itemToRemove)
        
    def toggleSelectionItem(self):
        """
        """

        self.selectAll = not self.selectAll
        if self.selectAll:
            state = Qt.Checked
        else:
            state = Qt.Unchecked
        
        if self.mode == 'wells':
            
            for i in range(self.filterWidget.count()):
                item = self.filterWidget.item(i)
                item.setCheckState(state)

        elif self.mode == 'parameters':
            
            for i in range(self.filterWidget.topLevelItemCount()):
                item = self.filterWidget.topLevelItem(i)
                item.setCheckState(0, state)
                self.selectItem(item)
                
        self.selectItem()
    

    def setStatus(self, mess = None):
        """
        """

        status = "Remember than you need at least 2 items selected to make the matrix changed"
        if mess:
            status += "  |  "
            status += mess
        self.status.setText(status)

    def saveTable(self):
        """
        """
        
        dest, filterExt = QFileDialog.getSaveFileName(self,
                                                      "Save File (csv format)",
                                                      QDir.homePath(),
                                                      "CSV files (*.csv)")

        if dest:
            itemToRemove = self.selectItem()
            self.makeCorrelation(mode = 'write',
                                 remove_lines = itemToRemove,
                                 fname = dest)


    def receiveControls(self, controls, table = None):
        """
        """

        tmp = []
        for c in controls:
            tmp.append(str(c))
        self.controls = tmp
        self.load(table)
        

    def switchCalculator(self):
        """
        """

        if self.computeMode == 'correlation':
            self.computeMode = 'distance'
        elif self.computeMode == 'distance':
            self.computeMode = 'correlation'
        else:
            return

        self.makeCorrelation()
