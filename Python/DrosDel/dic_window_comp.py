# dic_window_comp creates a dictionary to iterate with a user given window size
# through a table made by alt_table_gatk
# Copyright (C) 2014 Jessica Strein, jessica.strein@uconn.edu

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.


from sys import argv
import pickle

class subd():
    "creates bottom rung of dictionary for easy access"
    def __init__(self):
        self.st = 0
        self.en = 0
        self.depths = []
        self.hets = []

def main():
    """
    Makes a dictionary to iterate through a table and save to file with pickle.

    USAGE:
        python dic_window_comp.py <table> <s> <dicfile>

    ARGS:
        fil1, name and location of table file
        fil2, window size to use
        fil3, name and location for dictionary file.
    """
    depth_dic = {}
    with open(table) as t:
        for line in t:
            data = line.rstrip().split('\t')
            z = int(data[1])
            chrom = data[0]
            breaks = range(1, z, s)
            supd = {}
            i = 0
            while i < len(breaks) - 1:
                c = subd()
                c.st, c.en =breaks[i], breaks[i] + s - 1
                supd[i] = c
                depth_dic[chrom] = supd
                i += 1
            c = subd()
            c.st, c.en = breaks[i], z
            supd[i] = c
            depth_dic[chrom] = supd
    output = open(dicfile, 'wb')
    pickle.dump(depth_dic, output)

if __name__ == '__main__':
    if len(argv) != 4:
        print main.__doc__
        exit()
    table = argv[1]
    s = int(argv[2])
    dicfile = argv[3]
    main()
