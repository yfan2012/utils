def pafseqs(pafreport):
    '''get the ref sequences out of a pafreport'''
    seqs=[]
    with open(pafreport, 'r') as f:
        for line in f:
            if line[0] != '>':
                seqs.append(line.split('\t')[6])
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
            freqs[i[j-mersize:j]]+=1

    return freqs




def main(pafreport, mersize, outfile):
    seqs=pafseqs(pafreport)
    freqs=freqmotif(seqs, mersize)
    listfreqs=[[x, str(freqs[x])] for x in freqs]

    with open(outfile, 'w') as f:
        for x in listfreqs:
            f.write(','.join(x)+'\n')



        
if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description = 'Figure out some stuff about barcodes of the run')
    parser.add_argument('--inpaf', '-i', type=str, required=True,  help='input pafreport path')
    parser.add_argument('--mersize', '-m', type=int, required=True, help='mersize to look at')
    parser.add_argument('--outfile', '-o', type=str, required=True,  help='output path')
    args=parser.parse_args()
    main(args.inpaf, args.mersize, args.outfile)

