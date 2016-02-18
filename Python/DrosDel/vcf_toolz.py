class VCF():
    "splits vcf file into columns, may need to split farther in function"
    def __init__(self, line):
        self.line = line
        self.data = line.rstrip().split("\t")
        self.chrom = self.data[0]
        self.pos = self.data[1]
        self.ID = self.data[2]
        self.ref = self.data[3]
        self.alt = self.data[4]
        self.qual = self.data[5]
        self.filt = self.data[6]
        self.info = self.data[7]
        # self.info = self.mk_dict()
        self.form = self.data[8]
        self.s302 = self.data[9]

    # def mk_dict(self):
    #     dic = {}
    #     lis_info = self.data[7].split(';')
    #     for x in lis_info:
    #         key_val = x.split('=')
    #         if len(key_val) > 1:
    #             dic[key_val[0]] = key_val[1]
    #     return dic
