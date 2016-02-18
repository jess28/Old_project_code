# Pulls out indels from a vcf file and writes to new file.
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
    Pulls out 100 insertions and 100 deletions from a vcf file and writes to
    new.

    USAGE:
        python vcf_indelpull.py <gatkvcf> <newvcf>

    ARGS:
        fil1, name and location of GATK created vcf
        fil2, name and location for new vcf
    """
    dcount = 0
    icount = 1
    with open(gatkvcf) as vcf:
        with open(newvcf, 'wb') as new:
            for line in vcf:
                if "##fileformat=VCFv4.1" in line:
                    new.write(line)
                if not line.startswith("##"):
                    rec = VCF(line)
                    if len(rec.ref) != 1 and dcount < 101:
                        new.write(line)
                        dcount += 1
                    elif len(rec.alt) != 1 and icount < 101:
                        new.write(line)
                        icount += 1

if __name__=='__main__':
    if len(argv) != 3:
        print main.__doc__
        exit()
    gatkvcf = argv[1]
    newvcf = argv[2]
    main()
