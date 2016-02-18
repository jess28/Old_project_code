# Replaces the old version coordinates with new version coordinates for Emerson CNV map
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
    coor = mk_coor_ls()
    rplc_coor(coor)

def mk_coor_ls():
    coor = []
    with open(coords_file) as coords:
        for line in coords:
            data = line.rstrip().split('\t')
            newcor = data[1].split(':')[1]
            coor.append(newcor)
    return coor

def rplc_coor(coor):
    cnt = 0
    with open(CNV_file) as cnv:
        with open(new_file, 'wb') as new:
            for line in cnv:
                if line.startswith('#'):
                    new.write(bytes(line, 'UTF-8'))
                else:
                    c = coor[cnt].split('..')
                    data = line.rstrip().split('\t')
                    data[11] = c[0]
                    data[12] = c[1]
                    to_write = '\t'.join(data)
                    new.write(bytes((to_write + '\n'), 'UTF-8'))
                    cnt += 1

if __name__ == '__main__':
    if len(argv) != 4:
        print(main.__doc__)
        exit()
    coords_file = argv[1]
    CNV_file = argv[2]
    new_file = argv[3]
    main()