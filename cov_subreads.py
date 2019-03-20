'''subsample reads to evenly cover the genome'''

def readranges(bamfilename, chrname):
    '''read a bamfile and return list of reads that will cover  each base of a tig at least cov number of times'''
    import pysam
    bamfile=pysam.AlignmentFile(bamfilename, 'r')

    readinfo=[]
    for read in bamfile:
        if read.reference_name == chrname:
            readinfo.append([read.reference_start, read.reference_end, read.query_name])
    ##readinfo will be sorted by ref
    
    ##check last position of alignment
    

def subyield(fqfile, basesyield, subfile):
    '''read a fastq and write a subsampled file of a certain yield'''
    with open(fqfile, 'r') as f:
        content=[x.strip() for x in f.readlines()]
        names=content[0::4]
        seq=content[1::4]
        qual=content[3::4]
    f.close()
    total=0
    read=0
    with open(subfile, 'w') as f:
        while total < basesyield:
            if read < len(names):
                f.write(names[read]+'\n')
                f.write(seq[read]+'\n')
                f.write('+' + '\n')
                f.write(qual[read]+'\n')
                read+=1
                total+=len(seq[read])
            else:
                total=basesyield+1
    f.close()
    

def main(fqfile, basesyield, subfile):
    if basesyield is not None:
        subset=subyield(args.fq, args.bases, args.outfile)
        
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='subset fastq to a certain yield')
    parser.add_argument('--fq','-f',  help='input fastq path', type=str, required=True)
    parser.add_argument('--bases','-y',  help='desired yield in bp', type=int)
    parser.add_argument('--outfile','-o',  help='output fastq file', type=str, required=True)
    args=parser.parse_args()

    main(args.fq, args.bases, args.outfile)
    



    
