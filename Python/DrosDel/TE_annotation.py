# Pulls out annotations from GFF that correspond to TEs for use in the Tlex2 program
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
from GFF_toolz import GFF

def main():
    """
    Writes tab delimited file with name, chromosome, start and stop positions, and 
    strandedness from GFF annotation for use in the Tlex2 program.

    USAGE:
        python3 TE_annotation.py <gff_file> <te_table>

    ARGS:
        gff_file: location of gff
        te_table: location for new tab file
    """
    with open(gff_file) as gff:
        with open(te_table, 'wb') as te:
            for line in gff:
                if "transposable_element" in line:
                    rec = GFF(line)
                    attr = rec.atr.split(';')
                    name1 = ""
                    for i in attr:
                        if 'ID' in i:
                            name = i.split('=')[1]
                            if ',' in name:
                                name_lis = name.split(',')
                                for x in name_lis:
                                    if x.startswith('FB'):
                                        name1 = x
                            else:
                                if name.startswith('FB'):
                                    name1 = name
                    if name1 != "":
                        chrom = rec.chrom
                        st = str(rec.start)
                        en = str(rec.end)
                        strand = rec.strand
                        to_write_lis = [name1, chrom, st, en, strand]
                        to_write = '\t'.join(to_write_lis)
                        te.write(bytes((to_write + '\n'), 'UTF-8'))

if __name__ == '__main__':
    if len(argv) != 3:
        print(main.__doc__)
        exit()
    gff_file = argv[1]
    te_table = argv[2]
    main()