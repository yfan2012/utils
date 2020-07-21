library(tidyverse)
library(argparse)

parser=ArgumentParser()
parser$add_argument('-i', '--input', type='character', required=TRUE, help='sequencing summary file from guppy')
parser$add_argument('-o', '--output', type='character', required=TRUE, help='output pdf file')
parser$add_argument('-p', '--prefix', type='character', required=FALSE, default='', help='run prefix for titles and things')
args=parser$parse_args()

outfile=args$output
sumfile=args$input

sumdata=read_tsv(sumfile)

yield=sum(sumdata$sequence_length_template)
printyield=as.character(signif(yield, 3)/1000000000)


if (args$prefix!='') {
    samp=paste0(args$prefix, ', Yield=', printyield, 'Gb')
}else{
    samp=paste0('Read Length Histogram, Yield=', printyield, 'Gb')
}

pdf(outfile, h=7, w=15)
ggplot(sumdata, aes(x=sequence_length_template)) +
    geom_histogram(colour='#00BFC4', fill='#00BFC4', alpha=.3) +
    ggtitle(samp) +
    xlab('Read Length') +
    theme_bw()
dev.off()
    
