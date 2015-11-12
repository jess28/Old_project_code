# Removes fasta data from GFF file for easier parsing
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
    Makes new gff without fasta information.

    USAGE:
        python3 gff_no_fasta.py <gff_file> <new_file>

    ARGS:
        gff_file: path to orignal gff
        new_file: path to new fasta-less gff
    """
    fasta = False
    with open(gff_file) as gff:
        with open(new_file, 'wb') as new:
            for line in gff:
                if line.startswith('##FASTA'):
                    fasta = True
                else:
                    if fasta == False and not line.startswith("###"):
                        new.write(bytes(line, 'UTF-8'))

if __name__ == '__main__':
    if len(argv) != 3:
        print(main.__doc__)
        exit()
    gff_file = argv[1]
    new_file = argv[2]
    main()
