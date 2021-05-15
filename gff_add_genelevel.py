import argparse

def parseArgs():
    parser=argparse.ArgumentParser(description='take a gff and add genelevel info')
    parser.add_argument('-i', '--infile', type=str, required=True, help='input gff')
    parser.add_argument('-o', '--outfile', type=str, required=True, help='output gff')
    args=parser.parse_args()
    return args


def augustus_addgenes(augustus):
    '''
    take augustus annotations
    return agustus annotations grouped by genes
    '''
    ##assumes gene level is not listed
    augdict={}
    for i in augustus:
        parent=i[8].split(';')[1].split('=')[1]
        gene=parent.split('.')[0]
        if gene in augdict:
            augdict[gene].append(i)
        else:
            augdict[gene]=[i]
    return(augdict)


def liftoff_addgenes(liftoff):
    '''
    take liftoff annotations
    return liftoff annotations grouped by genes
    '''
    liftdict={}
    for i in liftoff:
        if i[2]!='gene':
            gene=i[8].split(';')[1].split('=')[1]
            if gene in liftdict:
                liftdict[gene].append(i)
            else:
                liftdict[gene]=[i]
    return(liftdict)


def liftoff_findgenes(liftoff):
    '''
    get dict of gene info
    '''
    liftgenes={}
    for i in liftoff:
        if i[2]=='gene':
            gene=i[8].split(';')[0].split('=')[1]
            liftgenes[gene]=i
    return(liftgenes)


def stringtie_addgenes(stringtie):
    '''
    take stringtie annotations
    return stringtie annotations grouped by genes
    assumes no gene level
    '''
    stringdict={}
    for i in stringtie:
        info=[x.lstrip() for x in i[8].replace('"', '').split(';')]
        gene=info[0].split(' ')[1]
        newinfo=';'.join(['='.join(x.split(' ')) for x in info])
        newentry=i[0:-1]
        newentry.append(newinfo)
        if gene in stringdict:
            stringdict[gene].append(newentry)
        else:
            stringdict[gene]=[newentry]
    return(stringdict)


def writegenes(tooldict):
    '''
    take either stringdict or augdict
    return something writable
    '''
    final=[]
    for i in tooldict:
        tigs=[]
        strands=[]
        info=[]
        starts=[]
        ends=[]
        info=[]
        tool=tooldict[i][0][1]
        for j in tooldict[i]:
            tigs.append(j[0])
            strands.append(j[6])
            starts.append(int(j[3]))
            ends.append(int(j[4]))
            info.append(j)
        if len(set(tigs))==1 and len(set(strands))==1:
            start=min(starts)
            end=max(ends)
            final.append([tigs[0], tool, 'gene', str(start), str(end), '.' , strands[0], '.', 'ID='+i])
            final.extend(info)
    return(final)
    

def addtranscripts(toolfinal):
    '''
    take list of lists
    get dict of transcript info in transcript info
    '''
    transdict={}
    genedict={}
    for i in toolfinal:
        if i[2]!='gene':
            parent=i[8].split(';')[1].split('=')[1]
            gene=parent.split('.')[0]
            if parent in transdict:
                transdict[parent].append(i)
            else:
                transdict[parent]=[i]
            if gene in genedict:
                genedict[gene].append(parent)
            else:
                genedict[gene]=[parent]
    transinfo={}
    for i in genedict:
        uniquescripts=list(set(genedict[i]))
        for j in uniquescripts:
            tigs=[]
            strands=[]
            info=[]
            starts=[]
            ends=[]
            info=[]
            tool=transdict[j][0][1]
            for k in transdict[j]:
                tigs.append(k[0])
                strands.append(k[6])
                starts.append(int(k[3]))
                ends.append(int(k[4]))
                info.append(k)
            if len(set(tigs))==1 and len(set(strands))==1:
                start=min(starts)
                end=max(ends)
                transinfo[j]=[tigs[0], tool, 'transcript', str(start), str(end), '.' , strands[0], '.', 'ID='+j]
    newfinal=[]
    for i in toolfinal:
        if i[2]=='gene':
            newfinal.append(i)
            gene=i[8].split('=')[1]
            transcriptlist=list(set(genedict[gene]))
            for j in transcriptlist:
                newfinal.append(transinfo[j])
                newfinal.extend(transdict[j])
    return(newfinal)
                

def uniqueid(liftgenes):
    '''
    make sure all ids are unique
    '''


def main(infile, outfile):
    '''
    run stuff
    '''
    with open(infile, 'r') as f:
        content=f.read().split('\n')
        augustus=[]
        liftoff=[]
        stringtie=[]
        for i in content:
            if len(i)>0:
                featinfo=i.split('\t')
                if featinfo[1]=='AUGUSTUS':
                    augustus.append(featinfo)
                elif featinfo[1]=='Liftoff':
                    liftoff.append(featinfo)
                elif featinfo[1]=='Genemark.hmm':
                    augustus.append(featinfo)
                elif featinfo[1]=='StringTie':
                    stringtie.append(featinfo)

    augdict=augustus_addgenes(augustus)
    liftdict=liftoff_addgenes(liftoff)
    liftgenes=liftoff_findgenes(liftoff)
    stringdict=stringtie_addgenes(stringtie)

    augwrite=writegenes(augdict)
    stringfinal=writegenes(stringdict)

    augtrans=addtranscripts(augwrite)

    liftlist=[]
    with open(outfile, 'w') as f:
        ##loop through liftoff first
        for gene in liftgenes:
            gid=liftgenes[gene][8].split(';')
            numdups=1
            ##check if gid is already used
            if gid not in liftlist:
                liftlist.append(gid)
                f.write('\t'.join(liftgenes[gene])+'\n')
            else:
                newid=gid+'_'+str(numdups)
                liftlist.append(newid)
                f.write('\t'.join(liftgenes[gene][8].replace(gid, newgid)))
            for i in liftdict[gene]:
                f.write('\t'.join(i)+'\n')
        for i in augtrans:
            f.write('\t'.join(i)+'\n')
        for i in stringfinal:
            f.write('\t'.join(i)+'\n')
            

if __name__ == '__main__':
    args=parseArgs()
    main(args.infile, args.outfile)
    
                
    

        
    
    
