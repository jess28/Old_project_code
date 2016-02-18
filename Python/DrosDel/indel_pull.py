# indel_pull searches through a sam file and finds any CIGAR strings with
# indel marked and prints read to new sam file.
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
from sam_toolz import SAMSplit
import gzip

def main():
    """
    Prints reads from sam file with indels marked in the CIGAR string
    to new sam file.

    USAGE:
        python indel_pull.py <shortfile> <samfile>

    ARGS:
        fil1, name and location of new indel sam file.
        fil2, name and location of original sam file.
    """
    sam = open(shortfile, 'wb')
    for line in gzip.open(samfile, 'rb'):
        if line.startswith("@"):
            sam.write(line)
        elif not line.startswith("@"):
            rec = SAMSplit(line)
            if 'I' in rec.CIGAR or 'D' in rec.CIGAR:
                sam.write(rec.line)
    sam.close()

if __name__ == '__main__':
    if len(argv) != 3:
        print main.__doc__
        exit()
    shortfile = argv[1]
    samfile = argv[2]
    main()
