# Removes Het and U scaffolds from .sam file
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
import gzip

chrom = ["\t4\t", "\t3R\t", "\t3L\t", "\t2R\t", "\t2L\t", "\tX\t"]

def main():
    """
    Makes samfile (no header) with no het or mitochondrian scaffolds

    USAGE:
        python remove_het.py <hetfile> <nohet>

    ARGS:
        fil1, path to original sam file
        fil2, path to new sam file
    """
    old = gzip.open(hetfile) 
    new = open(nohet, 'wb')
    for line in old:
        for i in chrom:
            if i in line:
                new.write(line)
    old.close()
    new.close()

if __name__ == '__main__':
    if len(argv) != 3:
        print main.__doc__
        exit()
    hetfile = argv[1]
    nohet = argv[2]
    main()