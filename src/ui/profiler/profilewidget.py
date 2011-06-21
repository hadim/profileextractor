#-*- coding: utf-8 -*-

# profilewidget.py

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

from lib.table import *
from lib.profiler import *

import config as cfg
import copy

class ProfileWidget(QtGui.QLabel):
    """
    """

    updateDone = QtCore.Signal()

    def __init__(self, parent = None):
        """
        """
        super(ProfileWidget, self).__init__(parent)

        # Display welcome image
        self.tmpFile = QDir.tempPath() + QDir.separator() + "tmp_ProfileWidget.png"
        self.isProfile = False

        self.setSizePolicy(QtGui.QSizePolicy.Ignored,
                           QtGui.QSizePolicy.Ignored)
        self.setScaledContents(True)

        self.scaleFactor = 1.0
        self.legend = False
        self.maker = None

        self.table = None

        self.clear()

    def drawProfile(self, table = None, blank = False):
        """
        Ask to draw the profile
        """

        if table:
            self.table = table

        # if not self.table or self.table and len(self.table) == 0:
        #     self.clear()
        #     return 
            
        if not blank and self.table and len(self.table) > 0:
            self.maker = Profiler(self.table, self.tmpFile, legend = self.legend)
            self.maker.done.connect(self.display)
            self.maker.start()
            #self.maker.setPriority(QThread.HighPriority)
        else:
            self.clear()

    def clear(self):
        """
        """

        self.display()
        self.isProfile = False
        

    def display(self, fname = None):
        """
        Display nex profile in the widget
        """

        if fname:
            pixmap = QPixmap.fromImage(QImage(fname))
        else:
            pixmap = QPixmap(1900, 640)
            pixmap.fill(Qt.white)
        
        self.setPixmap(pixmap)
        self.updateDone.emit()
        self.maker = None
        self.isProfile = True

    # def wheelEvent(self, event):
    #     """
    #     """

    #     if event.delta() > 0:
    #         self.zoomIn()
    #     else:
    #         self.zoomOut()

    # def zoomIn(self):
    #     """
    #     """
    #     self.scaleImage(1.25)

    # def zoomOut(self):
    #     """
    #     """
    #     self.scaleImage(0.8)

    # def scaleImage(self, factor):
    #     """
    #     """

    #     self.scaleFactor *= factor
    #     self.resize(self.scaleFactor * self.pixmap().size())
        
    #     # adjustScrollBar(scrollArea->horizontalScrollBar(), factor)
    #     # adjustScrollBar(scrollArea->verticalScrollBar(), factor)
        
