#!/bin/bash

##Set up the run name and input options
if [ -d "$1" ]; then
    prefix=` echo $1 | rev |  cut -d '/' -f1 | rev `
    if [ -z $prefix ]; then
	prefix=` echo $1 | rev |  cut -d '/' -f2 | rev `
    fi
else
    echo Enter sample directory
    exit
fi


##set up dirs
srcpath=~/Code/utils/marcc
outdir=$1/np_index_logs
raw=$1/raw
mkdir -p $outdir
mkdir -p $1/np_index 

##figure out array size
numdirs=`find $raw/* -maxdepth 0 -type d | wc -l `
dummy=1
maxdir=`expr $numdirs - $dummy`
echo maxdir is $maxdir
echo $prefix



sbatch --array=0-$maxdir --job-name=$prefix --output=$outdir/$prefix.%A_%a.out $srcpath/np_index.scr $1

