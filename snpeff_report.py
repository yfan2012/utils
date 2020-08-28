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
        if i[0]=='#':
            continue
        ref=info[3]
        gt=info[9].split(':')
        alt=info[4].split(',')
        ao=gt[5].split(',')
        altinfo=list(zip(alt, ao))
        ##sometimes snpeff leaves out bases
        ro=gt[3]
        snpeffann=info[7].split(';')[41].split(',')
        snpeffann[0]=snpeffann[0][4:]
        for var in snpeffann:
            annot=var.split('|')
            for alt in altinfo:
                if annot[0] in alt[0]:
                    annotnum=alt[1]
                    snpinfo.append([info[0], info[1], ref, annot[0], ro, annotnum, annot[1], annot[2], annot[3], annot[5], annot[10], annot[15]])
    return(snpinfo)


def main(snpsfile, outfile):
    snpinfo=assign_snps(snpsfile)
    with open(outfile, 'w') as f:
        f.write('chrm,pos,ref,alt,ro,ao,annotation,impact,genename,feature_type,prot_change,info')
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
