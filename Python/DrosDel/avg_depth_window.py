# Avg_depth_window iterates through a table made by alt_table_gatk using a
# dictionary made from dic_window_comp and finds depth and number of alts.
# Copyright (C) 2014 Jessica Strein, jessica.strein@uconn.edu
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

from sys import argv, exit
from depth_alt_toolz import table
import pickle
import math


class subd():
    def __init__(self):
        self.st = 0
        self.en = 0
        self.depths = []
        self.hets = []

def main():
    """
    Finds depth and number of alts in a window size across an alignment with
    premade dictionary.

    USAGE:
        python avg_depth_window.py <tablefile> <dictfile> <newfile> <winsize>

    ARGS:
        fil1, location and name of table to parse
        fil2, location and name of pickled dictionary
        fil3, location and name of file to write filled dictionary
        fil4, size of the window to use
    """
    pkl_dic = open(dictfile, 'rb')
    dic = pickle.load(pkl_dic)
    # winsize = get_window(dic)
    print winsize
    print "loaded"
    with open(tablefile) as t:
        counter = 0
        for line in t:
            rec = table(line)
            temp = dic[rec.chrom]
            w = rec.pos // int(winsize)
            temp[w].depths.append(rec.depth)
            temp[w].hets.append(rec.alt)
    with open(newfile, 'wb') as n:
        to_write = '\t'.join(['chrom', 'window', 'num_bp', 'mean_dp', 
        'dp_var', 'dp_sd', 'mean_snp', 'num_snp'])
        n.write(to_write + '\n')
        for k in dic.keys():
            for l in dic[k]:
                q = dic[k][l]
                if len(q.depths) == 0:
                    to_write = '\t'.join([str(k), str(l), str(len(q.depths)), "NA",
                    "NA", "NA", "NA", "NA"])
                    n.write(to_write + '\n')
                if len(q.depths) == 1:
                    to_write = '\t'.join([str(k), str(l), str(len(q.depths)), str(q.depths), "NA", "NA", "NA", str(q.hets)])
                    n.write(to_write + '\n')
                if len(q.depths) > 1:
                    m = mean(q.depths)
                    p, _ = snp(q.hets)
                    _, s = snp(q.hets)
                    v = var(q.depths, m)
                    sd = stdev(v)
                    to_write = '\t'.join([str(k), str(l), str(len(q.depths)), 
                    str(m), str(v), str(sd), str(s), str(p)])
                    n.write(to_write + '\n')

# def get_window(d):
#     keys = d.keys()
#     q = d[keys[0]].keys()
#     sz = d[keys[1]][q[0]].en - d[keys[1]][q[0]].st + 1
#     return sz

def mean(x):
    dm = sum(x)/len(x)
    return dm

def snp(l):
    snp = sum(l)
    msnp = float(snp)/len(l)
    return snp, msnp

def var(pl, m):
    sd = [(p - m)**2 for p in pl]
    ssd = sum(sd)
    v = ssd/(len(pl) - 1)
    return v

def stdev(s):
    sd = math.sqrt(s)
    return sd

if __name__ == '__main__':
    if len(argv) != 5:
        print main.__doc__
        exit()
    tablefile = argv[1]
    dictfile = argv[2]
    newfile = argv[3]
    winsize = argv[4]
    main()
