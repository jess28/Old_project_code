# Inserts missing feature key into embl file
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
    Inserts feature key into embl file for each record

    USAGE:
        python fix_featurekey_embl.py <old_file> <new_file>
    ARGS:
        old_file: starting embl file location
        new_file: location for fixed file
    """
    insert_key()

def insert_key():
    previous_line = ''
    with open(new_file, 'wb') as new:
        with open(old_file) as old:
            for line in old:
                if previous_line == '':
                    previous_line = line
                elif not previous_line.startswith('FT') and line.startswith('FT'):
                    key = 'FH   Key             Location/Qualifiers' + '\n' + 'FH' + '\n'
                    new.write(previous_line)
                    new.write(key)
                    previous_line = line
                else:
                    new.write(previous_line)
                    previous_line = line

if __name__ == '__main__':
    if len(argv) != 3:
        print main.__doc__
        exit()
    old_file = argv[1]
    new_file = argv[2]
    main()