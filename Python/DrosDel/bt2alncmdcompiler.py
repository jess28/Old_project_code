# Bowtie2 alignment code compiler for aln command
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

# Creates command file of aln code for Bowtie2 to be used in Stampede's
# launcher program.

from sys import argv

script, filename = argv

cmd = open(filename, 'wb')

fils = ['SRR332298', 'SRR332299', 'SRR332300', 'SRR332301', 'SRR332302']

for fil in fils:
    cmd.write("bowtie2 --very-sensitive-local --no-unal -x \
    $DATA/dmel-all-chromosome-r5.54 -U $FASTQ/" + fil + ".fastq \
    -S $ALIGN/" + fil + "vsenslocalnounal.sam" + "\n")
    cmd.write("bowtie2 --local --no-unal -x \
    $DATA/dmel-all-chromosome-r5.54 -U $FASTQ/" + fil + ".fastq \
    -S $ALIGN/" + fil + "localnounal.sam" + "\n")
cmd.close()
