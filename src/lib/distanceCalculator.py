#-*- coding: utf-8 -*-

# correlator.py

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

from table import *
from stats import *

from math import *

class DistanceCalculator:
    """
    This class compute a distance matrix
    """

    def __init__(self, table):
        """
        """

        self.table = table
        self.table.zipIter = False

    def build_matrix(self):
        """
        """

        headers = self.table.headers

        correl = Table()
        correl.headers = headers
        correl.lineHeaders = headers
        
        vectors = []

        for i in range(len(headers)):
            vec = []
            for line in self.table.data:
                vec.append(float(line[i]))
            vectors.append(vec)

        correl.data = []
        for i in range(len(headers)):
            line = []
            for j in range(len(headers)):
                if i == j:
                    line.append('NaN')
                elif i > j:
                    line.append(correl.data[j][i])
                else:
                    line.append(self.distance(vectors[i], vectors[j]))

            correl.data.append(line)

        return correl

    def distance(self, vec1, vec2):
        """
        Euclidian distance
        """

        dist = 0
        for e1, e2 in zip(vec1, vec2):
            dist += pow(e1 - e2, 2)

        return str(sqrt(dist))
    
