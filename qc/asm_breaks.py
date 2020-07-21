import pysam
'''
Take in mummer mcoords file as a list of possible places to break contigs
Take in nanopore read alignment bam as evidence
Take in illumina read alignment bam as evidence
Return breakpoints where too few reads span the breakpoint
'''


def get_breaks(mummerfile):
    '''
    grab mummerfile and give dict of refchr:[positions]
    get rid of vals too close to the beginning/end since it's not worth checking cov there
    '''
    with open(mummerfile, 'r') as f:
        content=[line for line in f.read().split('\n') if line.strip() != '']
    pos={}
    for i in content:
        info=i.split('\t')
        if info[11] not in pos:
            pos[info[11]]=[]
        if int(info[0]) > 300:
            pos[info[11]].append(info[0])
        if abs(int(info[1])-int(info[7])) > 300:
            pos[info[11]].append(info[1])
    return pos
            

def check_drop(position, bamfile, covrange):
    '''
    takes a position [refchr, position] and pysam object containing alignment
    returns whether there was a weird coverage drop +- 1kb 
    '''

def check_span(chrom, position, bamfile, span_len):
    '''
    takes a position [refchr, position] and pysam object containing alignment
    returns whether enough reads span the position on both sides
    '''
samfile=pysam.AlignmentFile(bamfile, "rb")
totalcov=0
spancov=0
for read in samfile.fetch(chrom, position-300, position+300):
    totalcov+=1
    start=position-300
    end=position+300
    if read.reference_end>end and read.reference_start<start:
        spancov+=1
    
def check_breaks(pos, bamfile, covfile, span_len):
    '''
    takes alignment and pos file
    returns list of problematic regions: [chr, position, spanpass, np_drop, ill_drop]
    '''
    breakinfo=[]
    ##read in the pysam object
    span_len=300
    for chrom in pos:
        for i in chrom:
            span=check_span(chrom, i, bamfile, span_len)
            
