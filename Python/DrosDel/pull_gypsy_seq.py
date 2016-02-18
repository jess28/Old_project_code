from sys import argv

def main():
    with open(reference) as ref:
        for line in ref:
            if line.startswith('>X'):
                count = 0
                X = True
            elif not line.startswith('>X') and X == True:
                if count == 11088517:
                    seq.append(line.rstrip())
                    count += 1
                elif count == 11095880:
                    