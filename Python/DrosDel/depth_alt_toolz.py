class table():
    "splits table made from alt_table_gatk into separate columns."
    def __init__(self, line):
        self.line = line
        self.data = line.rstrip().split('\t')
        self.chrom = self.data[0]
        self.pos = int(self.data[1])
        self.depth = int(self.data[2])
        self.alt = int(self.data[3])
        ##
