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
    '''Scan through list of positions and return list of ranges'''
    ##add pseudo location to the end so the while loop works easily
    ##if poslist[-1]-poslist[-2] == 1:
    poslist.append(999999999999999)
    diffs=[j-i for i,j in zip(poslist[:-1],poslist[1:])]
    ranges=[]
    i=0
    start=poslist[0]
    while i < len(diffs):
        if diffs[i] > 3:
            end=poslist[i]
            ranges.append([start-3, end+3])
            start=poslist[i+1]
            i+=1
        else:
            i+=1
    return ranges


def venn(posdict1, posdict2):
    '''given two dictionaries of tigs and positions, return a list [tig, both, r1, r2]'''
    ##scan through positions and collapse anything that's less than two bases away
    vencounts=[]
    for tig in posdict1:
        if tig in posdict2:
            collapsed1=collapse(posdict1[tig])
            collapsed2=collapse(posdict2[tig])
        bothlist=[]    
        both=0
        unique1=0
        for i in collapsed1:
            overlap=[ i[0] <= j[1] and i[1] >= j[0] for j in collapsed2 ]
            if sum(overlap)>=1:
                both+=1
            else:
                unique1+=1
        unique2=0
        both2=0
        for i in collapsed2:
            overlap=[ i[0] <= j[1] and i[1] >= j[0] for j in collapsed1 ]
            if sum(overlap)>=1:
                both2+=1
            else:
                unique2+=1
        ##if two distinct regions in one map to the same region in the other, the intersection of the venn diagram can e different
        ##force them to be the smaller - this essentially combines the two distinct regions
        if both > both2:
            both=both2
        else:
            both2=both
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
    parser = argparse.ArgumentParser(description='take mummer snp file and make csv that lists number of snps that are common, unique to samp1, and unique to samp2 for each tig')
    parser.add_argument('--mumfile1', '-m1', help='first mummer snp file', type=str)
    parser.add_argument('--mumfile2', '-m2', help='second mummer snp file', type=str)
    parser.add_argument('--outfile', '-o', help='output csv path', type=str)
    args = parser.parse_args()
    main(args.mumfile1, args.mumfile2, args.outfile)
                        
