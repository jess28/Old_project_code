# To pull ontology column with comma seperated data and join with database for
# view with names of ontologies associated with sequence.
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
    Pulls out comma seperated ontologies and splits on comma to join with 
    ontology names

    USAGE:
        python3 sql_split_data.py <database1> <database2> <table> <drop_state> <columns>
    ARGS:
        database1, path to sqlite database
        database2, path to ontology database
        table, name of table in database for parsing
        drop_state, whether to drop the joined table (drop or no_drop)
        columns, names of columns to pull out for joined table(put ontology column last)
    """
    tot = import_data(database1, database2, table, columns)
    ex_join(tot)

def import_data(database1, database2, table, columns):
    counter = 0
    names = ['SO', 'GO']
    count = 0
    for i in columns:
        if i != columns[-1]:
            names.insert(count, i)
            count += 1
    s = []
    for i in columns:
        s.append('%s')
        a = ', '.join(s)
    b = tuple(columns)
    data_0 = 'SELECT ' + a
    data_1 = data_0 % b
    data_2 = ' FROM %s' % table
    data = data_1 + data_2
    con1 = lite.connect(database1)
    con2 = lite.connect(database2)
    tot = []
    with con2:
        with con1:
            print('gathering data')
            cur2 = con2.cursor()
            cur1 = con1.cursor()
            cur1.execute(data)
            rows = cur1.fetchall()
            so = []
            go = []
            for row in rows:
                if so == [] and go == []:
                    print('new')
                    so = []
                    go = []
                    lis = list(row)
                    ont = lis[2].split(',')
                elif so != [] or go != []:
                    dt = []
                    dt.append(lis[0])
                    dt.append(lis[1])
                    dt.append('; '.join(so))
                    dt.append('; '.join(go))
                    tot.append(tuple(dt))
                    so = []
                    go = []
                    lis = list(row)
                    ont = lis[2].split(',')
                for i in ont:
                    if i != 'NA':
                        print(counter)
                        if i.startswith('!'):
                            i = i[1:]
                        table2 = i.split(':')[0] + "_dros"
                        pull = 'SELECT name FROM %s' % table2 + ' WHERE id GLOB "%s"' % i
                        cur2.execute(pull)
                        o = cur2.fetchone()
                        l = list(o)
                        l.insert(0, i)
                        ont_name = ": ".join(l)
                        if table2 == 'SO_dros':
                            so.append(ont_name)
                        elif table2 == 'GO_dros':
                            go.append(ont_name)
                        counter += 1
                    else:
                        so.append('NA')
                        go.append('NA')
    return tot

def ex_join(tot):
    print('Ready to execute')
    qlis = []
    for i in range(len(tot[0])):
        qlis.append("?")
    qmarks = ", ".join(qlis)
    new_table = 'onto_' + table
    insert_vals = 'INSERT INTO %s VALUES(%s)' % (new_table, qmarks)
    print(drop_state)
    con1 = lite.connect(database1)
    with con1:
        cur1 = con1.cursor()
        if drop_state == 'drop':
            print('dropping')
            drop_statement = 'DROP TABLE IF EXISTS %s' % new_table
            cur1.execute(drop_statement)
            make_table = 'CREATE TABLE %s(' % new_table + ' TEXT, '.join(names) + ' TEXT)'
            cur1.execute(make_table)
        print('executing')
        cur1.executemany(insert_vals, tot)
        print('done')



if __name__ == '__main__':
    drop_flag = ['drop', 'no_drop']
    if len(argv) < 5 or argv[4] not in drop_flag:
        print(main.__doc__)
        exit()
    database1 = argv[1]
    database2 = argv[2]
    table = argv[3]
    drop_state = argv[4]
    columns = argv[5:]
    main()