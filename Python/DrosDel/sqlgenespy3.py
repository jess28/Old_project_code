# Create sql table for gene information and what windows they are located in
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
from sys import argv, exit
from intersect_toolz import int_parse

def main():
    """
    Makes sqlite table for genes in each sliding window and all the information
    about them from the bedtools intersect file.

    USAGE:
        python sqlgenespy3.py <intersect> <table> <database> <w>

    ARGS:
        fil1: bedtools intersect file with window start and end and gene information
        fil2: sql table name (will drop if existing)
        fil3: sql database name (will create if not existing)
        fil4: window size
    NOTES:
        Make sure to use python 3 with this script
    """
    tot = []
    with open(intersect) as fil:
        for line in fil:
            data = []
            if len(line) > 1:
                rec = int_parse(line)
                win = find_winID(rec.wst, w)
                if int(rec.gst) != -1:
                    imp = rec.info.rstrip().split(';')
                    ID = imp[0].split('=')[1]
                    Name = imp[1].split('=')[1]
                    if imp[2].startswith('fullname'):
                        fullname = imp[2].split('=')[1]
                        if imp[3].startswith('Alias'):
                            Alias = imp[3].split('=')[1]
                            Ontology_term = imp[4].split('=')[1]
                            Dbxref = imp[5].split('=')[1]
                            GO, _ = split_ont(Ontology_term)
                            _, SO = split_ont(Ontology_term)
                            gst = rec.gst
                            gen = rec.gen
                        else:
                            Alias = 'NA'
                            Ontology_term = imp[3].split('=')[1]
                            Dbxref = imp[4].split('=')[1]
                            GO, _ = split_ont(Ontology_term)
                            _, SO = split_ont(Ontology_term)
                            gst = rec.gst
                            gen = rec.gen
                    else:
                        fullname = 'NA'
                        if imp[2].startswith('Alias'):
                            Alias = imp[2].split('=')[1]
                            Ontology_term = imp[3].split('=')[1]
                            Dbxref = imp[4].split('=')[1]
                            GO, _ = split_ont(Ontology_term)
                            _, SO = split_ont(Ontology_term)
                            gst = rec.gst
                            gen = rec.gen
                        else:
                            Alias = 'NA'
                            Ontology_term = imp[2].split('=')[1]
                            Dbxref = imp[3].split('=')[1]
                            GO, _ = split_ont(Ontology_term)
                            _, SO = split_ont(Ontology_term)
                            gst = rec.gst
                            gen = rec.gen
                else:
                    ID = 'NA'
                    Name = 'NA'
                    fullname = 'NA'
                    gst = 'NA'
                    gen = 'NA'
                    Alias = 'NA'
                    GO = 'NA'
                    SO = 'NA'
                    Dbxref = 'NA'
                data.append(ID)
                data.append(Name)
                data.append(fullname)
                data.append(gst)
                data.append(gen)
                data.append(Alias)
                data.append(GO)
                data.append(SO)
                data.append(Dbxref)
                data.append(rec.chrom)
                data.append(win)
                tot.append(tuple(data))
    writeTable(tot)

def find_winID(st, w):
    win = int(st)//int(w)
    return win

def split_ont(ont):
    tmp_ont = ont.split(',')
    go, so = [], []
    for i in tmp_ont:
        if i.startswith('GO'):
            go.append(i)
        elif i.startswith('SO'):
            so.append(i)
        GO = ','.join(go)
        SO = ','.join(so)
    return GO, SO

def writeTable(tot):
    qlis = []
    for i in range(len(tot[0])):
        qlis.append("?")
    qmarks = ", ".join(qlis)
    a = 'INSERT INTO %s VALUES(%s)' % (table, qmarks)
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        cur.execute('DROP TABLE IF EXISTS %s' % table)
        cur.execute('CREATE TABLE %s(ID TEXT, Name TEXT, Fullname TEXT, Start TEXT, END TEXT, Alias TEXT, GO TEXT, SO TEXT, Dbxref TEXT, Chrom TEXT, Window INT)' % table)
        cur.executemany(a, tot)
        print("Should be successful...")

if __name__ == '__main__':
    if len(argv) != 5:
        print(main.__doc__)
        exit()
    intersect = argv[1]
    table = argv[2]
    database = argv[3] 
    w = argv[4]
    main()
