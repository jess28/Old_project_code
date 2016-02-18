# ref_seq_win iterates through a reference fasta file to put the sequence
# of the reference per window into a new fasta
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
import pickle
import math


class subd():
    def __init__(self):
        self.st = 0
        self.en = 0
        self.seq = ""

def main():
    """
    Finds sequence of reference in a window size across an alignment with
    premade dictionary.

    USAGE:
        python ref_seq_win.py <reffile> <dictfile> <newfa> <winsize>

    ARGS:
        fil1, location and name of reference fasta
        fil2, location and name of pickled dictionary
        fil3, location and name of fasta to write filled dictionary
        fil4, size of window
    """
    pkl_dic = open(dictfile, 'rb')
    dic = pickle.load(pkl_dic)
    # winsize = get_window(dic)
    print winsize
    print "loaded"
    seqs = [] 
    chrom = ""
    with open(reffile) as ref:
        for line in ref:
            if line.startswith(">") and seqs == []:
                chrom = line.rstrip().split(" ")[0][1:]
                temp = dic[chrom]
            elif line.startswith(">") and seqs != []:
                seq = "".join(seqs)
                tw = (len(seq)//winsize) + 1
                w = range(0, tw)
                for i in w:
                    seq_frac = seq[temp[i].st:temp[i].en]
                    temp[i].seq = seq_frac
                chrom = line.rstrip().split(" ")[0][1:]
                temp = dic[chrom]
                seqs = []
            else:
                seqs.append(line.rstrip())
        seq = "".join(seqs)
        tw = (len(seq)//winsize) + 1
        w = range(0, tw)
        for i in w:
            seq_frac = seq[temp[i].st:temp[i].en]
            temp[i].seq = seq_frac
    with open(newfa, 'wb') as n:
        for k in dic.keys():
            for l in dic[k]:
                q = dic[k][l]
                chrom_head = "".join([">", k])
                to_write = ":".join([chrom_head, str(l), str(q.st), str(q.en)])
                n.write(to_write + '\n')
                for s in split_seq(q.seq):
                    n.write(s + '\n')

# def get_window(d):
#     "gives size of window found from empty dictionary"
#     keys = d.keys()
#     q = d[keys[0]].keys()
#     sz = d[keys[1]][q[0]].en - d[keys[1]][q[0]].st + 1
#     return sz

def split_seq(s):
    "splits total sequence in window into 50bp chucks for fasta file writing"
    for start in range(0, len(s), 50):
        yield s[start:start + 50]

if __name__ == '__main__':
    if len(argv) != 5:
        print main.__doc__
        exit()
    reffile = argv[1]
    dictfile = argv[2]
    newfa = argv[3]
    winsize = int(argv[4])
    main()
