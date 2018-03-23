#!/bin/bash

prefix=` basename $1 .fq `
echo $prefix

##Determine genome length
if [[ $prefix == *"Ecoli"* ]] ; then
    ##k-12 size
    gsize=4.6m
elif [[ $prefix == *"KLPN"* ]] ; then
    ##klpn size used for all others
    gsize=5.3m
elif [[ $prefix == *"AB"* ]] ; then
    ##Acinetobacter baumannii
    gsize=4m
elif [[ $prefix == *"cloacae"* ]]; then
    ##E. cloacae
    gsize=5.3m
elif [[ $prefix == *"Citrobacter"* ]]; then
    gsize=5.2m
elif [[ $prefix == *"Pantoea"* ]]; then
    gsize=3.9m 
elif [[ $prefix == *"amalon"* ]]; then
    gsize=5.6m
elif [[ $prefix == *"radio"* ]]; then
    gsize=3.2m
elif [[ $prefix == *"aero"* ]]; then
    gsize=4.9m
else 
    echo 'Cant figure out what the org is. Pls name ur fastq better. #datahygiene'
fi


##Assemble if it's not already done
if [ -f $1 ] ; then
    canu \
	-p $prefix -d $2 \
	-gridOptions="--time=22:00:00 --account=mschatz1" \
	genomeSize=$gsize \
	-nanopore-raw $1
fi
