# Removes SO_feature from embl file so it can be parsed by BioPython SeqIO
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
    Gets rid of SO feature problem in embl file so it can be parsed by Bio SeqIO

    USAGE:
        python3 fix_embl.py <old_file> <new_file>
    ARGS:
        old_file: location of old embl file
        new_file: location of new embl file
    """
    fix_embl()

def fix_embl():
    with open(new_file, 'wb') as new:
        with open(old_file) as old:
            for line in old:
                if line.startswith('FT   SO_feature'):
                    a = line.split('SO_feature      ')
                    b = ''.join(a)
                    c = b.split(' ; SO:')
                    d = [c[0], c[-1][8:]]
                    while len(d[0]) < 20:
                        d[0] = d[0] + ' '
                    e = ' '.join(d)
                    new.write(e)
                else:
                    new.write(line)

if __name__ == '__main__':
    if len(argv) != 3:
        print(main.__doc__)
        exit()
    old_file = argv[1]
    new_file = argv[2]
    main()