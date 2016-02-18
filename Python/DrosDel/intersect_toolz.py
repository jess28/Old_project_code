# Class for parsing a bedtools intersect file.
# Copyright (C) 2014 Jessica Strein jessica.strein@uconn.edu
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

class int_parse():
    "parses bedtools intersect file for features of interest"
    def __init__(self, line):
        self.line = line
        self.data = line.rstrip().split('\t')
        self.chrom = self.data[0]
        self.wst = self.data[1]
        self.wen = self.data[2]
        self.db = self.data[4]
        self.type = self.data[5]
        self.gst = self.data[6]
        self.gen = self.data[7]
        self.strand = self.data[9]
        self.info = self.data[11]
