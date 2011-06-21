#-*- coding: utf-8 -*-

# legendwidgetidget.py

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

from ui_legendwidget import *

import copy

class LegendWidget(QtGui.QWidget, Ui_LegendWidget):
    """
    """

    def __init__(self, parent = None):
        """
        """

        super(LegendWidget, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("Legend")

    def populate(self, headers, colors):
        """
        """

        # Remove old label
        for i in range(self.scrollWidget.layout().count()):
            item = self.scrollWidget.layout().itemAt(i)
            self.scrollWidget.layout().removeItem(item)

        i = 0
        for header, color in zip(headers, colors):

            color = QColor.fromRgbF(color[0], color[1], color[2])
            color.toRgb()

            self.layout = QtGui.QHBoxLayout()
            self.layout.setSpacing(30)
            
            self.headerLabel = QtGui.QLabel(self.scrollWidget)
            self.headerLabel.setText(header)
            self.layout.addWidget(self.headerLabel)
            
            self.colorLabel = QtGui.QLabel(self.scrollWidget)
            sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.colorLabel.sizePolicy().hasHeightForWidth())
            self.colorLabel.setSizePolicy(sizePolicy)
            self.colorLabel.setStyleSheet("QLabel { background-color : rgb(%f,%f,%f);}" % (color.red(), color.green(), color.blue()))
            self.colorLabel.setText(" "*15)
            self.layout.addWidget(self.colorLabel)
            
            spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
            self.layout.addItem(spacerItem1)
            
            self.scrollWidget.layout().insertLayout(0, self.layout)

            i += 1

        # Set correct window size
        self.resize(self.sizeHint())
        
