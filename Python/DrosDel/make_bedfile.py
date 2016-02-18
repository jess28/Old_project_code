# Creates a bed file from fa made by ref_seq_win with chromosome and start and 
# end positions
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
    Creates bed file from fasta fil with chromosome, window number, and start, 
    and end positions in header.

    USAGE:
        python make_bedfile.py <fastafil> <bedfil>
    
    ARGS:
        fil1, name and location of fasta file to parse.
        fil2, name and location of bed file to create.
    """ 
    with open(fastafil) as fasta:
        with open(bedfil, 'wb') as bed:
            for line in fasta:
                if line.startswith(">"):
                    head = line.rstrip().split(":")
                    chrom = head[0][1:]
                    start = head[2]
                    end = head[3]
                    to_write = '\t'.join([chrom, start, end])
                    bed.write(to_write + '\n')

if __name__ == '__main__':
    if len(argv) != 3:
        print main.__doc__
        exit()
    fastafil = argv[1]
    bedfil = argv[2]
    main()