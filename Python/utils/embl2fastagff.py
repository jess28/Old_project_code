# Changes an EMBL file to a GFF and a FASTA
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

from embl_toolz import EMBL
from sys import argv

def main():
    """
    Creates a GFF and a fasta file from an EMBL file with SO_feature where the
    name of the feature should be. (This improperly formatted file was downloaded
    from Flybase.org

    USAGE:
        python3 embl2fastagff.py <embl_file> <fasta_file> <GFF_file>

    ARGS:
        embl_file: path to the embl file to be parsed
        fasta_file: path to new fasta file
        GFF_file: path to new GFF file

    NOTES:
        This script uses any version of Python 3.
    """
    records = make_rec()
    to_fasta(records)
    to_GFF(records)

def make_rec():
    """
    Creates list of lists where each inner list contains all the lines of an
    EMBL record. The main list will contain each EMBL record in its own list.
    """
    print('Creating record list')
    first = True
    records = []
    record = []
    with open(embl_file) as embl:
        for line in embl:
            head = line[:2]
            if head == 'ID' and first == True:
                record.append(line)
                first = False
            elif head == 'ID' and first == False:
                records.append(record)
                record = []
                record.append(line)
            elif first == False:
                record.append(line)
    print('Record list created')
    return records

def to_fasta(records):
    "Uses the sequence and the sequence information from embl_toolz to make a fasta file."
    print('Creating fasta file')
    with open(fasta_file, 'wb') as fasta:
        for r in records:
            count = 0
            rec = EMBL(r)
            part_head = '; '.join(rec.seqinfo)
            header = '>' + rec.ID + '; ' + part_head + '\n'
            fasta.write(bytes(header, 'UTF-8'))
            seq = ''
            for l in rec.sequence:
                count += 1
                if count%80 == 0:
                    seq = seq + l
                    fasta.write(bytes((seq + '\n'), 'UTF-8'))
                    seq = ''
                else:
                    seq = seq + l
            if seq != '':
                fasta.write(bytes((seq + '\n'), 'UTF-8'))
    print('Fasta file created')

