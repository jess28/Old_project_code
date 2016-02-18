# Concatinates variation count tables into one
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

def main():
    """
    Concatinates variation count tables into one.

    USAGE:
        python cat_count.py <newtable> <filenames>

    ARGS:
        fil1, name and location for new table.
        fil2:, names and locations of table files.
    """
    new = open(newtable, 'wb')
    header = ['sample', 'n_del', 'n_ins', 'snp', 'hom_alt', 'het_alt', 'total_alts', 'total_bp']
    new.write('\t'.join(header) + '\n')
    for fil in filenames:
        for line in open(fil):
            new.write(line + '\n')

if __name__=='__main__':
    if len(argv) < 4:
        print main.__doc__
        exit()
    newtable = argv[1]
    filenames = argv[2:]
    main()