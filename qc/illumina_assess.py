def illrunstats(r1obj, r2obj):
    import statistics
    content1=r1obj.readlines()
    content2=r2obj.readlines()
    quals=content1[3::4]+content2[3::4]

    runyield=0
    numreads=len(quals)
    lengths=[]
    totalqual=0
    for i in quals:
        runyield+=len(i)
        lengths.append(len(i))
        for j in i:
            totalqual+=ord(j)-33

    return [str(runyield), str(numreads), str("{0:.2f}".format(float(runyield)/float(numreads))), str(statistics.median(lengths)), str("{0:.2f}".format(float(totalqual)/float(runyield)))]

    
def main(read1, read2, gz):
    import gzip
    if gz:
        print ','.join(illrunstats(gzip.open(args.read1, 'rb'), gzip.open(args.read2)))
    else:
        print ','.join(illrunstats(open(args.read1, 'rb'), open(args.read2, 'rb')))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='get run stats from fq or fq.gz files')
    parser.add_argument('--read1','-r',  help='read1 input fq or fq.gz file', type=str)
    parser.add_argument('--read2', '-s', help='read1 input fq or fq.gz file', type=str)
    parser.add_argument('--compressed', dest='gz', action='store_true', help='if file is compressed (assumes compressed)')
    parser.add_argument('--uncompressed', dest='gz', action='store_false', help='if file is compressed (assumes compressed)')
    parser.set_defaults(gz=True)
    args = parser.parse_args()

    main(args.read1, args.read2, args.gz)
    
    
