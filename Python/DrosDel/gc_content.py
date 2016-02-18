# give the GC and N content percentage per scaffold for fasta file
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

def main():
    """
    Find GC and N percent content of fasta scaffold

    USAGE:
        python gc_content.py <table> <fastafil>
    
    ARGS:
        fil1, file to write data found
        fil2, fasta file to count
    """ 
    seqs = []
    chrom = ""
    win = ""
    with open(table, 'wb') as new:
        to_write = '\t'.join(["chrom", "win", "gc_per", "n_per"])
        new.write(to_write + '\n')
        with open(fastafil) as fasta:
            for line in fasta:
                if line.startswith(">") and seqs == []:
                    scaff = line.rstrip().split(":")
                    chrom = scaff[0][1:]
                    win = scaff[1]
                if line.startswith(">") and seqs != []:
                    seq = "".join(seqs)
                    gc_per = gc_cont(str(seq))
                    n_per = n_count(str(seq))
                    to_write = '\t'.join([str(chrom), str(win), str(gc_per), str(n_per)])
                    new.write(to_write + '\n')
                    scaff = line.rstrip().split(":")
                    chrom = scaff[0][1:]
                    win = scaff[1]
                    seqs = []
                else:
                    seqs.append(line.rstrip())

def gc_cont(s):
    G = s.count("G")
    C = s.count("C")
    g = s.count("g")
    c = s.count("c")
    tot = len(s)
    gccount = G + C + g + c
    gc_per = gccount/float(tot)
    return gc_per

def n_count(s):
    N = s.count("N")
    tot = len(s)
    n_per = N/float(tot)
    return n_per

if __name__ == '__main__':
    if len(argv) != 3:
        print main.__doc__
        exit()
    table = argv[1]
    fastafil = argv[2]
    main()