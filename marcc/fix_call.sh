#!/bin/bash

for i in $1/called/* ;
do
    num=`echo $i | rev | cut -d / -f 1 | rev`
    touch $1/call_done/$num.txt
done
