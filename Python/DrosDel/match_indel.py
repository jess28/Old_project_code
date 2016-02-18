# match_indel will pull reads from .sam files that match the indel reads
# from the sam file made by the indel_pull script.
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
from sam_toolz import SAMSplit
import gzip

def main():
    """
    Creates a .sam file with reads that match the reads pulled using the
    indel_pull script.

    USAGE:
        python match_indel.py <newsam> <indelsam> <fullsam>

    ARGS:
        fil1, name of new sam file.
        fil2, name and location of indel sam file.
        fil3, name and location of full sam file to pull from.
    """
    reads = load_indel_ids()
    with open(newsam, 'wb') as matchsam:
        for line in gzip.open(fullsam):
            if line.startswith("@"):
                matchsam.write(line)
            else:
                #print "Hurray!"
                r = SAMSplit(line)
                if r.seqID in reads:
                    #print "Who's the boss?"
                    matchsam.write(line)
    #print "I did it!"

def load_indel_ids():
    """
    Puts seqIDs of indel reads into set.
    """
    indels = set()
    for line in gzip.open(indelsam):
        if not line.startswith("@"):
            i = SAMSplit(line)
            indels.add(i.seqID)
    #print "Made the set."
    return indels

if __name__ == '__main__':
    if len(argv) != 4:
        print main.__doc__
        exit()
    newsam = argv[1]
    indelsam = argv[2]
    fullsam = argv[3]
    main()
