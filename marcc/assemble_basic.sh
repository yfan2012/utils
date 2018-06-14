#!/bin/bash

sampdir=$1
gsize=$2

prefix=`echo $1 | rev | cut -d / -f 1 | rev`

fq=$sampdir/fastqs/$prefix.fq
canudir=$sampdir/canu_assembly


echo $prefix
echo $gsize
echo $fq
echo $canudir

if [ -f $1 ] ; then
##    canu \
##	-p $prefix -d $canudir \
##	-gridOptions="--time=22:00:00 --account=mschatz1" \
##	genomeSize=$gsize \
##	-nanopore-raw $fq
fi
