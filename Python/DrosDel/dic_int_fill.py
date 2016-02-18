# Fills the empty intersect dictionary with the appropriate genes.
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

from sys import argv
from intersect_toolz import int_parse
import pickle

class subd():
    "creates bottom rung of dictionary for easy access"
    def __init__(self):
        self.wst = 0
        self.wen = 0
        self.gname = {}

def main():
    """
    fills empty intersect dictionary, and pickles filled dictionary for easy access

    USAGE:
        python dic_int_fill.py <dictfile> <bedfile> <new_dict>
    
    ARGS:
        fil1, location of empty pickled dictionary
        fil2, location of intersect file
        fil3, name of new pickled dictionary
    """ 
    pkl_dic = open(dictfile, 'rb')
    dic = pickle.load(pkl_dic)
    winsize = get_window(dic)
    with open(bedfile) as bed:
        for line in bed:
            rec = int_parse(line)
            temp = dic[rec.chrom]
            w = int(rec.wen)/winsize
            if len(rec.info) > 1:
                name = rec.info.split(';')[1].split('=')[1]
            else:
                name = "NA"
            size = [rec.gst, rec.gen]
            temp[w].gname[name] = size
    output = open(new_dict, 'wb')
    pickle.dump(dic, output)

def get_window(d):
    keys = d.keys()
    q = d[keys[0]].keys()
    sz = d[keys[1]][q[0]].wen - d[keys[1]][q[0]].wst + 1
    return sz

if __name__ == '__main__':
    if len(argv) != 4:
        print main.__doc__
        exit()
    dictfile = argv[1]
    bedfile = argv[2]
    new_dict = argv[3]
    main()
