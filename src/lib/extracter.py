#-*- coding: utf-8 -*-

# extracter.py

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

try:
    from PySide import QtCore, QtGui
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    print "Error : This script need Qt libraries for Python."
    print "Please install PySide: http://www.pyside.org/"

from table import *
from stats import *

import config as cfg
from lib.utils import *
from lib.stats import *

import sys

class DataExtracter(QThread):
    """
    """

    message = QtCore.Signal(str)
    progression = QtCore.Signal(int)
    done = QtCore.Signal()

    def __init__(self, resuFolder, cellsDiameter, salDiameter, parent = None):
        """
        """
        super(DataExtracter, self).__init__(parent) 

        self.resultsFolder = resuFolder
        self.cellsDiameter = cellsDiameter
        self.salDiameter = salDiameter

    def run(self):
        """
        """

        self.verbose = True
        self.setPriority(QThread.LowestPriority)

        ##############
        # Read files #
        ##############

        csvRaw = {}
        data = {}
        self.headers = {}
        path = self.resultsFolder

        if self.verbose:
            print "* Loading .csv files :"
            
        self.message.emit("Loading .csv files")

        for f in cfg.files:

            pathFile = os.path.join(path, cfg.files[f])
            csvRaw[f] = csv.reader(open(pathFile, 'rb'),
                                   delimiter = cfg.delimiterCSV)

            size = getSize(pathFile)
            if self.verbose:
                print "\t. " + f + " -> " + cfg.files[f] + " ( " + size + " )"
            
            dataset = []
            currentSize = 0
            isHeader = True
            for line in csvRaw[f]:

                if isHeader:
                    isHeader = False
                    self.headers[f] = line
                else:
                    dataset.append(line)
                    currentSize += sys.getsizeof(line)
                
            data[f] = dataset

        if self.verbose:
            print

        # Our data structure
        dataStruct = {}

        ##############################################################
        # Reading cells informations to construct the data structure #
        ##############################################################

        if self.verbose:
            print "* Reading informations from .cvs files"
        self.message.emit("Reading informations from .cvs files")

        self.excludeCells = len(data["cellsFile"])
        self.totalCells = len(data["cellsFile"])

        all_wells = []

        for line in data["cellsFile"]:

            idx_majorAxis = self.headers["cellsFile"].index(cfg.fields['majorAxisLength'])

            if float(line[idx_majorAxis]) > self.cellsDiameter['min'] and \
               float(line[idx_majorAxis]) < self.cellsDiameter['max']:
                
                self.excludeCells -= 1

                idx_expNameField = self.headers["cellsFile"].index(cfg.expNameField)
                idx_dateField = self.headers["cellsFile"].index(cfg.dateField)
                idx_wellField = self.headers["cellsFile"].index(cfg.wellField)

                # Create keys in dataStruct if not already in
                if line[idx_expNameField] not in dataStruct.keys():
                    dataStruct[line[idx_expNameField]] = {}

                if line[idx_dateField] not in dataStruct[line[idx_expNameField]].keys():
                    dataStruct[line[idx_expNameField]][line[idx_dateField]] = {}

                if line[idx_wellField] not in dataStruct[line[idx_expNameField]][line[idx_dateField]].keys():
                    dataStruct[line[idx_expNameField]][line[idx_dateField]][line[idx_wellField]] = { 'cells' : [], }

                # Calculate number of wells
                wells_id = line[idx_expNameField] + " -- " + line[idx_dateField] + " -- " + line[idx_wellField]
                if wells_id not in all_wells:
                    all_wells.append(wells_id)

                # Build a cell, which is a simple dict
                cell = {}

                for f in cfg.fields:
                    idx = self.headers["cellsFile"].index(cfg.fields[f])
                    cell[f] = line[idx]

                # Add cell to the well
                dataStruct[line[idx_expNameField]][line[idx_dateField]][line[idx_wellField]]['cells'].append(cell)

        totWells = len(all_wells)

        #########################################################################
        # Perform statistics on dataStruct and get more informations from other #
        # files                                                                 #
        #########################################################################

        if self.verbose:
            print
            print "* Compute statistics"

        self.message.emit("Compute statistics (it can take some time)")

        i = 0

        self.excludeSal = 0
        self.totalSal = 0

        for exp in dataStruct:
            for date in dataStruct[exp]:
                for well in dataStruct[exp][date]:

                    i += 1
                    self.progression.emit(int(i*100/(totWells*2)))
                    self.message.emit("Compute statistics (%i / %i)" % (i, totWells))
                    if self.verbose:
                        print "%i / %i" % (i, totWells)
                    
                    currWell = dataStruct[exp][date][well]
                    salmonella = []
                    totInfected = 0.0

                    # Memorize id number for all cells
                    # id = (imageNumber, ObjectNumber)
                    idCells = []
                    
                    for cell in currWell['cells']:

                        totSal = int(cell['totalSalmonella'])
                        salmonella.append(totSal)
                        if totSal > 0:
                            totInfected += 1

                        idCells.append((cell['imageNb'], cell['objNb']))

                    currWell['salmonella'] = {}
                    currWell['nuclei'] = {}
                    currWell['cytoplasm'] = {}
                    currWell['cellsInfo'] = {}
                    currWell['salmonella']['perCell'] = Stats(salmonella).dict()

                    currWell['totalSalmonella'] = currWell['salmonella']['perCell']['sum']
                    currWell['totalCells'] = len(currWell['cells'])
                    currWell['totalInfected'] = totInfected
                    if currWell['totalCells'] == 0:
                        currWell['ratioInfected'] = 0
                    else:
                        currWell['ratioInfected'] = "%.4f" % (totInfected / currWell['totalCells'])

                    # Get more information about Salmonella
                    for f in cfg.fieldsSalmonella:
                        if f not in currWell['salmonella'].keys():
                            currWell['salmonella'][f] = []

                    for line in data["salmonellaFile"]:
                        self.totalSal += 1

                        idx_majorAxis = self.headers["salmonellaFile"].index(cfg.fieldsSalmonella['majorAxisLength'])
                        
                        if float(line[idx_majorAxis]) > self.salDiameter['min'] and \
                               float(line[idx_majorAxis]) < self.salDiameter['max']:

                            idx_ImageNb = self.headers["salmonellaFile"].index('ImageNumber')
                            idx_ParentCells = self.headers["salmonellaFile"].index('Parent_CellsObject')

                            if (line[idx_ImageNb], line[idx_ParentCells]) in idCells:

                                # Save data we need
                                for f in cfg.fieldsSalmonella:
                                    idx= self.headers["salmonellaFile"].index(cfg.fieldsSalmonella[f])
                                    currWell['salmonella'][f].append(float(line[idx]))
                        else:
                            self.excludeSal += 1

                    # Create a new parameter:
                    # dynamicLocation =  nucDist / (nucDist + cellDist)
                    currWell['salmonella']['dynamicLocation'] = []
                    for nuc, cell in zip(currWell['salmonella']['nucDist'],
                                         currWell['salmonella']['cellDist']):
                        try:
                            ratio = float(nuc / (nuc + cell))
                        except ZeroDivisionError:
                            ratio = 0
                            
                        currWell['salmonella']['dynamicLocation'].append(ratio)

                    # Compute stats about salmonella
                    fSal = cfg.fieldsSalmonella.keys() + ['dynamicLocation']
                    fSal.remove('nucDist')
                    fSal.remove('cellDist')
                    for f in fSal:
                        stats = Stats(currWell['salmonella'][f]).dict()
                        currWell['salmonella'][f] = stats

                    # Get more information about Nuclei
                    for f in cfg.fieldsNuclei:
                        if f not in currWell['nuclei'].keys():
                            currWell['nuclei'][f] = []

                    for line in data["nucleiFile"]:

                        idx_ImageNb = self.headers["nucleiFile"].index('ImageNumber')
                        idx_ParentCells = self.headers["nucleiFile"].index('Parent_CellsObject')

                        if (line[idx_ImageNb], line[idx_ParentCells]) in idCells:

                            # Save data we need
                            for f in cfg.fieldsNuclei:
                                idx = self.headers["nucleiFile"].index(cfg.fieldsNuclei[f])
                                currWell['nuclei'][f].append(float(line[idx]))

                    # Compute stats about nuclei
                    for f in cfg.fieldsNuclei:
                        stats = Stats(currWell['nuclei'][f]).dict()
                        currWell['nuclei'][f] = stats

                    # Get more information about Cytoplasm
                    for f in cfg.fieldsCytoplasm:
                        if f not in currWell['cytoplasm'].keys():
                            currWell['cytoplasm'][f] = []

                    for line in data["cytoplasmFile"]:

                        idx_ImageNb = self.headers["cytoplasmFile"].index('ImageNumber')
                        idx_ParentCells = self.headers["cytoplasmFile"].index('Parent_CellsObject')

                        if (line[idx_ImageNb], line[idx_ParentCells]) in idCells:

                            # Save data we need
                            for f in cfg.fieldsCytoplasm:
                                idx = self.headers["cytoplasmFile"].index(cfg.fieldsCytoplasm[f])
                                currWell['cytoplasm'][f].append(float(line[idx]))

                    # Compute stats about cytoplasm
                    for f in cfg.fieldsCytoplasm:
                        stats = Stats(currWell['cytoplasm'][f]).dict()
                        currWell['cytoplasm'][f] = stats

                    # Get more information about cells
                    for f in cfg.fieldsCells:
                        if f not in currWell['cellsInfo'].keys():
                            currWell['cellsInfo'][f] = []

                    for line in data["cellsFile"]:

                        idx_ImageNb = self.headers["cellsFile"].index('ImageNumber')
                        idx_ParentCells = self.headers["cellsFile"].index('ObjectNumber')

                        if (line[idx_ImageNb], line[idx_ParentCells]) in idCells:

                            # Save data we need
                            for f in cfg.fieldsCells:
                                idx = self.headers["cellsFile"].index(cfg.fieldsCells[f])
                                currWell['cellsInfo'][f].append(float(line[idx]))

                    # Compute stats about cells
                    for f in cfg.fieldsCells:
                        stats = Stats(currWell['cellsInfo'][f]).dict()
                        currWell['cellsInfo'][f] = stats

        ########################################################################
        # Write output file with dataStruct and compute some stats before save #
        # data                                                                 #
        ########################################################################

        if self.verbose:
            print
            print "* Write final data to output file"

        self.message.emit("Write final data to output file")

        # Open file
        pathFile = os.path.join(path, cfg.extractedDataFile)
        outWriter = csv.writer(open(pathFile, 'wb'), delimiter = cfg.delimiterCSV)

        # Generate and write headers
        headers = []

        for i in range(len(cfg.headersOutLevelOne)):
            for col in cfg.headersOutLevelTwo[i]:
                if cfg.headersOutLevelOne[i][1]:
                    headers.append(cfg.headersOutLevelOne[i][0] + '_' + col + '_Mean')
                    headers.append(cfg.headersOutLevelOne[i][0] + '_' + col + '_Median')
                    headers.append(cfg.headersOutLevelOne[i][0] + '_' + col + '_Std')
                else:
                    headers.append(cfg.headersOutLevelOne[i][0] + '_' + col)

        outWriter.writerow(headers)

        i = 0

        for exp in dataStruct:
            for date in dataStruct[exp]:
                for well in dataStruct[exp][date]:

                    i += 1
                    self.progression.emit(int(50+(i*100/(totWells*2))))
                    self.message.emit("Write final data to output file (%i / %i)" % (i, totWells))
                    if self.verbose:
                        print "%i / %i" % (i, totWells)
                    

                    currWell = dataStruct[exp][date][well]
                    line = []

                    # Metadata
                    line += [exp, date, well]

                    # General informations
                    line += [ currWell['totalCells'], currWell['totalSalmonella'],
                              currWell['totalInfected'], currWell['ratioInfected'] ]

                    # Salmonella informations
                    line += [ currWell['salmonella']['perCell']['mean'],
                              currWell['salmonella']['perCell']['median'],
                              currWell['salmonella']['perCell']['std'] ]

                    fSal = cfg.fieldsSalmonella.keys() + ['dynamicLocation']
                    fSal.remove('nucDist')
                    fSal.remove('cellDist')
                    for f in sorted(fSal):
                        line += [ currWell['salmonella'][f]['mean'],
                                  currWell['salmonella'][f]['median'],
                                  currWell['salmonella'][f]['std'] ]

                    # Nuclei informations
                    for f in sorted(cfg.fieldsNuclei.keys()):
                        line += [ currWell['nuclei'][f]['mean'],
                                  currWell['nuclei'][f]['median'],
                                  currWell['nuclei'][f]['std'] ]

                    # Cells informations
                    for f in sorted(cfg.fieldsCells.keys()):
                        line += [ currWell['cellsInfo'][f]['mean'],
                                  currWell['cellsInfo'][f]['median'],
                                  currWell['cellsInfo'][f]['std'] ]

                    # Cytoplasm informations
                    for f in sorted(cfg.fieldsCytoplasm.keys()):
                        line += [ currWell['cytoplasm'][f]['mean'],
                                  currWell['cytoplasm'][f]['median'],
                                  currWell['cytoplasm'][f]['std'] ]

                    # Write line on csv
                    outWriter.writerow(line)

            if self.verbose:
                    print

        ########################################################
        # Compute statistics about performance of the pipeline #
        ########################################################

        if self.verbose:
            print "* Reading " + cfg.files["imageFile"] + " file to compute some performance statistics"

        self.message.emit("Reading " + cfg.files["imageFile"] + " file to compute some performance statistics")

        execTime = {}
        for line in data['imageFile']:
            for c in line:
                if 'ExecutionTime_' in c:

                    step = c.split('_')[1]
                    if step not in execTime.keys():
                        execTime[step] = []

                    execTime[step].append(float(line[c]))

        # Write results to output perf file
        pathFile = os.path.join(path, cfg.performanceFile)
        perfWriter = csv.writer(open(pathFile, 'wb'), delimiter = cfg.delimiterCSV)

        perfWriter.writerow(['StepName', 'TotalTime', 'MeanTimePerImage',
                             'MedianTimePerImage', 'StdTimePerImage'])

        means = []
        medians = []
        stds = []
        sums = []

        for s in execTime:

            stats = Stats(execTime[s]).dict()
            execTime[s] = [stats['sum'], stats['mean'], stats['median'], stats['std']]

            sums.append(float(stats['sum']))
            means.append(stats['mean'])
            medians.append(stats['median'])
            stds.append(stats['std'])

        perfWriter.writerows(sortedDict(execTime))
        perfWriter.writerow(['Total', str(sum(sums))])

        self.message.emit("")
        self.done.emit()

        # self.exec_()


if __name__ == '__main__':

    import sys
    from PySide import QtCore, QtGui

    app = QtCore.QCoreApplication(sys.argv)
    
    extract = DataExtracter(sys.argv[1],
                            { 'min' : 30, 'max': 800 },
                            { 'min' : 0, 'max': 200 })
    extract.start()
    extract.wait()

    #sys.exit(app.exec_())
                                  
