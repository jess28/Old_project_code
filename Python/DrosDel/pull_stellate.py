# pulls out read ids mapped to stellate region
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
from sam_toolz import SAMSplit

def main():
    """
    Grabs read IDs that map to the stellate cluster on the X in D. melanogaster

    USAGE:
        python3 pull_stellate.py <sam_file> <new_file>
    ARGS:
        sam_file: path to sam file
        new_file: path to file with read IDs found
    """
    with open(new_file, 'wb') as new:
        with open(sam_file) as sam:
            for line in sam:
                if not line.startswith('@'):
                    rec = SAMSplit(line)
                    if rec.refseq == 'X':
                        end = int(rec.pos) + 36
                        if int(rec.pos) > 14046000 and int(rec.pos) < 14062000:
                            new.write(bytes((rec.seqID + '\n'), 'UTF-8'))
                        elif end > 14046000 and end < 14062000:
                            new.write(bytes((rec.seqID + '\n'), 'UTF-8'))

if __name__ == '__main__':
    if len(argv) != 3:
        print(main.__doc__)
        exit()
    sam_file = argv[1]
    new_file = argv[2]
    main()
