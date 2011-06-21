#-*- coding: utf-8 -*-

# normalizer.py

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

from decimal import *

class Normalizer:
    """
    This class normalize data calculating z-value for
    each column of Table() object.
    See http://en.wikipedia.org/wiki/Standard_score
    """

    def __init__(self, table):
        """
        """

        self.table = table
        self.table.zipIter = False

    def normalize(self):
        """
        Return a normalized Table() object
        """

        normalTable = Table()
        normalTable.zipIter = False

        normalTable.headers = self.table.headers
        normalTable.lineHeaders = self.table.lineHeaders

        means = {}
        stds = {}
        for h in self.table.headers:

            col = self.table.column(h)
            stats = Stats(col)

            means[h] = stats.mean
            stds[h] = stats.std

        for l in self.table:

            line = []

            for i in range(len(self.table.headers)):
                header = self.table.headers[i]
                if stds[header] != 0:
                    normalValue = (Decimal(str(l[i])) - means[header]) / stds[header]
                else:
                    normalValue = 0
                line.append(normalValue)

            normalTable.data.append(line)

        return normalTable
        

    
