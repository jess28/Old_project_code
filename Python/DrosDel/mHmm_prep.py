# Uses VCF file to create control, sample and position files with R program mHMM.
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
from vcf_toolz import VCF

def main():
    """
    Creates control and sample files for each specified chromosome, position info
    is contained in both files.

    USAGE: 
        python3 mHmm_prep.py <control_vcf> <samp_vcf> <path> <fil_names>

    ARGS:
        control_vcf: vcf file to be used as control_vcf
        samp_vcf: vcf file to be used as the sample
        path: path to directory for new files
        fil_names: names of chromosomes as they are written in the vcf for names of new files
    """
    make_con()
    make_samp()

def make_con():
    for fil in fil_names:
        fil_loc = path + fil + '_con.tab'
        with open(control_vcf) as vcf:
            with open(fil_loc, 'wb') as pfile:
                for line in vcf:
                    if not line.startswith('#'):
                        rec = VCF(line)
                        if rec.chrom == fil:
                            to_write = [rec.pos, rec.info['DP']]
                            w = '\t'.join(to_write)
                            pfile.write(w + '\n')

def make_samp():
    for fil in fil_names:
        fil_loc = path + fil + '_samp.tab'
        with open(samp_vcf) as vcf:
            with open(fil_loc, 'wb') as pfile:
                for line in vcf:
                    if not line.startswith('#'):
                        rec = VCF(line)
                        if rec.chrom == fil:
                            to_write = [rec.pos, rec.info['DP']]
                            w = '\t'.join(to_write)
                            pfile.write(w + '\n')

if __name__ == '__main__':
    if len(argv) < 5:
        print(main.__doc__)
        exit()
    control_vcf = argv[1]
    samp_vcf = argv[2]
    path = argv[3]
    fil_names = argv[4:]
    main()