def n50(asmpath):
    import sys
    sys.path.insert(0, '/home-4/yfan7@jhu.edu/Code/utils')
    from fasta_utils import fasta_dict

    asm=fasta_dict(asmpath)
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

    return [len(lens), lens[nfifty-1], lens[0], lens[-1]]


def main(asmpath):
    print ','.join(map(str,n50(asmpath)))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='summarize abricate results, including only the gene name, %ident, %cov, and possible function')
    parser.add_argument('--input','-i',  help='input assembly', type=str)
    args = parser.parse_args()
    main(args.input)

