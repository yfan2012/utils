#!/bin/bash

##get some run stats from fq file
yield=`zcat $1 | awk 'BEGIN {ORS=","}; {if (NR%4==2) sum+=length($0)} END {print arr} END {print sum} END {print NR / 4} END {print sum *4 / NR}'`

echo ${1}`basename $yield ,`



