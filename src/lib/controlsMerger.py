#-*- coding: utf-8 -*-

# controlsMerger.py

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

class ControlsMerger:
    """
    """

    def __init__(self, table, controls):
        """
        """

        self.table = table
        self.controls = controls
        self.controlsName = []

    def merge(self):
        """
        """

        lines = {}

        # Select controls lines
        for l, header in zip(self.table, self.table.lineHeaders):

            if header in self.controls:
                exp = " -- ".join(header.split(' -- ')[:2])

                if exp not in lines.keys():
                    lines[exp] = []

                lines[exp].append(l)

        # Merge each selected lines per experiment
        for exp in lines:

            l = lines[exp]
            lineHeaderLabel = exp + " -- " + "Controls"
            self.controlsName.append(lineHeaderLabel)

            means = self.do_lines_average(l)
            self.table.append_line(means, lineHeaderLabel)

        return self.table

    def do_lines_average(self, lines):
        """
        """

        tmpLine = [0] * len(lines[0])
        for l in lines:
            for i in range(len(l)):
                tmpLine[i] += l[i]

        n = len(lines)
        line = []
        for l in tmpLine:
            line.append(Decimal(l) / Decimal(n))

        return line
