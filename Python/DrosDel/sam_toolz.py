class SAMSplit():
    "Splits sam file on tabs to use each column separately"
    def __init__(self, line):
        self.line = line
        self.data = line.rstrip().split('\t')
        #print "number 1"
        self.seqID = self.data[0]
        #print "number 2"
        self.bitflag = self.data[1]
        #print "number 3"
        self.refseq = self.data[2]
        #print "number 4"
        self.pos = self.data[3]
        #print "number 5"
        self.MAPQ = int(self.data[4])
        #print "number 6"
        self.CIGAR = self.data[5]
        #print "number 7"
        self.nextseq = self.data[6]
        #print "number 8"
        self.nextpos = self.data[7]
        #print "number 9"
        self.templen = self.data[8]
        #print "number 10"
        self.seq = self.data[9]
        #print "number 11"
        self.qualstr = self.data[10]
        #print "number 12"
        self.options = self.data[11:]
        #print "done"