def to_GFF(records):
    "Uses the information from embl_toolz to make a GFF file."
    print('Creating GFF file')
    with open(GFF_file, 'wb') as GFF:
        GFF.write(bytes(('##gff-version 3' + '\n'), 'UTF-8'))
        GFF.write(bytes(('#Because of inconsistant start positions, all phase columns have been set to 0.' + '\n'), 'UTF-8'))
        GFF.write(bytes(('#If the start and end positions are both 1, they have been set that way for validity, they are not known.' + '\n'), 'UTF-8'))
        for r in records:
            rec = EMBL(r)
            loc = rec.length.split(' BP')[0]
            start = '1'
            end = loc.replace(' ', '')
            Attribute = 'ID=' + rec.ID + ';' + 'Name=' + rec.ID
            trans_write = '\t'.join([rec.ID, rec.derived[0], 'gene', start, end, '.', '.', '0', Attribute])
            GFF.write(bytes((trans_write + '\n'), 'UTF-8'))
            variables = [[rec.five_prime_UTR, 'five_prime_UTR'],
                         [rec.start_codon, 'start_codon'],
                         [rec.CDS, 'CDS'],
                         [rec.three_prime_UTR, 'three_prime_UTR'],
                         [rec.RR_tract, 'RR_tract'],
                         [rec.TATA_box, 'TATA_box'],
                         [rec.dinucleotide_repeat_microsatellite_feature, 'dinucleotide_repeat_microsatellite_feature'],
                         [rec.direct_repeat, 'direct_repeat'],
                         [rec.five_prime_LTR, 'five_prime_LTR'],
                         [rec.intron, 'intron'],
                         [rec.inverted_repeat, 'inverted_repeat'],
                         [rec.long_terminal_repeat, 'long_terminal_repeat'],
                         [rec.non_LTR_retrotransposon, 'non_LTR_retrotransposon'],
                         [rec.non_LTR_retrotransposon_polymeric_tract, 'non_LTR_retrotransposon_polymeric_tract'],
                         [rec.polyA_sequence, 'polyA_sequence'],
                         [rec.polyA_signal_sequence, 'polyA_signal_sequence'],
                         [rec.polyA_site, 'polyA_site'],
                         [rec.primer_binding_site, 'primer_binding_site'],
                         [rec.pseudogene, 'pseudogene'],
                         [rec.region, 'region'],
                         [rec.terminal_inverted_repeat, 'terminal_inverted_repeat'],
                         [rec.tetranucleotide_repeat_microsatellite_feature, 'tetranucleotide_repeat_microsatellite_feature'],
                         [rec.three_prime_LTR, 'three_prime_LTR'],
                         [rec.transcription_start_site, 'TSS']]
            count = 0
            Par_lis = ['CDS', 'five_prime_UTR', 'three_prime_UTR', 'intron', 'start_codon']
            note = []
            for variable in variables:
                if variable[0] != {}:
                    for key in variable[0].keys():
                        count += 1
                        ID = 'ID=' + rec.ID + '.' + str(count)
                        if variable[1] in Par_lis:
                            Parent = 'Parent=' + rec.ID
                            attrs = [ID, Parent]
                        else:
                            attrs = [ID]
                        if 'NA' not in variable[0][key].keys():
                            for k in variable[0][key].keys():
                                a = []
                                for i in variable[0][key][k]:
                                    if ';' in i:
                                        i = i.replace(';', ':')
                                    if i != "":
                                        a.append(i)
                                ajoin = ','.join(a)
                                if ajoin != '':
                                    attr = k + '=' + ajoin
                                    attrs.append(attr)
                        attr_full =  ';'.join(attrs)
                        if '..' in key:
                            if ',' not in key:
                                l = key.split('..')
                                typ = variable[1]
                                if 'complement' in l[0]:
                                    tst = l[0][11:]
                                    ten = l[1][:-1]
                                    note.append('complement')
                                elif key == '..':
                                    tst = '1'
                                    ten = '1'
                                elif key == '?..?':
                                    tst = '1'
                                    ten = '1'
                                else:
                                    tst = l[0]
                                    ten = l[1]
                                if '<' in tst or '>' in tst:
                                    tst = tst.replace('>', '')
                                    tst = tst.replace('<', '')
                                    note.append("uncertain start position")
                                if '<' in ten or '>' in ten:
                                    ten = ten.replace('>', '')
                                    ten = ten.replace('<', '')
                                    note.append("uncertain end position")
                                if int(tst) > int(ten):
                                    strand = '-'
                                    st = ten
                                    en = tst
                                else:
                                    strand = '+'
                                    st = tst
                                    en = ten
                                if ' ' in st:
                                    st = st.replace(' ', '')
                                if ' ' in en:
                                    en = en.replace(' ', '')
                                if note != []:
                                    n = ','.join(note)
                                    attr_full = attr_full + ';Note=' + n
                                to_write_l = [rec.ID, rec.derived[0], typ, st, en, '.', strand, '0', attr_full]
                                to_write = '\t'.join(to_write_l)
                                GFF.write(bytes((to_write + '\n'), 'UTF-8'))
                            elif ',' in key:
                                typ = variable[1]
                                breaks = key.split(',')
                                exons = []
                                for i in breaks:
                                    if 'join' in i:
                                        exons.append(i[5:].split('..'))
                                    elif ')' in i:
                                        exons.append(i[:-1].split('..'))
                                    else:
                                        exons.append(i.split('..'))
                                tst = exons[0][0]
                                ten = exons[-1][-1]
                                if '<' in tst or '>' in tst:
                                    tst = tst.replace('>', '')
                                    tst = tst.replace('<', '')
                                    note.append("uncertain start position")
                                if '<' in ten or '>' in ten:
                                    ten = ten.replace('>', '')
                                    ten = ten.replace('<', '')
                                    note.append("uncertain end position")
                                if int(tst) > int(ten):
                                    strand = '-'
                                    st = ten
                                    en = tst
                                else:
                                    strand = '+'
                                    st = tst
                                    en = ten
                                if ' ' in st:
                                    st = st.replace(' ', '')
                                if ' ' in en:
                                    en = en.replace(' ', '')
                                if note != []:
                                    n = ','.join(note)
                                    attr_full = attr_full + ';Note=' + n
                                to_write_l = [rec.ID, rec.derived[0], typ, st, en, '.', strand, '0', attr_full]
                                to_write = '\t'.join(to_write_l)
                                to_write_exon = []
                                for x in range(len(exons), 2):
                                    p = 'Parent=' + ID
                                    tst = exons[a]
                                    ten = exons[a+1]
                                    if '<' in tst or '>' in tst:
                                        tst = tst.replace('>', '')
                                        tst = tst.replace('<', '')
                                        note.append("uncertain start position")
                                    if '<' in ten or '>' in ten:
                                        ten = ten.replace('>', '')
                                        ten = ten.replace('<', '')
                                        note.append("uncertain end position")
                                    if int(tst) > int(ten):
                                        strand = '-'
                                        st = ten
                                        en = tst
                                    else:
                                        strand = '+'
                                        st = tst
                                        en = ten
                                    if ' ' in st:
                                        st = st.replace(' ', '')
                                    if ' ' in en:
                                        en = en.replace(' ', '')
                                    if note != []:
                                        n = ','.join(note)
                                        p = p + ';Note=' + n
                                    to_write_ex = [rec.ID, rec.derived[0], 'exon', st, en, '.', strand, '0', p]
                                    to_write_e = '\t'.join(to_write_ex)
                                    to_write_exon.append(to_write_e)
                                GFF.write(bytes((to_write + '\n'), 'UTF-8'))
                                for i in to_write_exon:
                                    GFF.write(bytes((i + '\n'), 'UTF-8'))
                        else:
                            typ = variable[1]
                            to_write_l = [rec.ID, rec.derived[0], typ, '1', '1', '.', '.', '0', attr_full]
                            to_write = '\t'.join(to_write_l)
                            GFF.write(bytes((to_write + '\n'), 'UTF-8'))
    print('GFF file created')

if __name__ == '__main__':
    if len(argv) != 4:
        print(main.__doc__)
        exit()
    embl_file = argv[1]
    fasta_file = argv[2]
    GFF_file = argv[3]
    main()