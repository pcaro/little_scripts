#!/bin/bash

if [ $# -lt 1 ]
then
        echo "uso: $0 <clase C>"
        exit -1
fi

ARG1=$1

IP=(${ARG1//./ })

for (( K=1; K<255; K++ ))
do
    IP[3]=$K
    ADDR=${IP[0]}.${IP[1]}.${IP[2]}.$K

    ANS=$(dig -x $ADDR 2>/dev/null | grep -v ";; flags:" | grep -A 1 "ANSWER" | grep "PTR")
    COUNT=$(echo -n $ANS | wc -w)

    if [ $COUNT -gt 0 ]
    then
        echo -n $ADDR" ==> "
        echo $ANS | cut -d' ' -f5
    fi

done