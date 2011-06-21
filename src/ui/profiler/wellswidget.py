#-*- coding: utf-8 -*-

# wellswidget.py

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
# HOLDER OR CONTRIBUTORS BE LIABLE FOR AN6Y DIRECT, INDIRECT, INCIDENTAL,
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

from lib.table import *


class WellItem(QtGui.QTreeWidgetItem):
    """
    """

    def __init__(self, label, color, parent = None):
        """
        """

        super(WellItem, self).__init__(parent)
        
        self.setText(0, label)
        self.setCheckState(0, Qt.Unchecked)

        if color:
            brush = QBrush(QColor.fromRgbF(color[0], color[1], color[2]))
            self.setForeground(0, brush)

    def __eq__(self, item):
        """
        """

        return self.text(0) == item.text(0)
    

class WellsWidget(QtGui.QTreeWidget):
    """
    """

    refreshProfile = QtCore.Signal(list, list)

    def __init__(self, parent = None):
        """
        """
        super(WellsWidget, self).__init__(parent)

        self.items = []
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemClicked.connect(self.selectItem)
        self.itemDoubleClicked.connect(self.doubleClick)

        self.setHeaderHidden(True)
        self.nWells = 0
        self.nControls = 0

        self.objects = []

        self.controls = []
        self.toDisplay = []
        self.controlWells = []

        self.items = []

    def load(self, table):
        """
        """

        # Empty treeWidget
        while self.topLevelItemCount() > 0:
            self.takeTopLevelItem(0)

        self.items = []

        self.nWells = 0
        self.nControls = 0

        self.objects = []

        self.controls = []
        self.toDisplay = []
        self.controlWells = []
        
        self.table = table
        self.fill()
        
    def fill(self):
        """
        Fill tree widget with all well from the table
        """

        tree = {}
        self.table.zipIter = False
        i = 0
        for l in self.table.lineHeaders:

            l = l.split(" -- ")
            exp = l[0]
            date = l[1]
            well = l[2]

            if exp not in tree.keys():
                tree[exp] = {}
            if date not in tree[exp]:
                tree[exp][date] = []

            tree[exp][date].append((well, self.table.colors[i]))
            i += 1

        for exp in tree:
            expItem = WellItem(exp, None, None)
            self.addTopLevelItem(expItem)
            
            for date in tree[exp]:
                dateItem = WellItem(date, None, expItem)
                self.addTopLevelItem(dateItem)
                
                for well, color in tree[exp][date]:
                    label = well
                    wellItem = WellItem(label, color, dateItem)
                    self.addTopLevelItem(wellItem)
                    self.items.append(wellItem)
                    self.objects.append(wellItem)

        self.sortItems(0, Qt.AscendingOrder)

    def selectItem(self, item = None):
        """
        """

        if item:
            newState = item.checkState(0)

            for i in range(item.childCount()):
                child = item.child(i)
                child.setCheckState(0, newState)
                if child.childCount() != 0:
                    for j in range(child.childCount()):
                        child.child(j).setCheckState(0, newState)
        tmp = []
        for i in self.items:
            if i.checkState(0) == Qt.Checked:
                name = i.parent().parent().text(0) + ' -- '
                name += i.parent().text(0) + ' -- '
                name += i.text(0)
                tmp.append(name)

        controls = []
        for item in self.controls:
            name = item.parent().parent().text(0) + ' -- '
            name += item.parent().text(0) + ' -- '
            name += item.text(0)
            controls.append(name)

        if self.nWells != len(tmp) or self.nControls != len(controls):
            #self.refreshProfile.emit(tmp, controls)
            self.toDisplay = tmp
            self.nWells = len(tmp)

        self.nControls = len(controls)
        self.controlWells = controls

    def doubleClick(self, item, column):
        """
        """

        if item in self.controls:
            self.controls.remove(item)
            font = QFont()
            font.setWeight(QFont.Normal)
            item.setFont(0, font)
        else:
            self.controls.append(item)
            font = QFont()
            font.setWeight(QFont.Bold)
            item.setFont(0, font)

        self.selectItem()

    def itemSignal(self, name, mode = 'singleClick'):
        """
        """

        for i in self.items:
            itemName = i.parent().parent().text(0) + ' -- '
            itemName += i.parent().text(0) + ' -- '
            itemName += i.text(0)

            if name == itemName:

                if mode == 'singleClick':
                    i.setCheckState(0, Qt.Checked)
                    self.itemClicked.emit(i, 0)
                elif mode == 'doubleClick':
                    self.itemDoubleClicked.emit(i, 0)
                    
        self.selectItem()
        
