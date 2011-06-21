#-*- coding: utf-8 -*-

# table.py

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

import csv, sys, copy, re

class Table:
    """
    """

    def __init__(self, fcsv = None,
                 delimiterCSV = ",",
                 zipIter = True):
        """
        """

        self.fcsv = fcsv
        self.delimiterCSV = delimiterCSV
        self.iter_index = -1
        self.zipIter = zipIter

        self.max = None

        # Data variable
        self.headers = []
        self.lineHeaders = []
        self.lineHeadersName = ""
        self.data = []

        if self.fcsv:
            self.loadCSV()

    def loadCSV(self,):
        """
        """

        csvReader = csv.DictReader(open(self.fcsv, 'rb'),
                                   delimiter = self.delimiterCSV)

        self.headers = csvReader.fieldnames
        for d in csvReader:
            line = []
            for i in self.headers:
                line.append(d[i])
            self.data.append(line)

    def write(self, fname):
        """
        """

        writer = csv.writer(open(fname, 'wb'), delimiter = self.delimiterCSV)
        if len(self.lineHeaders) > 0:
            writer.writerow([self.lineHeadersName] + self.headers)
            for h, l in zip(self.lineHeaders, self.data):
                writer.writerow([h] + l)

        else:
            writer.writerow(self.headers)
            writer.writerows(self.data)
           

    ###############
    # Read method #
    ###############

    def __str__(self,):
        """
        """

        s = ""
        for i in self.data:
            s += str(i)
        return s
    
    def __getitem__(self, key):
        """
        """

        return self.data[key]

    def __len__(self,):
        """
        """

        return len(self.data)

    def __call__(self, line, field):
        """
        """

        return self.data[line][self.index(field)]

    def column(self, field):
        ""
        ""

        col = []
        for d in self.data:
            col.append(d[self.index(field)])

        return col

    def index(self, field):
        """
        """

        return self.headers.index(field)

    def __iter__(self):
        """
        """
        return self
    
    def next(self):
        """
        """

        if self.iter_index >= len(self.data) - 1:
            self.iter_index = -1
            raise StopIteration

        self.iter_index += 1

        if self.zipIter:
            return zip(self.headers, self.data[self.iter_index])
        else:
            return self.data[self.iter_index]

    def find_lines(self, header, content):
        """
        """

        index = self.index(header)
        selection = []

        for i in range(len(self.data)):
            if content in self.data[i][index]:
                selection.append(i)

        return selection

    def mmax(self):
        """
        """

        if self.max != None:
            return self.max

        mmax = 0
        for l in self.data:
            for e in l:
                try:
                    e = float(e)
                    if mmax < e:
                        mmax = e
                except ValueError:
                    pass
        self.max = float(mmax)
        return self.max

    ################
    # Write method #
    ################
    
    def append_line(self, line, headerLine = "", color = (0,0,0)):
        """
        """

        if len(line) > len(self.headers):
            print 'Error : line is too big for this table'
            sys.exit(0)

        for i in range(len(self.headers) - len(line)):
            line.append(None)

        self.colors.append(color)
        self.data.append(line)
        self.lineHeaders.append(headerLine)
        self.thickness.append(1)

    def remove_line(self, index):
        """
        """

        self.data.pop(index)
        self.thickness.pop(index)
        self.colors.pop(index)
        self.lineHeaders.pop(index)

    def remove_lines(self, index):
        """
        """

        for i in index:
            self.remove_line(i)

    def remove_lines_by_name(self, lines_name):
        """
        """

        for n in lines_name:
            idx = self.lineHeaders.index(n)
            self.remove_line(idx)
        
    def append_column(self, header, data, index = None):
        """
        """

        if not index:
            index = len(self.headers)

        self.headers.insert(index, header)

        if len(data) < len(self.data):
            for i in range(len(self.data) - len(data)):
                data.append(None)

        for i in range(len(data)):
            if i == len(self.data):
                self.data.append([None] * len(self.headers))
            self.data[i].insert(index, str(data[i]))

    def remove_column(self, header):
        """
        """

        idx = self.index(header)

        for l in self.data:
            l.pop(idx)
        self.headers.pop(idx)

    def remove_column_by_regex(self, regexs):
        """
        Only keep column which match with regex
        """

        for h in copy.copy(self.headers):

            keep = False
            for regex in regexs:
                m = re.match(regex, h)
                if m:
                    keep = True

            if not keep:
                self.remove_column(h)

    def merge_column_by_regex(self, regexs, colum_name, separator = " -- "):
        """
        Merge column together which match with regex. The new column
        won't belong to self.data anymore but will be place in a new
        variable called self.lineHeaders
        """

        hToMerge = []
        for h in copy.copy(self.headers):

            keep = False
            for regex in regexs:
                m = re.match(regex, h)
                if m:
                    keep = True

            if keep:
                hToMerge.append(h)

        self.lineHeaders = []
        self.lineHeadersName = colum_name
        for l in self:
            merged = ""
            for h in hToMerge:
                idx = self.headers.index(h)
                merged += l[idx][1] + separator

            merged = merged[:-len(separator)]
            self.lineHeaders.append(merged)
 
        for h in hToMerge:
            self.remove_column(h)

    def rotate(self):
        """
        """

        newTable = Table()
        newTable.lineHeaders = self.headers
    
        self.zipIter = False
        for header, line in zip(self.lineHeaders, self):
            newTable.append_column(header, line)

        return newTable

    def invertAxis(self, nHeaders = 0):
        """
        """

        newData = []
        newHeaders = []
        newLineHeaders = []

        i = 0
        for nRows in range(nHeaders, len(self.data[0])):
            row = [self.headers[i + nHeaders]]
            i += 1
            for nCols in range(len(self.data)):
                row.append(self.data[nCols][nRows])
            newData.append(row)

        # Set headers
        # firstH = ""
        # for i in range(nHeaders):
        #     firstH += self.headers[i] + ' -- '
        # newHeaders.append(firstH[:-4])

        newHeaders.append(self.lineHeadersName)
        for row in self.data:
            headerLabel = ''
            for h in row[:nHeaders]:
                headerLabel += h + ' -- '
            newHeaders.append(headerLabel[:-4])

        self.headers = newHeaders
        self.lineHeaders = newLineHeaders
        self.data = newData


if __name__ == '__main__':

    # Read csv file
    table = Table("test.csv")

    # print len(table)
    # print table(5, 'AreaShape_Center_X')
    # print table.column('AreaShape_Center_X')
    # print

    # for line in table:
    #     for i in line:
    #         print i

    table.invertAxis(nHeaders = 3)
    table.write('output.csv')
    
