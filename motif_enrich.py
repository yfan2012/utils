def pafseqs(pafreport):
    '''get the ref sequences out of a pafreport'''
    seqs=[]
    with open(pafreport, 'r') as f:
        for line in f:
            if line[0] != '>':
                seqs.append(line.split('\t')[6])
    return seqs


def mumseqs(snps, ref):
    import sys
    sys.path.insert(0, '/home-4/yfan7@jhu.edu/Code/utils')
    from fasta_utils import fasta_dict
    refseqs=fasta_dict(ref)
    with open(snps, 'r') as f:
        content=f.read().splitlines()
    seqs=[]
    for i in content:
        pos=int(i.split('\t')[0])
        chrom=i.split('\t')[10]
        seqs.append(refseqs['>'+chrom][pos-3:pos+3])
    return seqs


def freqmotif (seqs, mersize):
    '''count number of occurences of each kmer'''
    import itertools
    ##get all possible motifs of length mersize
    motifs=[''.join(x) for x in list(itertools.product(['A', 'T', 'C', 'G'], repeat=mersize))]
    ##initialize dictionary from motifs to add to later
    freqs=dict.fromkeys(motifs, 0)
    for i in seqs:
        length=len(i)
        for j in range(mersize, length+1):
            if i[j-mersize:j] in freqs:
                freqs[i[j-mersize:j]]+=1
            else:
                freqs[i[j-mersize:j]]=1
    return freqs




def main(pafreport, snps, ref, mersize, outfile):
    import sys
    
    if snps is None:
        seqs=pafseqs(pafreport)
    elif pafreport is None:
        seqs=mumseqs(snps, ref)
    else:
        print 'Need some kind of input'
        sys.exit
        
    freqs=freqmotif(seqs, mersize)
    listfreqs=[[x, str(freqs[x])] for x in freqs]

    with open(outfile, 'w') as f:
        for x in listfreqs:
            f.write(','.join(x)+'\n')



        
if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description = 'Figure out some stuff about barcodes of the run')
    parser.add_argument('--inpaf', '-i', type=str,  help='input pafreport path')
    parser.add_argument('--snps', '-s', type=str,  help='input mummer snps file path')
    parser.add_argument('--ref', '-r', type=str, help='path the reference used to make the mummer snp file')
    parser.add_argument('--mersize', '-m', type=int, required=True, help='mersize to look at')
    parser.add_argument('--outfile', '-o', type=str, required=True,  help='output path')
    args=parser.parse_args()
    main(args.inpaf, args.snps, args.ref, args.mersize, args.outfile)

