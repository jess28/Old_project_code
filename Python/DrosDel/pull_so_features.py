# Pulls out SO_feature names from embl file and pretty prints a set
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

import pprint as pp
from sys import argv

def main():
    feat = set()
    with open(embl_file) as embl:
        for line in embl:
            if "SO_feature" in line:
                a = line[21:].split(' ; ')
                feat.add(a[0])
    pp.pprint(feat)

if __name__ == '__main__':
    if len(argv) != 2:
        print(main.__doc__)
        exit()
    embl_file = argv[1]
    main()