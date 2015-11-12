# shrimpfacompiler writes a command file to change fastq files to fasta format.
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
    uses the shrimp command fastq_to_fasta to write a script to change a
    fastq file to a fasta file. Useful when you have many files to convert
    at the same time.

    USAGE:
        python shrimpfacompiler.py <filename> <fasta> <fastq>

    ARGS:
        filename: name and location of new command file.
        fasta: path to new fasta files. They will be named the same as the fq files
        fastq: names and locations for fastq files.
    """
    cmd = open(filename, 'wb')
    print filename
    for fil in fastq:
	print fil
	fastaname = fasta + fil.split(".")[0].split("/")[-1]
	print fastaname
        cmd.write("fastq_to_fasta " + fil + " > " + fastaname + ".fa" + "\n")
    cmd.close

if __name__ == '__main__':
    if len(argv) < 4:
        print main.__doc__
        exit()
    filename = argv[1]
    fasta = argv[2]
    fastq = argv[3:]
    main()
