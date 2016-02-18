# Making sure that control and sample files for mHMM have matching positions
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
from collections import OrderedDict

def main():
    """
    Writes new file with both control and sample depths, using only the positions 
    that both have.

    USAGE:
        python3 pos_sort_mHMM.py <cont_file> <samp_file> <new_file>

    ARGS:
        cont_file: control file with position and depths
        samp_file: sample file with position and depths
        new_file: path to new file with both sample and control data
    """
    cont_dic = mk_dic(cont_file)
    samp_dic = mk_dic(samp_file)
    check_pos(cont_dic, samp_dic)

def mk_dic(pos_file):
    dic = OrderedDict()
    with open(pos_file) as pos:
        for line in pos:
            data = line.rstrip().split('\t')
            dic[data[0]] = data[1]
    return dic

def check_pos(cont_dic, samp_dic):
    with open(new_file, 'wb') as new:
        new.write(bytes(('Position' + '\t' + 'cont_dp' + '\t' + 'samp_dp' + '\n'), 'UTF-8'))
        for key in cont_dic.keys():
            if key in samp_dic:
                to_write = [key, cont_dic[key], samp_dic[key]]
                join_write = '\t'.join(to_write)
                new.write(bytes((join_write + '\n'), 'UTF-8'))
            else: 
                pass

if __name__ == '__main__':
    if len(argv) != 4:
        print(main.__doc__)
        exit()
    cont_file = argv[1]
    samp_file =  argv[2]
    new_file = argv[3]
    main()
