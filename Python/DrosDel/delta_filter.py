# filters out unnessacery scaffolds from a delta file generated by NUCmer
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
    yes = False
    want = ['X', '2L', '2R', '3L', '3R', '4']
    with open(old_file) as old:
        with open(new_file, 'wb') as new:
            for line in old:
                if line.startswith('/'):
                    new.write(bytes((line), 'UTF-8'))
                elif line.startswith('NUC'):
                    new.write(bytes((line), 'UTF-8'))
                elif line.startswith('>'):
                    data = line.rstrip().split(' ')
                    if data[1] in want:
                        new.write(bytes((line), 'UTF-8'))
                        yes = True
                    else: 
                        yes = False
                else:
                    if yes == True:
                        new.write(bytes((line), 'UTF-8'))

if __name__ == '__main__':
    if len(argv) != 3:
        print(main.__doc__)
        exit()
    old_file = argv[1]
    new_file = argv[2]
    main()