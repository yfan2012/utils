suppressPackageStartupMessages(library(ggplot2))
suppressPackageStartupMessages(library(tidyverse))
suppressPackageStartupMessages(library(argparse))
suppressPackageStartupMessages(library(plyr))
suppressPackageStartupMessages(library(foreach))
suppressPackageStartupMessages(library(gridExtra))

mcoordsfile='/kyber/Data/Nanopore/projects/nina/mummer/st31_wtdbg2/st31_canu.mcoords'
outdir='~/Dropbox/yfan/nina_fungus/tigbreaks/'

mcoords=read_tsv(mcoordsfile, col_names=F)
colnames(mcoords)=c('rstart', 'rend', 'qstart', 'qend', 'rlen', 'qlen', 'ident', 'rtotal', 'qtotal', 'sim', 'stop', 'rname', 'qname')
tigs=unique(mcoords$rname)

outfile=paste0(outdir, 'st31_wtdbg2.st31_canu.pdf')

##want all plots on one page, so i *should* be able to add all the plot objects to a list and arrange?
##lol let's see

maxlen=max(mcoords$rtotal)


plots=foreach(i=1:length(tigs)) %dopar% {
    x=tigs[i]
    tigcoords=mcoords[mcoords$rname==x,]
    tigcoords$tile=tigcoords$rstart+(tigcoords$rlen/2)
    tigcoords$label=paste0(tigcoords$qname,'\n', as.character(tigcoords$qstart), ':', as.character(tigcoords$qend))
    tigcoords$strand=.2+(as.numeric(tigcoords$qstart>tigcoords$qend)*.6)
    
    tiglength=tigcoords$rtotal[1]

    ##will need to change when doing the facet wrap thing
   
    plot=ggplot(tigcoords, aes(x=tile, y=qname, width=rlen, fill=qname)) +
        geom_tile(aes(fill=qname, alpha=strand)) +
        geom_text(aes(label=label)) +
        ggtitle(tigcoords$rname[1]) +
        xlim(0, tiglength) +
        xlab('Contig Coordinate') +
        theme_bw() +
        theme(axis.text.y=element_blank(), axis.title.y=element_blank(), legend.position="none")

    return(plot)
}

pdf(outfile, height=1000, width=100)
do.call('grid.arrange', c(plots, ncol=1))
##grid.arrange(plots[[1]], plots[[2]], plots[[3]])
dev.off()
