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
    


        



    
