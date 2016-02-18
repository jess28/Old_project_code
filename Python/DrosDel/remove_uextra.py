from sys import argv

def main():
    Uextra = False
    with open(fasta_file) as fasta:
        with open(new_file, 'wb') as new:
            for line in fasta:
                if line.startswith('>'):
                    if not line.startswith('>Uextra'):
                        Uextra = False
                        new.write(bytes(line, 'UTF-8'))
                    else:
                        Uextra = True
                elif not line.startswith('>') and Uextra == False:
                    new.write(bytes(line,'UTF-8'))

if __name__ == '__main__':
    fasta_file = argv[1]
    new_file = argv[2]
    main()
