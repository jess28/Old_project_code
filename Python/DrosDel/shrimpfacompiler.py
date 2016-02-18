# shrimpfacompiler changes fastq files to fasta format.
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


<<<<<<< HEAD
# Writes a command script that uses SHRiMP's fastq_to_fasta command to
# change fastq files into fasta format.


=======
>>>>>>> 7b737f77162bf22f7f665983dda9261a962e5252
from sys import argv

def main():
    """
    uses the shrimp command fastq_to_fasta to write a script to change a
    fastq file to a fasta file.

    USAGE:
        python shrimpfacompiler.py <filename> <fasta> <fastq>

    ARGS:
        fil1, name and location of new command file.
        fil2, location for new fasta files.
        fil3, names and locations for fastq files.
    """
    cmd = open(filename, 'wb')
    for fil in fastq:
        name = fil.split('/')[-1].split('.')[0]
        cmd.write("fastq_to_fasta " + fil + " > " + fasta + name +  ".fa")
    cmd.close

if __name__ == '__main__':
    if len(argv) < 4:
        print main.__doc__
        exit()
    filename = argv[1]
    fasta = argv[2]
    fastq = argv[3:]
    main()
