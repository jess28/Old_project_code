# pulls IDs of all TEs from previously created TE table (TE_annotation.py)
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
    Pulls out IDs from file created with TE_annotation.py and puts in new file
    for use with tlex2

    USAGE:
        python3 TE_ID_pull.py <TE_file> <new_file>

    ARGS:
        TE_file: path to file created with TE_annotation.py
        new_file: path to new ID file
    """
    with open(TE_file) as TE:
        with open(new_file, 'wb') as new:
            for line in TE:
                data = line.rstrip().split("\t")
                new.write(bytes((data[0] + '\n'), 'UTF-8'))

if __name__ == '__main__':
    if len(argv) != 3:
        print(main.__doc__)
    TE_file = argv[1]
    new_file = argv[2]
    main()