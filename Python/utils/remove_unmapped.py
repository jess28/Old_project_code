# Removes unmapped reads from a sam file.
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
    Removes unmapped .sam file reads and rewrites file.

    USAGE:
        python remove_unmapped.py <filename>

    ARGS:
        fil1, name and location of sam file
    """
    b = filename.split(".")[0] + "_clear.sam"
    with open(filename) as old:
        with open(b, 'wb') as new:
            for line in old:
                if line.startswith("@"):
                    new.write(line) # keep sam headers
                else:
                    col = line.split("\t")
                    if col[1] != '4': # 4 is the bitwise FLAG for unmapped reads
                        new.write(line)

if __name__ == '__main__':
    if len(argv) != 2:
        print main.__doc__
        exit()
    filename = argv[1]
    main()
