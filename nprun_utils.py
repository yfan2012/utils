'''
check some metrics of nanopore runs
'''
import argparse
import os

def check_unique(indir):
    '''
    take an input directory basecalled with albacore and figure out if the number of reads is consistent between workspace, fqs, and maybe fast5s
    '''

    import os

    numfolders=len(os.listdir(indir+'/called'))
    
    read_ids=[]
    for i in range(0,numfolders):
        sspath=indir+'/called/'+str(i)+'/sequencing_summary.txt'
        with open(sspath, 'r') as f:
            for line in f:
                read_ids.append(line.split('\t')[1])
            
    ssnum=len(read_ids)
    ssunique=len(set(read_ids))
            
    fq_lines=0
    for i in range(0,numfolders):
        for filt in ['/pass', '/fail']:
            filtpath=indir+'/called/'+str(i)+'/workspace'+filt
            for bc in os.listdir(filtpath):
                bcpath=filtpath+'/'+bc
                for fq in os.listdir(bcpath):
                    if fq.endswith('.fastq'):
                        with open(bcpath+'/'+fq) as f:
                            for line in f:
                                fq_lines+=1

    fq_reads=fq_lines/4
    
    return [fq_reads, ssunique, ssnum]



def main(indir):
    counts=check_unique(indir)
    print('Reads in fastqs: ', str(counts[0]))
    print('Number of unique read_ids: ', str(counts[1]))
    print('Number of read_ids: ', str(counts[2]))

    
if __name__ == '__main__':
    parser=argparse.ArgumentParser(description = 'Figure out some stuff about reads of the run')
    parser.add_argument('--indir', '-i', type=str, required=True,  help='input directory path')
    args=parser.parse_args()

    main(args.indir)
