'''
functions for barcoding stuff
'''

def bc_percent(indir, outfile):
    import os

    numdirs=os.listdir(indir+'/called')
    bc_bases=[]
    barcodes=[]
    
    for i in numdirs:
        seqsum=indir+'/called/'+str(i)+'/sequencing_summary.txt'
        with open(seqsum, 'r') as f:
            for line in f:
                if line.split('\t')[0]!='filename':
                    bc_bases.append([line.split('\t')[19],line.split('\t')[12]])
                    barcodes.append(line.split('\t')[19])
                
    existing_bc=set(barcodes)
    bc_counts={}
    
    for i in existing_bc:
        bases=0
        for j in bc_bases:
            if j[0]==i:
                bases+=int(j[1])
        mbases=float(bases)/1000000
        bc_counts[i]=[barcodes.count(i), mbases]
        
        
    total=0
    for i in bc_counts:
        total+=int(bc_counts[i][0])
    
    with open(outfile, 'w') as f:
        f.write(','.join(['barcode', 'num_reads', 'percent','mbase_yield'+'\n']))
        for i in bc_counts:
            perc=float(bc_counts[i][0])/float(total)
            f.write(','.join([str(i), str(bc_counts[i][0]), str(perc), str(bc_counts[i][1])+'\n']))


def main(indir, outfile):
    bc_percent(indir, outfile)
    

if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description = 'Figure out some stuff about barcodes of the run')
    parser.add_argument('--indir', '-i', type=str, required=True,  help='input directory path')
    parser.add_argument('--outfile', '-o', type=str, required=True,  help='output path')
    args=parser.parse_args()
    
    main(args.indir, args.outfile)
