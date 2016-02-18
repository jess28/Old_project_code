# Checks Fastq files for end of line characters and quality string versus 
# sequence length.

# Copyright (C) 2014 Jessica Strein, jessica.strein@uconn.edu
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

def EOL_check():
    """ Makes sure there is a \n at the end of each line. """
    for filename in filenames:
        with open(filename) as fil:
            for line in fil:
                if line[-1] != '\n':
                    print line

def qual_seq_comp():
    """
    Makes sure that the quality sequence length is the sequence length.
    """
    for filename in filenames:
        with open(filename) as fil:
            counter = ""
            count = []
            for line in fil:
                if line.startswith("@"):
                    counter = 1
                elif line.startswith("+"):
                    counter = 3
                else:
                    count.append(line.rstrip())
                    if counter == 3:
                        if len(count[0]) != len(count[1]):
                            print count
                            counter = ""
                            count = []
                        else:
                            counter = ""
                            count = []

def main():
    """
    Checks a fastq file for incorrect quality string length and missing \n
    characters.

    USAGE:
        python fastqchecker.py <fastqfile>

    ARGS:
        fil1, path to fastq file
    """
    EOL_check()
    qual_seq_comp()

if __name__ == '__main__':
    if len(argv) < 2:
        print main.__doc__
        exit()
    filenames = argv[1:]
    main()
