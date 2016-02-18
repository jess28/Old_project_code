# Uses read IDs found by pull_stellate.py to find any multi-mapped to Uextra
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
    Pulls out reads that mapped to both the stellate cluster on the X and the Uextra

    USAGE:
        python3 stel_uextra.py <id_file> <sam_file> <multi_file>
    ARGS:
        id_file: path to file with stellate read ids
        sam_file: path to sam file to check
        multi_file: path to file to write multi-mapped ids
    """
    with open(id_file) as ids:
        with open(sam_file) as sam:
            with open(multi_file, 'wb') as multi:
                for line in sam:
                    if not line.startswith('@'):
                        rec = SAMSplit(line)
                        if rec.refseq == 'Uextra':
                            for line in ids:
                                read = line.rstrip()
                                if read == rec.seqID:
                                    multi.write(bytes((read + '\n'), 'UTF-8'))

if __name__ == '__main__':
    if len(argv) != 4:
        print(main.__doc__)
        exit()
    id_file = argv[1]
    sam_file = argv[2]
    multi_file = argv[3]
    main()