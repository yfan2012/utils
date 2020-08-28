import argparse
'''
take a vcf and find where the two non-ref seqs are different
take an annotation of the ref genome and find what genes are mutated
'''

def assign_snps(snpsfile):
    '''
    input snp bedfile made from intersecting vcf and gff
    return list of lists [chr, pos, refbase, altbase, refobs, altobvs, feature, prodinfo, geneinfo, noteinfo]
    '''
    with open(snpsfile) as f:
        content=f.read().split('\n')
        f.close()
    snpinfo=[]
    for i in content:
        info=i.split('\t')
        if len(i)==0:
            continue
        ref=info[3]
        alt=info[4].split(',')
        gt=info[9].split(':')
        ao=gt[5].split(',')
        ro=gt[3]
        altinfo=list(zip(alt, ao))
        tags=info[18].split(';')
        prodinfo=[x for x in tags if 'product=' in x]
        if len(prodinfo)==0:
            prodinfo=['no product info']
        geneinfo=[x for x in tags if 'gene=' in x]
        if len(geneinfo)==0:
            geneinfo=['no gene info']
        noteinfo=[x for x in tags if 'Note=' in x]
        if len(noteinfo)==0:
            noteinfo=['no note info']
        for i in altinfo:
            snpinfo.append([info[0], info[1], ref, i[0], ro, i[1], info[12], info[13], info[14], ' '.join(prodinfo), ' '.join(geneinfo), ' '.join(noteinfo)])
    return(snpinfo)


def main(snpsfile, outfile):
    snpinfo=assign_snps(snpsfile)
    with open(outfile, 'w') as f:
        for i in snpinfo:
            f.write(','.join(i)+'\n')
        f.close()

    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='find reads that aligned exactly one time')
    parser.add_argument('--vcf','-v',  help='vcf bedfile - made from `bedtools intersect -wa -wb <vcf> <gff3>`', type=str, required=True)
    parser.add_argument('--out','-o',  help='final csv file', type=str, required=True)
    args = parser.parse_args()

    main(args.vcf, args.out)
