# Code to parse a gff file for only genes for use in IGV
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

from sys import argv
from GFF_toolz import GFF

def main():
    """
    Creates .gff file with only gene information and no repeats.

    USAGE:
        python gff_genes.py <newgff> <oldgff>

    ARGS:
        fil1, name and location for new .gff file.
        fil2, name and location of old .gff file.
    """
    seq = set()
    start = set()
    with open(newgff, 'wb') as new:
        with open(oldgff) as old:
            for line in old:
                if line.startswith("##"):
                    new.write(line)
                elif line.startswith("##FASTA"):
                    new.write(line)
                    fasta(seq)
                else:
                    rec = GFF(line)
                    if "gene" in rec.typ and rec.start not in start:
                        new.write(line)
                        start.add(rec.start)
                        seq.add(rec.typ)

def fasta(seq):
    """
    Adds on the fasta sequences at the end of the file.
    """
    

if __name__ == '__main__':
    if len(argv) != 3:
        print main.__doc__
        exit()
    newgff = argv[1]
    oldgff = argv[2]
    main()
