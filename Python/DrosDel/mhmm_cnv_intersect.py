# Finding intersections of CNVs from mhmm analysis
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
    Finds CNVs that intersect in position and records them in new file

    USAGE:
        python mhmm_cnv_intersect.py <file_1> <file_2> <new_file>

    ARGS:
        file_1: path to first CNV file
        file_2: path to second CNV file
        new_file: path to new file with recorded intersections
    """
    lis = grab_data()
    compare(lis)

def grab_data():
    lis = []
    with open(file_1) as one:
        for line in one:
            if not line.startswith("left"):
                data = line.rstrip().split('\t')
                dic = {'left' : int(data[0]), 'right' : int(data[1]), 'state' : data[2], 'length' : data[3], 'ratio' : data[4]}
                lis.append(dic)
    return lis

def compare(lis):
    with open(new_file, 'wb') as new:
        with open(file_2) as two:
            for line in two:
                if not line.startswith("left"):
                    data = line.rstrip().split('\t')
                    for i in lis:
                        if int(data[0]) in range(i["left"], i["right"] + 1) or data[1] in range(i["left"], i["right"] + 1):
                            to_write = ["first", str(i["left"]), str(i["right"]), i["state"], i["length"], i["ratio"]]
                            w_one = "\t".join(to_write)
                            two_write = "second" + "\t" + line
                            new.write(w_one + '\n' + two_write)

if __name__ == '__main__':
    if len(argv) != 4:
        print main.__doc__
        exit()
    file_1 = argv[1]
    file_2 = argv[2]
    new_file = argv[3]
    main()