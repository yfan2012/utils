library(tidyverse)
library(Biostrings)
library(ggplot2)
library(argparse)

parser <- ArgumentParser()
parser$add_argument('-i', '--input', type='character', help='fasta file')
parser$add_argument('-o', '--outdir', type='character', help='path to output directory')
parser$add_argument('-p', '--prefix', type='character', help='prefix to name files')
args <- parser$parse_args()

fafile=args$input
outdir=args$outdir
prefix=args$prefix

fa=readDNAStringSet(fafile)
fadf=data.frame(seqname=names(fa), len=width(fa))

pdf(paste0(outdir, '/',prefix, '_len_hist.pdf'), height=8.5, width=11)
ggplot(fadf, aes(x=len)) +
    geom_histogram(binwidth=1000, colour='black', fill='black') +
    xlab('Sequence Lengths') +
    scale_y_log10() +
    ylab('Number of Sequences (log scale)') +
    ggtitle(paste0('Sequence Length Histogram:',prefix)) +
    theme_bw()
dev.off()
