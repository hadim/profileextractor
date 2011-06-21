#-*- coding: utf-8 -*-

# config.py

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

verbose = False

######################
# Path configuration #
######################

# Path where CellProfiler raw data are store
# (raw data are .csv files)
mainPathCellProfiler = "C:\\Documents and Settings\\h.mary\\My Documents\\results\\resultsMedium\\"

# CSV files to analyse
files = { "cellsFile" : "DefaultOUT_CellsObject.csv",
          "cytoplasmFile" : "DefaultOUT_CytoplasmObject.csv",
          "imageFile" : "DefaultOUT_Image.csv",
          "nucleiFile" : "DefaultOUT_NucleiObject.csv",
          "salmonellaFile" : "DefaultOUT_SalmonellaObject.csv", }

# Clean CSV files with interesting extracted data 
extractedDataFile = "extractedData.csv"

# CSV file which contains some CellProfiler performance statistics
performanceFile = "performance.csv"

# Delimiter symbol for parsing CSV files
delimiterCSV = ","

####################################
# Profile visualizer configuration #
####################################

# Regex to identify metadata fields
metadata_column = "^Metadata\_.*$"

# Regex to identify fields which will be
# normalized and plotted on the profile
displayed_column = "^General\_.*|.*\_Mean$"

######################
# Matrix correlation #
######################

color = { (-1, -0.8) : {'r': 255, 'g': 0, 'b': 0},
          (-0.8, -0.6) : {'r': 255, 'g': 50, 'b': 50},
          (-0.6, -0.4) : {'r': 255, 'g': 100, 'b': 100},
          (-0.4, -0.2) : {'r': 255, 'g': 150, 'b': 150},
          (-0.2, -0.0) : {'r': 255, 'g': 200, 'b': 200},
          (0.0, 0.2) : {'r': 200, 'g': 200, 'b': 255},
          (0.2, 0.4) : {'r': 150, 'g': 150, 'b': 255},
          (0.4, 0.6) : {'r': 100, 'g': 100, 'b': 255},
          (0.6, 0.8) : {'r': 50, 'g': 50, 'b': 255},
          (0.8, 1.0) : {'r': 20, 'g': 20, 'b': 255},
          }

# Tmp file ( used to display correlation graph image in the interface )
tmpCorrelFile = "tmp_correl.png"

#########################################
# Extracted data CSV file configuration #
#########################################
# Warning : do not touch this part,
# unless you know what you're doing
#########################################

# Metadata fields
expNameField = 'Metadata_ExpName'
dateField = 'Metadata_Date'
wellField = 'Metadata_Well'

# Fields to keep in CSV files
fields = { 'imageNb' : 'ImageNumber',
           'objNb' : 'ObjectNumber',

           'area' : 'AreaShape_Area',
           'perimeter' : 'AreaShape_Perimeter',
           'majorAxisLength' : 'AreaShape_MajorAxisLength',
           'minorAxisLength' : 'AreaShape_MinorAxisLength',
           'formFactor' : 'AreaShape_FormFactor',
           
           'totalSalmonella' : 'Children_SalmonellaObject_Count' }

fieldsSalmonella = { 'area' : 'AreaShape_Area',
                     'perimeter' : 'AreaShape_Perimeter',
                     'majorAxisLength' : 'AreaShape_MajorAxisLength',
                     'minorAxisLength' : 'AreaShape_MinorAxisLength',
                     'formFactor' :  'AreaShape_FormFactor',
                     'cellDist' : 'Distance_Minimum_CellsObject',
                     'nucDist' : 'Distance_Minimum_NucleiObject', }

fieldsNuclei = { 'area' : 'AreaShape_Area',
                 'perimeter' : 'AreaShape_Perimeter',
                 'majorAxisLength' : 'AreaShape_MajorAxisLength',
                 'minorAxisLength' : 'AreaShape_MinorAxisLength',
                 'formFactor' :  'AreaShape_FormFactor', }

fieldsCytoplasm = { 'area' : 'AreaShape_Area',
                    'perimeter' : 'AreaShape_Perimeter',
                    'majorAxisLength' : 'AreaShape_MajorAxisLength',
                    'minorAxisLength' : 'AreaShape_MinorAxisLength',
                    'formFactor' :  'AreaShape_FormFactor', }

fieldsCells = { 'area' : 'AreaShape_Area',
                'perimeter' : 'AreaShape_Perimeter',
                'majorAxisLength' : 'AreaShape_MajorAxisLength',
                'minorAxisLength' : 'AreaShape_MinorAxisLength',
                'formFactor' :  'AreaShape_FormFactor',
                'meanIntensity' : 'Intensity_MeanIntensity_OriCytoplasm', }

# Extraction configuration, default values
salMinDiameter = 0
salMaxDiameter = 200
cytMinDiameter = 30
cytMaxDiameter = 800

# Headers and organization of the extracted data CSV file
headersOutLevelOne = [ ('Metadata', False), ('General', False),
                       ('InfoSalmonella', True), ('InfoNuclei', True),
                       ('InfoCells', True), ('InfoCytoplasm', True) ]

headersOutLevelTwo = [ ['Experiment', 'Date', 'Well'],
                       ['TotalCells', 'TotalSalmonella',
                        'TotalInfectedCells', 'RatioInfectedCells' ],
                       [ 'PerCell', 'Area', 'dynamicLocation', 'FormFactor',
                         'MajorAxisLength', 'MinorAxisLength', 'Perimeter'],
                       [ 'Area', 'FormFactor', 'MajorAxisLength',
                         'MinorAxisLength', 'Perimeter'],
                       [ 'Area', 'FormFactor', 'MajorAxisLength', 'MeanIntensity',
                         'MinorAxisLength', 'Perimeter', ],
                       [ 'Area', 'FormFactor', 'MajorAxisLength',
                         'MinorAxisLength', 'Perimeter'],
                       ]
