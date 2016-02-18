# Finds every locus's read coverage and alternate state.
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
from vcf_toolz import VCF

def main():
    """
    Writes to table every locus mapped in vcf (v4.1) file including read depth and
    alternate state. The file is created by samtools-0.1.19 mpileup (-g).

    USAGE:
        python alt_table_gatk.py <newfile> <gatkfile>

    ARGS:
        fil1, name and location of new table
        fil2, name and location of vcf file
    """
    table = open(newfile, 'wb')
    table.write("chrom" + "\t" + "locus" + "\t" + "depth" + "\t" + "alt" + "\n")
    chrom = ""
    locus = ""
    depth = ""
    alt = ""
    with open(newfile, 'wb') as table:
        with open(gatkfile) as gatk:
            for line in gatk:
                if not line.startswith('#'):
                    rec = VCF(line)
                    if locus == "":
                        locus = rec.pos
                        chrom = rec.chrom
                        if "INDEL" in rec.info.split(';')[0]:
                            depth = rec.info.split(';')[2].split('=')[1]
                            alt = '1'
                        elif '.' not in rec.alt:
                            depth = rec.info.split(';')[0].split('=')[1]
                            alt = '1'
                        else:
                            depth = rec.info.split(';')[0].split('=')[1]
                            alt = '0'
                    else:
                        if locus != rec.pos:
                            table.write(chrom + '\t' + locus + '\t' + depth + '\t' + alt + '\n')
                            locus = rec.pos
                            chrom = rec.chrom
                            if "INDEL" in rec.info.split(';')[0]:
                                depth = rec.info.split(';')[2].split('=')[1]
                                alt = '1'
                            elif '.' not in rec.alt:
                                depth = rec.info.split(';')[0].split('=')[1]
                                alt = '1'
                            else:
                                depth = rec.info.split(';')[0].split('=')[1]
                                alt = '0'
                        elif locus == rec.pos:
                            locus = rec.pos
                            chrom = rec.chrom
                            if "INDEL" in rec.info.split(';')[0]:
                                depth = rec.info.split(';')[2].split('=')[1]
                                alt = '1'
                            else:
                                depth = rec.info.split(';')[0].split('=')[1]
                                alt = '1'
            table.write(chrom + '\t' + locus + '\t' + depth + '\t' + alt + '\n')

if __name__ == '__main__':
    if len(argv) != 3:
        print(main.__doc__)
        exit()
    newfile = argv[1]
    gatkfile = argv[2]
    main()
