def run_assess(fofn):
    '''take in seq summary texts as file of file names, and report yield, numreads, mean len, median len, avg basequal in a csv'''
    from statistics import median

    filelist=fofn.read().splitlines()
    files=set(filelist)
    ##run=[['yield', 'number of reads', 'mean length', 'median length', 'mean basequal']]
    runyield=0
    numreads=0
    lengths=[]
    totalqual=0
    for seqsum in files:
        with open(seqsum) as f:
            rundata=[x.split('\t') for x in f.read().splitlines()[1::]]
        numreads+=len(rundata)
        for i in rundata:
            if i[7] == 'True':
                runyield+=float(i[12])
                totalqual+=float(i[13])
                lengths.append(int(i[12]))
    runmedian=median(lengths)
    return [str("{0:.3f}".format(runyield/1000000000)), str(numreads), str("{0:.2f}".format(runyield/numreads)), str(int(runmedian)), str("{0:.2f}".format(totalqual/numreads))]


def main(fofn):
    '''print csv line to stdout'''
    print ','.join(run_assess(sys.stdin))


if __name__ == '__main__':
    import sys
    main(sys.stdin)
