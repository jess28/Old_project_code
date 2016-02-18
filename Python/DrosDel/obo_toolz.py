# Module to parse obo format and insert information into sqlite table
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
import sqlite3 as lite

class obo_parse():
    def __init__(self, line):
        self.line = line
        self.data = self.line.rstrip().split(': ')
        self.key = self.data[0]
        self.value = ':'.join(self.data[1:])

def main():
    """Read an ontology (OBO format) into an SQLite database.

    USAGE:
        python obo_toolz.py <ontology> <database> <drop_flag>
    ARGS:
        ontology, path to an OBO file
        database, path to the database
        drop_flag, 'drop' or 'no_drop' for dropping table decision
    """
    emp_dic, keys = key_dict()
    full_dic = dict_fill(emp_dic, keys)
    sql_table(full_dic, keys)

def key_dict():
    "Return an empty dict for an OBO and a list of table fields."
    previous_line = ""
    d = {}
    key = []
    real_k = []
    with open(ontology) as obo:
        for line in obo:
            if line.startswith('[') and previous_line == "":
                previous_line = line
            elif line.startswith('[') and previous_line != "":
                for i in key:
                    if i not in d:
                        d[i] = []
                        real_k.append(i)
                previous_line = line
                key = []
            elif previous_line != "" and not line.startswith('[') and line != "\n":
                rec = obo_parse(line)
                key.append(rec.key)
        for i in key:
            if i not in d:
                d[i] = []
                real_k.append(i)
        previous_line = line
        key = []
    return d, real_k

def dict_fill(d, keys):
    "Return a list of tuples of OBO data to be loaded into db."
    previous_line = ""
    tot = []
    with open(ontology) as obo:
        for line in obo:
            data = []
            if line.startswith('[') and previous_line == "":
                previous_line = line
            elif line.startswith('[') and previous_line != "":
                for i in keys:
                    if d[i] != []:
                        a = ','.join(d[i])
                        data.append(a)
                    else:
                        data.append('NA')
                tot.append(tuple(data))
                for i in keys:
                    d[i] = []
                previous_line = line
            elif previous_line != "" and not line.startswith('[') and line != "\n":
                rec = obo_parse(line)
                d[rec.key].append(rec.value)
    return tot

def sql_table(tot, keys):
    "Write the data in tot with fields in keys to database."
    table = ontology.split('.')[0].split('/')[-1]
    qlis = []
    for i in range(len(tot[0])):
        qlis.append("?")
    qmarks = ", ".join(qlis)
    insert_vals = 'INSERT INTO %s VALUES(%s)' % (table, qmarks)
    make_table = 'CREATE TABLE %s(' % table + ' TEXT, '.join(keys) + ' TEXT)' 
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        if drop_flag == "drop":
            cur.execute('DROP TABLE IF EXISTS %s' % table)
            cur.execute(make_table)
        cur.executemany(insert_vals, tot)
        print("Should be successful...")

if __name__ == '__main__':
    dropargs = ['drop', 'no_drop']
    if len(argv) != 4 or argv[3] not in dropargs:
        print(main.__doc__)
        exit()
    ontology = argv[1]
    database = argv[2]
    drop_flag = argv[3]
    main()
