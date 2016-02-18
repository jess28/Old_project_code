# fastqdumpcompiler creates the code to use fastq-dump to change sra to fastq.
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
    Creates command file for stampede launcher for changing SRA files
    to fastq files with use of fastq-dump from the SRAtoolkit.

    USAGE:
        python fastqdumpcompiler.py <filename> <fastq> <SRA>

    ARGS:
        fil1, name and location for new command file.
        fil2, location for new fastq files.
        fil3 to infinity, name and location of SRA files.
    """
    cmd = open(filename, 'wb')
    for fil in sra:
        cmd.write("fastq-dump -O " + fastq + " " + fil + "\n")
    cmd.close

if __name__ == '__main__':
    if len(argv) < 4:
        print main.__doc__
        exit()
    filename = argv[1]
    fastq = argv[2]
    sra = argv[3:]
