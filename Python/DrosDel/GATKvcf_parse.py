# Parses GATK results for read depth and variation frequency.
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
from vcf_toolz import VCF

def main():
    """
    Parses a GATK vcf for read depth and variation.

    USAGE:

    ARGS:
    """
    dic = {}
    with open(gatkvcf) as vcf:
        for line in vcf:
            if "##fileformat=VCFv4.1" in line:
                if not line.startswith("##"):
                    rec = VCF(line)
                    s302 = rec.s302.split(":")
                    if len(s302) = 2:
                        if float(s302[1]) > 5:
                            dic['n_cover_5'] += 1
                        elif float(s302[1]) > 2:
                            dic['n_cover_2'] += 1
                        elif float(s302[1]) > 1:
                            dic['n_cover_1'] += 1
                    elif len(s302) > 2:
                        if float(s302[2]) > 5:
                            dic['n_cover_5'] += 1
                        elif float(s302[2]) > 2:
                            dic['n_cover_2'] += 1
                        elif float(s302[2]) > 1:
                            dic['n_cover_1'] += 1
                        # Finds type of alt
                        if s302[0] == '1/1' and s302[3] > 29:
                            dic['hom_alt'] += 1
                        elif s302[0] == '0/1' and s302[3] > 29:
                            dic['het_alt'] =+ 1
                    ref = rec.ref
                    alt = rec.alt
                    if len(ref) != 1:
                        dic['n_del'] += 1
                    elif len(alt) != 1:
                        dic['n_ins'] += 1
            else:
                print """
                Your vcf file must be version 4.1 for this code to work. Please
                go to https://github.com/samtools/hts-specs for an explanation
                of the version.
                """

if __name__='__main__':
    if len(argv) != 1
        print main.__doc__
        exit()
    gatkvcf = argv[1]
    main()
