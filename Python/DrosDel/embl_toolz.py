# Parses embl file from flybase.org, must contain 'SO_feature' in FT section.
# Copyright (C) 2014 Jessica Strein jessica.strein@uconn.edu
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as publinehed by
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

from sys import exit

class EMBL():
    def __init__(self, record):
        """
        For use with embl2fastagff.py, embl2sql.py or other script created by user.
        record should be a list containing all the information from each line
        of an EMBL record (from ID to //).  This is for use with EMBL files that
        contain 'SO_feature' in the FT section where the feature name should be.
        This type of file is not parsable with BioPython, so this code was created 
        to deal with it.  This class will return an object containing all the
        information in one record.  An iterator needs to be created to get more
        than one record's information.
        """
        self.record = record
        self.ID = ""
        self.length = ""
        self.accession = []
        self.derived = []
        self.synonym = []
        self.source = ""
        self.CDS = {}
        self.RR_tract = {}
        self.TATA_box = {}
        self.dinucleotide_repeat_microsatellite_feature = {}
        self.direct_repeat = {}
        self.five_prime_LTR = {}
        self.five_prime_UTR = {}
        self.intron = {}
        self.inverted_repeat = {}
        self.long_terminal_repeat = {}
        self.non_LTR_retrotransposon = {}
        self.non_LTR_retrotransposon_polymeric_tract = {}
        self.polyA_sequence = {}
        self.polyA_signal_sequence = {}
        self.polyA_site = {}
        self.primer_binding_site = {}
        self.pseudogene = {}
        self.region = {}
        self.start_codon = {}
        self.terminal_inverted_repeat = {}
        self.tetranucleotide_repeat_microsatellite_feature = {}
        self.three_prime_LTR = {}
        self.three_prime_UTR = {}
        self.transcription_start_site = {}
        self.comments = []
        self.seqinfo = []
        self.sequence = ""
        self.parse_all()

    def parse_all(self):
        "Splits up the record into its parts and sends them to the appropriate method."
        ID_line = ""
        AC = []
        DR_line = ""
        SY = []
        features = []
        CC = []
        SQ_line = ""
        seq = []
        for i in self.record:
            head = i[:2]
            if head == 'ID':
                ID_line = i[5:]
            elif head == 'AC':
                AC.append(i)
            elif head == 'DR':
                DR_line = i
            elif head == 'SY':
                SY.append(i) 
            elif head == 'FT':
                features.append(i)  
            elif head == 'CC':
                CC.append(i)
            elif head == 'SQ':
                SQ_line = i
            elif head == '  ':
                seq.append(i)
            elif head == '//':
                pass
            elif head == 'XX':
                pass
            else:
                print("%s does not belong" % head)
                exit()
        if ID_line != "":
            self.ID_parse(ID_line)
        if AC != []:
            self.AC_parse(AC)
        if DR_line != "":
            self.DR_parse(DR_line)
        if SY != []:
            self.SY_parse(SY)
        if features != []:
            self.FT_parse(features)
        if CC != []:
            self.CC_parse(CC)
        if SQ_line != "":
            self.SQ_parse(SQ_line)
        if seq != []:
            self.seq_parse(seq)

    def ID_parse(self, ID_line):
        "Splits the ID line into an ID and the length of the sequence."
        self.ID = ID_line.rstrip().split(' ')[0]        
        self.length = ID_line.rstrip().split('; ')[-1][:-1] 
        return self.ID, self.length

    def AC_parse(self, AC):
        "Creates a list of given accession IDs."
        for a in AC:
            nohead = a[5:].rstrip().split(';')
            for i in nohead:
                self.accession.append(i)
        return self.accession

    def DR_parse(self, DR_line):
        "Makes a list of the derived information."
        self.derived = DR_line[5:].rstrip().split('; ')
        return self.derived

    def SY_parse(self, SY):
        "Makes a list of the given synonyms."
        for i in SY:
            syn = i.rstrip().split(': ')[-1]
            self.synonym.append(syn)
        return self.synonym

    def FT_parse(self, features):
        """
        Finds source, if given, as well as splits the features into individual
        lists with information about the features and sends the information
        to the SO_parse method for furthur processing.
        """
        SO_index = []
        for i in range(len(features)):
            if 'source' in features[i]:
                self.source = features[i][21:].rstrip().split(':')
            elif 'SO_feature' in features[i]:
                SO_index.append(i)
        feat = [features[j:SO_index[SO_index.index(j)+1]] for j in SO_index[:-1]]
        if feat != []:
            f_last = features[SO_index[-1]:]
            feat.append(f_last)
            for lis in feat:
                self.SO_parse(lis)
        return self.source

    def CC_parse(self, CC):
        "Creates list of any comments in record."
        for c in CC:
            self.comments.append(c[5:].rstrip())
        return self.comments

    def SQ_parse(self, SQ_line):
        "Splits up the information about the sequence (base content and length)."
        self.seqinfo = SQ_line[14:].rstrip().split('; ')
        return self.seqinfo

    def seq_parse(self, seq):
        "Concatenates the sequence into one string for simpler use."
        s_part = []
        for s in seq:
            s_lis = s.rstrip().split(' ')
            s_part.append(''.join(s_lis[:-1]))
        self.sequence = ''.join(s_part)
        return self.sequence

    def SO_parse(self, lis):
        """
        Adds all information about a feature to the appropriate feature variable.
        Find the location and uses this as a key to the feature dictionary, with 
        more information in a nested dictionary containing all the other information
        such as translation of protein or protein id.
        """
        loc = 'YES'
        desc = {}
        previous_lin = ''
        for lin in lis:
            if 'SO:' in lin:
                if '..' in lin:
                    loc = lin.rstrip().split(':')[-1]
                previous_lin = lin
            elif 'SO:' not in lin:
                if '..' in lin and 'SO:' in previous_lin and '..' in previous_lin:
                    loc = loc + lin.rstrip()[21:]
                elif '..' in lin and 'SO:' in previous_lin and '..' not in previous_lin:
                    loc = lin.rstrip()[21:]
                elif '..' in lin and '..' not in previous_lin:
                    loc = lin.rstrip().split(':')[-1]
                elif 'translation' not in lin and '/' in lin:
                    d = lin.rstrip().split('=')
                    if d[0][22:] not in desc.keys():
                        desc[d[0][22:]] = []
                    desc[d[0][22:]].append(d[1].replace('"', ''))
                elif 'translation' in lin:
                    whole_t = []
                    trans = lis[lis.index(lin):]
                    for t in trans:
                        whole_t.append(t[22:].rstrip())
                    w_trans = ''.join(whole_t)
                    d = w_trans.split('=')
                    if 'translation' not in desc.keys():
                        desc['translation'] = []
                    desc['translation'].append(d[1].replace('"', ''))
        if 'CDS' in lis[0]:
            self.CDS[loc] = desc
            return self.CDS
        elif 'RR_tract' in lis[0]:
            self.RR_tract[loc] = desc
            return self.RR_tract
        elif 'TATA_box' in lis[0]:
            self.TATA_box[loc] = desc
            return self.TATA_box
        elif 'dinucleotide_repeat_microsatellite_feature' in lis[0]:
            self.dinucleotide_repeat_microsatellite_feature[loc] = desc
            return self.dinucleotide_repeat_microsatellite_feature
        elif 'direct_repeat' in lis[0]:
            self.direct_repeat[loc] = desc
            return self.direct_repeat
        elif 'five_prime_LTR' in lis[0]:
            self.five_prime_LTR[loc] = desc
            return self.five_prime_LTR
        elif 'five_prime_UTR' in lis[0]:
            self.five_prime_UTR[loc] = desc
            return self.five_prime_UTR
        elif 'intron' in lis[0]:
            self.intron[loc] = desc
            return self.intron
        elif 'inverted_repeat' in lis[0]:
            self.inverted_repeat[loc] = desc
            return self.inverted_repeat
        elif 'long_terminal_repeat' in lis[0]:
            self.long_terminal_repeat[loc] = desc
            return self.long_terminal_repeat
        elif 'non_LTR_retrotransposon' in lis[0]:
            self.non_LTR_retrotransposon[loc] = desc
            return self.non_LTR_retrotransposon
        elif 'non_LTR_retrotransposon_polymeric_tract' in lis[0]:
            self.non_LTR_retrotransposon_polymeric_tract[loc] = desc
            return self.non_LTR_retrotransposon_polymeric_tract
        elif 'polyA_sequence' in lis[0]:
            self.polyA_sequence[loc] = desc
            return self.polyA_sequence
        elif 'polyA_signal_sequence' in lis[0]:
            self.polyA_signal_sequence[loc] = desc
            return self.polyA_signal_sequence
        elif 'polyA_site' in lis[0]:
            self.polyA_site[loc] = desc
            return self.polyA_site
        elif 'primer_binding_site' in lis[0]:
            self.primer_binding_site[loc] = desc
            return self.primer_binding_site
        elif 'pseudogene' in lis[0]:
            self.pseudogene[loc] = desc
            return self.pseudogene
        elif 'region' in lis[0]:
            self.region[loc] = desc
            return self.region
        elif 'start_codon' in lis[0]:
            self.start_codon[loc] = desc
            return self.start_codon
        elif 'terminal_inverted_repeat' in lis[0]:
            self.terminal_inverted_repeat[loc] = desc
            return self.terminal_inverted_repeat
        elif 'tetranucleotide_repeat_microsatellite_feature' in lis[0]:
            self.tetranucleotide_repeat_microsatellite_feature[loc] = desc
            return self.tetranucleotide_repeat_microsatellite_feature
        elif 'three_prime_LTR' in lis[0]:
            self.three_prime_LTR[loc] = desc
            return self.three_prime_LTR
        elif 'three_prime_UTR' in lis[0]:
            self.three_prime_UTR[loc] = desc
            return self.three_prime_UTR
        elif 'transcription_start_site' in lis[0]:
            self.transcription_start_site[loc] = desc
            return self.transcription_start_site
