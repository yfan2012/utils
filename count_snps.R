library(tidyverse)
library(plyr)
library(grid)
library(gridExtra)
library(argparse)

parser <- ArgumentParser()
parser$add_argument('-i', '--input', type='character', help='vcf file from parsnp')
parser$add_argument('-o', '--outdir', type='character', help='path to output directory')
args <- parser$parse_args()

vcf=args$input
outdir=args$outdir

snptab=read_tsv(vcf, comment='##') %>%
    filter(FILTER=='PASS')

numsamps=dim(snptab)[2]-9
snps=matrix(nrow=numsamps, ncol=numsamps)
for (i in 1:numsamps) {
    for (j in 1:numsamps) {
        snps[i, j]=sum(snptab[,i+9]!=snptab[,j+9])
    }
}
names=colnames(snptab)[10:dim(snptab)[2]]

for (i in 1:length(names)){
    ##newname=strsplit(gsub('.spades.fasta', '',names[i]), split= '_', fixed=TRUE)[[1]][1]
    newname=gsub('.fasta', '',names[i])
    names[i]=newname
}

rownames(snps)=names
colnames(snps)=names

##remove the 'new' samples since we trust that they're right
for (i in 1:length(names)){
    newname=strsplit(names[i], split= '_', fixed=TRUE)[[1]][1]
    names[i]=newname
}

rownames(snps)=names
colnames(snps)=names

snps[lower.tri(snps,diag=TRUE)]=''

csvpath=paste0(outdir, '/', 'numsnps.csv')
write.table(snps, csvpath, sep=',', col.names=NA)

pdfpath=paste0(outdir, '/', 'numsnps.pdf')
pdf(pdfpath, width=15, height=7)
grid.table(snps)
dev.off()

