from statistics import median

def run_assess(seqsum):
    '''take in a seq summary text, and report yield, numreads, mean len, median len, avg basequal in a csv'''

    ##run=[['yield', 'number of reads', 'mean length', 'median length', 'mean basequal']]
    runyield=0
    lengths=[]
    totalqual=0

    ##with open(seqsum) as f:
    rundata=[x.split('\t') for x in seqsum.read().splitlines()[1::]]
    numreads=len(rundata)
    for i in rundata:
        if i[9] == 'True':
            runyield+=float(i[13])
            totalqual+=float(i[14])
            lengths.append(int(i[13]))
    runmedian=median(lengths)
    return [str("{0:.3f}".format(runyield/1000000000)), str(numreads), str("{0:.2f}".format(runyield/numreads)), str(int(runmedian)), str("{0:.2f}".format(totalqual/numreads))]

def main(sumfile):
    summary=run_assess(sumfile)

if __name__ == '__main__':
    import sys
    main(sys.stdin)
