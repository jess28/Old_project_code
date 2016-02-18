class GFF():
    "Splits gff file on tabs to use columns separately"
    def __init__(self, line):
        self.line = line
        self.data = line.rstrip().split('\t')
        self.chrom = self.data[0]
        self.source = self.data[1]
        self.typ = self.data[2]
        self.start = int(self.data[3])
        self.end = int(self.data[4])
        self.score = self.data[5]
        self.strand = self.data[6]
        self.phase = self.data[7]
        self.atr = self.data[8]
