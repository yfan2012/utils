import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description='get num_contigs, n50, longest, shortest, total lengths')
    parser.add_argument('--input','-i',  help='input assembly path', required=True, type=str)
    parser.add_argument('--prefix','-p',  help='assembly label', type=str)
    args = parser.parse_args()
    return args
    
def n50(asmpath):
    import sys
    import pysam

    fa=pysam.FastaFile(asmpath)
    tigs=fa.references
    asm={ x:fa.fetch(x) for x in tigs }

    lens=[]
    for i in asm:
        lens.append(len(asm[i]))
    target=sum(lens)/2
    lens.sort(reverse=True)

    nfifty=0
    bases=0
    for i in lens:
        nfifty+=1
        bases+=i
        if bases>target:
            break

    return [len(lens), lens[nfifty-1], lens[0], lens[-1], sum(lens)]


def main():
    args=parseArgs()
    asmstats=n50(args.input)
    if args.prefix :
        asmstats.insert(0, args.prefix)
    print(','.join(map(str, asmstats)))
    
if __name__ == '__main__':
    main()

