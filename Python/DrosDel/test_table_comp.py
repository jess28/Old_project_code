from sys import argv
import math

def main():
    """
    Creates test table for dic

    USAGE:
        python test_table_comp.py <reffile> <tablefile> <win>
    """
    with open(reffile) as ref:
        with open(tablefile, 'wb') as table:
            for line in ref:
                s = line.rstrip().split('\t')
                chrom = s[0]
                pos = int(s[1])
                win_num = pos // win + 1  
                count = 0
                base = 1 
                while count < win_num:
                    to_write = '\t'.join([chrom, str(base), '50', '0'])
                    table.write(to_write + '\n')
                    base += win
                    count += 1

if __name__ == '__main__':
    if len(argv) != 4:
        print main.__doc__
        exit()
    reffile = argv[1]
    tablefile = argv[2]
    win = int(argv[3])
    main()