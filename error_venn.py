def tig_to_pos(mumsnps):
    '''get a dictionary of tigs that map to list of its positions of error'''
    with open(mumsnps, 'r') as f:
        content=f.read().splitlines()
    posdict={}
    for i in content:
        tig=i.split('\t')[10]
        if tig not in posdict:
            posdict[tig]=[int(i.split('\t')[0])]
        else:
            posdict[tig].append(int(i.split('\t')[0]))
    return posdict

def collapse(poslist):
    '''scan through a list of positions and delete runs of consecutive numbers. 
    It should be rare that there are more than a few in a row, so you should just scan for ranges of three when doing the venn diagram.
    Think of a more precise way to do this later'''
    diffs=[j-i for i,j in zip(poslist[:-1],poslist[1:])]
    poscon=[ i for i, x in enumerate(diffs) if x == 1][::-1]
    for i in poscon:
        del poslist[i]
    return poslist
                
                
def venn(posdict1, posdict2):
    '''given two dictionaries of tigs and positions, return a list [tig, both, r1, r2]'''
    ##scan through positions and collapse anything that's less than two bases away
    vencounts=[]
    for tig in posdict1:
        if tig in posdict2:
            collapsed1=collapse(posdict1[tig])
            collapsed2=collapse(posdict2[tig])
        both=0
        unique1=0
        for i in collapsed1:
            delt=[ abs(i - x) for x in collapsed2 ]
            if any( d < 2 for d in delt):
                both+=1
            else:
                unique1+=1
        unique2=0
        both2=0
        for i in collapsed2:
            delt=[ abs(i - x) for x in collapsed1 ]
            if any( d < 2 for d in delt):
                both2+=1
            else:
                unique2+=1
        vencounts.append([tig, str(both), str(both2), str(unique1), str(unique2)])
    return vencounts

def main(mumfile1, mumfile2, outfile):
    mum1=tig_to_pos(mumfile1)
    mum2=tig_to_pos(mumfile2)
    counts=venn(mum1, mum2)
    with open(outfile, 'w') as f:
        f.write(','.join(['tig', 'both1', 'both2', 'samp1', 'samp2'])+'\n')
        for i in counts:
            f.write(','.join(i)+'\n')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='get info about which mummer snps are common between two queries aligned to the same ref')
    parser.add_argument('--mumfile1', '-m1', help='first mummer snp file', type=str)
    parser.add_argument('--mumfile2', '-m2', help='second mummer snp file', type=str)
    parser.add_argument('--outfile', '-o', help='output csv path', type=str)
    args = parser.parse_args()
    main(args.mumfile1, args.mumfile2, args.outfile)
                        
