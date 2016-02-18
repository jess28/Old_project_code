# Creates table with chromosome name and length.
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
from pprint import pprint as pp

def main():
    """
    Makes table with chromosome name and length
    
    USAGE:
        python reftable_compiler.py <reftable> <reference>
    ARGS:
        fil1, name and location of new table.
        fil2, name and location of reference fasta file.
    """
    length = 0
    with open(reftable, 'wb') as table:
        with open(reference) as ref:
            for line in ref:
                if line.startswith('>'):
                    if length != 0:
                        table.write(str(length) + '\n')
                    c = line.split(" ")[0][1:]
                    table.write(c + '\t')
                    length = 0
                else:
                    length += len(line.rstrip())
            table.write(str(length))

if __name__ == '__main__':
    if len(argv) != 3:
        print main.__doc__
        exit()
    reftable = argv[1]
    reference = argv[2]
    main()
