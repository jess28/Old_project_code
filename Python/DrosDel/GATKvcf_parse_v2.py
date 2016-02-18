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
    Parses a GATK vcf for read depth and variation and creates a new table.
    Must have vcf_toolz installed to use this code.

    USAGE:
        python GATKvcf_parse_v2.py <gatkvcf> <newfile>

    ARGS:
        gatkvcf: filename and location of gatk created vcf
        newfile: filename and location of new table
    """
    dic = {'n_cover_1' : 0, 'n_cover_2' : 0, 'n_cover_5' : 0, 'hom_alt' : 0, 'het_alt' : 0, 'n_del' : 0, 'n_ins' : 0, 'snp' : 0}
    new = open(newfile, 'wb')
    with open(gatkvcf) as vcf:
        for line in vcf:
            if not line.startswith("#"):
                rec = VCF(line)
                s302 = rec.s302.split(":")
                if len(s302) == 1:
                    if int(s302[1]) > 5:
                        dic['n_cover_5'] += 1
                    elif int(s302[1]) > 2:
                        dic['n_cover_2'] += 1
                    elif int(s302[1]) > 1:
                        dic['n_cover_1'] += 1
                elif len(s302) > 2:
                    if int(s302[2]) > 5:
                        dic['n_cover_5'] += 1
                    elif int(s302[2]) > 2:
                        dic['n_cover_2'] += 1
                    elif int(s302[2]) > 1:
                        dic['n_cover_1'] += 1
                  # Finds type of alt
                    if s302[0] == '1/1' and s302[3] > 29:
                        dic['hom_alt'] += 1
                    elif s302[0] == '0/1' and s302[3] > 29:
                        dic['het_alt'] += 1
                ref = rec.ref
                alt = rec.alt
                if len(ref) != 1:
                    dic['n_del'] += 1
                elif len(alt) != 1:
                    dic['n_ins'] += 1
                elif len(ref) == len(alt) and "." not in alt:
                    dic['snp'] += 1

                
    dic['Total_alts'] = dic['snp'] + dic['n_del'] + dic['n_ins']
    new.write(gatkvcf + '\n')
    new.write("n_del" + "\t" + "n_ins" + "\t" + 'snp' + '\t' + 'hom_alt' + '\t' + 'het_alt' + '\t' + "Total_alts" + '\n')
    new.write(str(dic['n_del']) + '\t' + str(dic['n_ins']) + '\t' + str(dic['snp']) + '\t' + str(dic['hom_alt']) + '\t' + str(dic['het_alt']) + '\t' + str(dic['Total_alts']))

if __name__=='__main__':
    if len(argv) != 3:
        print main.__doc__
        exit()
    gatkvcf = argv[1]
    newfile = argv[2]
    main()
