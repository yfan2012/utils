#!/bin/bash

##get some run stats from fq file

if [[ $1 == *.gz ]] ;  then
    yield=`zcat $1 | awk 'BEGIN {ORS=","}; {if (NR%4==2) sum+=length($0)} END {print arr} END {print sum} END {print NR / 4} END {print sum *4 / NR}'`
else
    yield=`awk 'BEGIN {ORS=","}; {if (NR%4==2) sum+=length($0)} END {print arr} END {print sum} END {print NR / 4} END {print sum *4 / NR}' $1`
fi
    
echo ${1}`basename $yield ,`



