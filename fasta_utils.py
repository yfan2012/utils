def fasta_dict(fastapath):
    '''fasta names are keys, sequences are values'''
    fasta={}
    with open(fastapath, 'r') as f:
        content=f.readlines()

    name=''
    seq=''
    for i in content:
        if i[0]=='>':
            if len(name)>0 and len(seq)>0:
                fasta[name]=seq
            name=i.strip('\n')
            seq=''
        else:
            seq+=i.strip('\n')
    fasta[name]=seq

    return(fasta)


def rev_comp(seq):
    key={'A': 'T', 'T':'A', 'G':'C',  'C':'G'}
    newseq=''
    for i in seq:
        newseq+=key[i]
    
    return newseq[::-1]
                            

def count_bases(fastapath):
    '''Count number of bases in a fasta'''
    with open(fastapath, 'r') as f:
        content=f.readlines()
    bases=0
    for i in content:
        if i[0]!='>':
            bases+=len(i.strip('\n'))

    return bases




def main(fastapath):
    '''get rid of all duplicate read names in a fasta file'''
    namedict=fasta_dict(fastapath)
    with open(fastapath, 'w') as f:
        for i in namedict:
            f.write(i+'\n')
            f.write(namedict[i]+'\n')


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description = 'make sure there are no duplicate read names')
    parser.add_argument('--infasta', '-i', type=str, required=True,  help='input fasta file')
    args=parser.parse_args()
    
    main(args.infasta)
