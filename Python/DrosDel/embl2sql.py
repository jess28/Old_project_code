# Uses embl_toolz to create sqlite table from embl file with SO_features
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

import sqlite3 as lite
from embl_toolz import EMBL
from sys import argv

def main():
    records = make_rec()

def make_rec():
first = True
records = []
record = []
with open(embl_file) as embl:
    for line in embl:
        head = line[:2]
        if head == 'ID' and first == True:
            record.append(line)
            first = False
        elif head == 'ID' and first == False:
            records.append(record)
            record = []
            record.append(line)
        elif first == False:
            record.append(line)
return records

def make_sqlite():
    make_table = 'CREATE TABLE %s(' % table + ' TEXT, '.join(keys) + ' TEXT)'

if __name__ == '__main__':
    if len(argv) != 3:
        print(main.__doc__)
        exit()
    embl_file = argv[1]
    database = argv[2]
    table = argv[3]
    main()