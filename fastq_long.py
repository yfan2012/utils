def rm_short(fqfile, outfile, least):
    from itertools import islice
    with open(fqfile) as f:
        with open(outfile, 'w') as g:
            while True:
                next_read=list(islice(f, 4))
                if not next_read:
                    break
                if len(next_read[1]) > least:
                    for i in next_read:
                        g.write(i)
        g.close()
    f.close()


def rm_short_fa(fqfile, outfile, least):
    import sys
    sys.path.insert(0, '/home/yfan/Code/utils')
    from fasta_utils import fasta_dict
    fa=fasta_dict(fqfile)
    with open(outfile, 'w') as f:
        for i in fa:
            if len(fa[i]) > least:
                f.write(i+'\n')
                f.write(fa[i]+'\n')
                

    
def main(fqfile, outfile, least):
    if fqfile.endswith(('.fa', '.fasta')):
        rm_short_fa(fqfile, outfile, least)
    else:
        rm_short(fqfile, outfile, least)

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='delete reads shorter than a certain length in fq')
    parser.add_argument('--fqfile','-i',  help='input fastq path', type=str, required=True)
    parser.add_argument('--outfile','-o',  help='output fastq path', type=str, required=True)
    parser.add_argument('--length', '-l', help='shortest length', type=int, required=True)
    args = parser.parse_args()
    
    main(args.fqfile, args.outfile, args.length)


                    
