# Allows removal of unwanted line from samfile.
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
    Allows removal of unwanted .sam file line and rewrites file.

    USAGE:
        python clear_sam.py <nline> <filename>

    ARGS:
        nline: unwanted line number
        filename: path to sam file
    """
    counter = 1
    b = filename.split(".")[0] + "_clear.sam"
    with open(filename) as old:
        with open(b, 'wb') as new:
            for line in old:
                if counter != nline:
                    counter += 1
                    new.write(line)
                    if counter % 1000000 == 0:
                        print counter # to keep track of progress
                else:
                    print line
                    a = raw_input("Delete? (y/n) > ")
                    if a == "n":
                        counter += 1
                        new.write(line) # this will write the same file you already have
                    elif a == "y":
                        counter += 1

if __name__ == '__main__':
    if len(argv) != 3:
        print main.__doc__
        exit()
    nline = int(argv[1])
    filename = argv[2]
    main()
