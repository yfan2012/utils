def makecons(vcfgz, ref, outfa):
    '''get consensus from zipped and indexed bcf, ref fasta to new cons fasta'''
    import pyfaidx

    consensus=pyfaidx.FastaVariant(ref, vcfgz, het=False, hom=True)
    out=open(outfa, 'w')

    for chrom in consensus.keys():
        for var in consensus[chrom].variant_sites:
            record = consensus[chrom][var-1:var]
            out.write(record)
    out.close()

def main(vcfgz, ref, outfa):
    makecons(vcfgz, ref, outfa)

if __name__ =='__main__':
    import argparse
    parser = argparse.ArgumentParser(description='take bgzipped/tabix vcf and ref fa into cons fa')
    parser.add_argument('--vcf', '-v', help='vcf bgzipped and tabixed', type=str)
    parser.add_argument('--ref', '-r', help='reference used to make vcf', type=str)
    parser.add_argument('--out', '-o', help='output cons fa path', type=str)
    args = parser.parse_args()
    main(args.vcf, args.ref, args.out)
