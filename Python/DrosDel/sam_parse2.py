# sam_parse2 does the same thing as sam_parse but using a dictionary.
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


from sys import argv, exit
from sam_toolz import SAMSplit

def main():
    """
    Summarize the MAPQ, pct. mapped, pct. indel for a .sam file.

    USAGE:
        python sam_parse.py <samfile> <fastqfile>

    ARGS:
        fil1, path to sam file to be processed
        fil2, path to fastq file from which sam file originated
    """
    num_seq = count_all()
    MAPQS = {}
    countindel = 0
    countsam = 0
    for line in open(samfile):
        if not line.startswith("@"):
            rec = SAMSplit(line)
            if rec.MAPQ in scores:
                MAPQS[k] += 1
            else:
                MAPQS[k] = 1
            if 'I' in rec.CIGAR or "D" in rec.CIGAR:
                countindel += 1
            countsam += 1
    sum = 0
    for k in MAPQS:
        sum += k * MAPQS[k]
    mean = sum/float(sum(MAPQS.values()))
    map_reads = countsam/float(num_seq)
    indel_rate = countindel/float(countsam)
    print "mean MAPQ:", mean
    print "indel rate:", indel_rate
    print "percent of mapped reads:", map_reads

def count_all():
    """ Counts the number of lines in the fastq file. """
    countfq = 0
    for line in open(fastqfile):
        if line.startswith("@"):
            countfq += 1
    return countfq


if __name__ == '__main__':
    if len(argv) != 3:
        print main.__doc__
        exit()
    samfile = argv[1]
    fastqfile = argv[2]
    main()
