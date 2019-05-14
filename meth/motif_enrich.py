def pafseqs(pafreport):
    '''get the ref sequences out of a pafreport'''
    seqs=[]
    with open(pafreport, 'r') as f:
        for line in f:
            if line[0] != '>':
                seqs.append(line.split('\t')[6])
    return seqs

def groupmum(snps):
    '''get indexes of snp groups (grouped by distance between two snps)'''
    with open(snps, 'r') as f:
        content=f.read().splitlines()
    pos=[]
    for i in content:
        pos.append([i.split('\t')[10], int(i.split('\t')[0])])
    ##no need to look back because you're always looking ahead
    ranges=[]
    current=[]
    for i in range(0,len(pos)-1):
        if len(current)==0:
            current=[pos[i]]
            chrom=pos[i][0]
        if pos[i+1][1]-pos[i][1]<6 and pos[i][0]==chrom: ##if next position is within 5 bases of the current one, add to the current range
            current.append(pos[i])
        else: ##if next position is more than 5 bases from the current one, record the current range and blank the current list
            ranges.append([current[0][0], current[0][1]-2, pos[i][1]+2])
            current=[]
    return ranges
        
        
def mumseqs(ranges, ref):
    '''takes in a list of rangelists [chrom, start, stop]'''
    import sys
    sys.path.insert(0, '/home-4/yfan7@jhu.edu/Code/utils')
    from fasta_utils import fasta_dict
    refseqs=fasta_dict(ref)
    ##get rid of extras in chrom name
    for i in refseqs:
        newkey=i.split(' ')[0]
        refseqs[newkey]=refseqs.pop(i)
    seqs=[]
    for i in ranges:
        seqs.append(refseqs['>'+i[0]][i[1]:i[2]])
    return seqs


def freqmotif (seqs, mersize):
    '''count number of occurences of each kmer in the error motifs'''
    import itertools
    ##get all possible motifs of length mersize
    motifs=[''.join(x) for x in list(itertools.product(['A', 'T', 'C', 'G'], repeat=mersize))]
    ##initialize dictionary from motifs to add to later
    freqs=dict.fromkeys(motifs, 0)
    ##scan through the motifs and count occurence of each
    for i in seqs:
        length=len(i)
        for j in range(mersize, length+1):
            freqs[i[j-mersize:j]]+=1
    return freqs


def reffreqmotif (ref, mersize):
    '''count number of occurences of each kmer in a reference genome'''
    ##take lots of this from freqmotif function
    import itertools
    import sys
    sys.path.insert(0, '/home-4/yfan7@jhu.edu/Code/utils')
    from fasta_utils import fasta_dict
    motifs=[''.join(x) for x in list(itertools.product(['A', 'T', 'C', 'G'], repeat=mersize))]
    reffreqs=dict.fromkeys(motifs, 0)
    refseqs=fasta_dict(ref)
    for i in refseqs:
        length=len(refseqs[i])
        for j in range(mersize, length+1):
            reffreqs[refseqs[i][j-mersize:j]]+=1
    return reffreqs
    

def main(pafreport, snps, ref, mersize, outfile):
    import sys
    if snps is None:
        seqs=pafseqs(pafreport)
    elif pafreport is None:
        ranges=groupmum(snps)
        seqs=mumseqs(ranges, ref)
    else:
        print 'Need some kind of input'
        sys.exit
    freqs=freqmotif(seqs, mersize)
    reffreqs=reffreqmotif(ref, mersize)
    listfreqs=[[x, str(freqs[x]), str(reffreqs[x]), str(float(freqs[x])/float(reffreqs[x]))] for x in freqs]
    with open(outfile, 'w') as f:
        for x in listfreqs:
            f.write(','.join(x)+'\n')
    with open(outfile+'.ranges', 'w') as f:
        for i in ranges:
            f.write(','.join(x)+'\n')


        
if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description = 'find percent of k-mers in involved in errors')
    parser.add_argument('--inpaf', '-i', type=str,  help='input pafreport path')
    parser.add_argument('--snps', '-s', type=str,  help='input mummer snps file path')
    parser.add_argument('--ref', '-r', type=str, help='path the reference used to make the mummer snp file')
    parser.add_argument('--mersize', '-m', type=int, required=True, help='mersize to look at')
    parser.add_argument('--outfile', '-o', type=str, required=True,  help='output path')
    args=parser.parse_args()
    main(args.inpaf, args.snps, args.ref, args.mersize, args.outfile)

