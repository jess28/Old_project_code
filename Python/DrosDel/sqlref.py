# Test to see if fasta can be fed to sqlite for a table
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
from sys import argv


def main():
    """
    Makes table with chromosome, window number, and reference sequence in database

    USAGE:
        python sqlref.py <database> <fasta> <cg_table> <table> <drop_state>

    ARGS:
        database: name and location of database
        fasta: name and location of window sequence fasta
        cg_table: name and location of cg_content table
        table: name of table in database
        drop_state: 'drop' or 'no_drop' to table in database
    """
    cg, n = cg_n_cont(cg_table)
    data = mk_data(cg, n, fasta)
    writeTable(data)

def cg_n_cont(cg_table):
    cg = []
    n = []
    with open(cg_table) as tab:
        for line in tab:
            if not line.startswith('chrom'):
                temp = line.rstrip().split('\t')
                cg_temp = temp[2]
                n_temp = temp[3]
                cg.append(cg_temp)
                n.append(n_temp)
    return cg, n

def mk_data(cg, n, fasta):
    tot = []
    temp = []
    with open(fasta) as ref:
        chrom = ""
        win = 0
        data, seq = [], []
        for line in ref:
            if line.startswith('>') and chrom == "":
                head = line.rstrip().split(':')
                chrom = str(head[0][1:])
                win = head[1]
            elif line.startswith('>') and chrom != "":
                seqall = ''.join(seq)
                data.append(chrom)
                data.append(win)
                data.append(seqall)
                temp.append(tuple(data))
                head = line.rstrip().split(':')
                chrom = str(head[0][1:])
                win = head[1]
                seq = []
                data = []
            else:
                c = line.rstrip()
                seq.append(c)
        seqall = ''.join(seq)
        data.append(chrom)
        data.append(win)
        data.append(seqall)
        temp.append(tuple(data))
    index = range(len(cg))
    for i in index:
        d = temp[i] + (cg[i], n[i])
        tot.append(d)
    return tot

def writeTable(tot):
    a = 'INSERT INTO %s VALUES(?, ?, ?, ?, ?)' % table
    con = lite.connect(database)
    with con:
        cur = con.cursor()
        if drop_state == 'drop':
            cur.execute('DROP TABLE IF EXISTS %s' % table)
            cur.execute('CREATE TABLE %s(Chrom TEXT, Window TEXT, Seq TEXT, CG TEXT, N TEXT)' % table)
        cur.executemany(a, tot)

if __name__ == '__main__':
    dropargs = ['drop', 'no_drop']
    if len(argv) != 6 or argv[5] not in dropargs:
        print(main.__doc__)
        exit()
    database = argv[1]
    fasta = argv[2]
    cg_table = argv[3]
    table = argv[4]
    drop_state = argv[5]
    main()