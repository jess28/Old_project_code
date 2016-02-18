from multiprocessing import Pool
import sys

def main():
    """
    Find GC and N percent content of fasta scaffold

    USAGE:
        python gc_content.py <fastafil>
    
    ARGS:
        fil1, fasta file to count
    """ 
    table = fastafil.split('.')[0].split('_')[0] + '_ref_gc.tab'
    seqs = []
    chrom = ""
    win = ""
    with open(table, 'wb') as new:
        to_write = '\t'.join(["chrom", "win", "gc_per", "n_per"])
        new.write(to_write + '\n')
        with open(fastafil) as fasta:
            for line in fasta:
                if line.startswith(">") and seqs == []:
                    scaff = line.rstrip().split(":")
                    chrom = scaff[0][1:]
                    win = scaff[1]
                if line.startswith(">") and seqs != []:
                    seq = "".join(seqs)
                    gc_per = gc_cont(str(seq))
                    n_per = n_count(str(seq))
                    to_write = '\t'.join([str(chrom), str(win), str(gc_per), str(n_per)])
                    new.write(to_write + '\n')
                    scaff = line.rstrip().split(":")
                    chrom = scaff[0][1:]
                    win = scaff[1]
                else:
                    seqs.append(line.rstrip())

def gc_cont(s):
    G = s.count("G")
    C = s.count("C")
    g = s.count("g")
    c = s.count("c")
    tot = len(s)
    gccount = G + C + g + c
    gc_per = gccount/float(tot)
    return gc_per

def n_count(s):
    N = s.count("N")
    tot = len(s)
    n_per = N/float(tot)
    return n_per

if __name__ == '__main__':
    if len(argv) != 2:
        print main.__doc__
        exit()
    fastafil = argv[1]
    pool = Pool(processes = 4)
    main()