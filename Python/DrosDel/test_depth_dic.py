from sys import argv
import pprint

class subd():
    def __init__(self):
        self.st = 0
        self.en = 0
        self.depths = []
        self.hets = []

def main():
    depth_dic = {}
    with open(table) as t:
        for line in t:
            z = int(line.rstrip().split('\t')[1])
            chrom = line.split('\t')[0]
            s = int(win)
            breaks = range(1, z, s)
            supd = {}
            i = 0
            while i < len(breaks) - 1:
                c = subd()
                c.st, c.en =breaks[i], breaks[i] + s - 1
                supd[i] = c
                depth_dic[chrom] = supd
                i += 1
            c = subd()
            c.st, c.en = breaks[i], z
            supd[i] = c
            depth_dic[chrom] = supd
    for k in depth_dic.keys():
        for l in depth_dic[k]:
            q = depth_dic[k][l]
            print k, l, q.st, q.en, q.depths, q.hets


if __name__ == '__main__':
    if len(argv) != 3:
        print main.__doc__
        exit()
    table = argv[1]
    win = argv[2]
    main()
