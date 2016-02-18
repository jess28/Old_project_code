# Parses mpileup results for variation frequency and total number of called basepairs.
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
    Parses an mpileup vcf for variation and total number of called basepairs.

    USAGE:
        python mpileup_parse.py <mpileupvcf> <newfile>

    ARGS:
        fil1, filename and location of mpileup created vcf
        fil2, filename and location of new table
    """
    dic = {'hom_alt' : 0, 'het_alt' : 0, 'n_del' : 0, 'n_ins' : 0, 'snp' : 0}
    counter = 0
    new = open(newfile, 'wb')
    with open(mpileupvcf) as vcf:
        for line in vcf:
            if not line.startswith("#"):
                counter += 1
                rec = VCF(line)
                s302 = rec.s302.split(":")
                indel = rec.info.split(";")[0]
                if indel == "INDEL":
                    if len(rec.alt) == 1:
                        dic['n_del'] += 1
                        if s302[0] == '1/1': 
                            dic['hom_alt'] += 1 
                        elif s302[0] == '0/1':
                            dic['het_alt'] += 1
                    elif len(rec.alt) > 1:
                        dic['n_ins'] += 1
                        if s302[0] == '1/1': 
                            dic['hom_alt'] += 1 
                        elif s302[0] == '0/1':
                            dic['het_alt'] += 1
                elif len(rec.ref) == len(rec.alt) and "." not in rec.alt:
                    dic['snp'] += 1
                    if s302[0] == '1/1':
                        dic['hom_alt'] += 1
                    elif s302[0] == '0/1':
                        dic['het_alt'] += 1

                
    dic['Total_alts'] = dic['snp'] + dic['n_del'] + dic['n_ins']
    sample = mpileupvcf.split('/')[-1].split('.')[0]
    lis = [sample, str(dic['n_del']), str(dic['n_ins']), str(dic['snp']), str(dic['hom_alt']), str(dic['het_alt']), str(dic['Total_alts']), str(counter)]
    a = '\t'.join(lis)
    new.write(a)

if __name__=='__main__':
    if len(argv) != 3:
        print(main.__doc__)
        exit()
    mpileupvcf = argv[1]
    newfile = argv[2]
    main()
