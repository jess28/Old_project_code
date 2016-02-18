# Pulls out coordinates from Emerson CNV map to use flybase's converter to genome 6
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
    with open(CNV_map) as cnv:
        with open(new_file, 'wb') as new:
            for line in cnv:
                if not line.startswith('#'):
                    data = line.rstrip().split('\t')
                    print(data)
                    exit()
                    chrom = data[7]
                    st = data[11]
                    en = data[12]
                    to_write = chrom + ':' + st + '..' + en
                    new.write(bytes((to_write + '\n'), 'UTF-8'))

if __name__ == '__main__':
    if len(argv) != 3:
        print(main.__doc__)
        exit()
    CNV_map = argv[1]
    new_file = argv[2]
    main()
