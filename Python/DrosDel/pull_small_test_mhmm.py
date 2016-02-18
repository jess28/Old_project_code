from sys import argv

def main():
    w = False
    with open(pos_file) as pos:
        with open(new_file, 'wb') as new:
            new.write(bytes('Position\tcont_dp\tsamp_dp\n', 'UTF-8'))
            for line in pos:
                if not line.startswith('Position'):
                    if w == False:
                        if int(line.split('\t')[0]) >= 3060:
                            w = True
                    else:
                        if int(line.split('\t')[0]) >= 13060:
                            w = False
                        else:
                            new.write(bytes(line, 'UTF-8'))

if __name__ == '__main__':
    pos_file = argv[1]
    new_file = argv[2]
    main()