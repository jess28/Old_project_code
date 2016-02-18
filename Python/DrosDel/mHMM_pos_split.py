# Splits mHMM pos files into 4MB pieces w/ 500KB overlap
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
    Creates series of files for mHMM program with 4MB each and a 500KB overlap.

    USAGE:
        python3 mHMM_pos_split.py <pos_file>

    ARGS:
        pos_file: full positon/control depth/sample depth file location

    NOTES:
        All new files will be labeled as the original plus number (in order of 
        position) in same location as original.
    """
    count = 1
    pos, con, sam = [], [], []
    fil = open(pos_file)
    for line in fil:
        if not line.startswith("Position"):
            if len(pos) == 4000000:
                write(pos, con, sam, count)
                pos = pos[3500000:]
                con = con[3500000:]
                sam = sam[3500000:]
                count += 1
            else:
                data = line.rstrip().split('\t')
                pos.append(data[0])
                con.append(data[1])
                sam.append(data[2])
    write(pos, con, sam, count)
    fil.close()

def write(pos, con, sam, count):
    name = pos_file.split('.')[0] + '_' + str(count) + '.tab'
    with open(name, 'wb') as new:
        lines = ['\t'.join([pos[x], con[x], sam[x]]) for x in range(len(pos))]
        to_write = "Position\tcont_dp\tsamp_dp\n" + '\n'.join(lines)
        new.write(bytes((to_write + '\n'), 'UTF-8'))

if __name__ == '__main__':
    if len(argv) != 2:
        print(main.__doc__)
        exit()
    pos_file = argv[1]
    main()