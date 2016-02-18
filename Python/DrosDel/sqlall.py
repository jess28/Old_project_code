# Parses bedtools intersect with all info about genome per window into sql table
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
from intersect_toolz import int_parse

def main():
    """Read a bedtools intersect file with all info about genome per window
    into an SQLite database.

    USAGE:
        python sqlall.py <bedfile> <database> <table> <drop_flag>
    ARGS:
        bedfile, path to intersect file
        database, path to the database
        table, name of table in database
        drop_flag, "drop" or "no_drop" for table in database
    """
    emp_dic, keys = key_dict(bedfile)
    sql_table(keys)
    full_dic = dict_fill(emp_dic, keys, bedfile)
    sql_ex(full_dic)

def key_dict(bedfile):
    "Return an empty dict for a bedtools intersect and a list of table fields."
    print("making dict...")
    d = {}
    key = []
    real_k = []
    with open(bedfile) as bed:
        for line in bed:
            rec = int_parse(line)
            info = rec.info.rstrip().split(';')
            for i in info:
                tmp = i.split('=')[0]
                key.append(tmp.replace("-", "_"))
            for k in key:
                if k not in d:
                    d[k] = ""
                    real_k.append(k)
            key = []
    return d, real_k

def find_winID(st, en):
    "Find window number for item."
    w = int(en) - int(st) + 1
    win = int(st)//int(w)
    return win

def dict_fill(d, keys, bedfile):
    "Return a list of tuples of notable sequence data to be loaded into db."
    print("making tuples...")
    tot = []
    with open(bedfile) as bed:
        for line in bed:
            data = []
            rec = int_parse(line)
            w = find_winID(rec.wst, rec.wen)
            info = rec.info.rstrip().split(';')
            for i in info:
                a = i.split('=') 
                k = a[0].replace("-", "_")
                dat = a[1]
                d[k] = dat
            for k in keys:
                if d[k] != "":
                    data.append(d[k])
                else:
                    data.append("NA")
            data.append(rec.gst)
            data.append(rec.gen)
            data.append(rec.db)
            data.append(rec.type)
            data.append(str(w))
            data.append(rec.chrom)
            tot.append(tuple(data))
            data = []
            for k in keys:
                d[k] = ""
            if len(tot)%1000000 == 0:
                sql_ex(tot)
                tot = []
    return tot

def sql_table(keys):
    print("creating table...")
    "Write the data in tot with fields in keys to database."
    make_table = 'CREATE TABLE %s(' % table + ' TEXT, '.join(keys) + ' TEXT, gene_start TEXT, gene_end TEXT, db_loc TEXT, type TEXT, window TEXT, chrom TEXT)' 
    con = lite.connect(database)
    with con:
        print("opening database")
        cur = con.cursor()
        if drop_flag == "drop":
            print("dropping table")
            drop_state = 'DROP TABLE IF EXISTS %s' % table
            cur.execute(drop_state)
            print("help")
            cur.execute(make_table)
            print("done")

def sql_ex(tot):
    "Add tuples of data into table."
    print('recording')
    qlis = []
    for i in range(len(tot[0])):
        qlis.append("?")
    qmarks = ", ".join(qlis)
    insert_vals = 'INSERT INTO %s VALUES(%s)' % (table, qmarks)
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        cur.executemany(insert_vals, tot)

if __name__ == '__main__':
    dropargs = ['drop', 'no_drop']
    if len(argv) != 5 or argv[4] not in dropargs:
        print(main.__doc__)
        exit()
    bedfile = argv[1]
    database = argv[2]
    table = argv[3]
    drop_flag = argv[4]
    main()
