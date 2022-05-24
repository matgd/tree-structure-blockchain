#!/bin/bash

TIMESTAMP=$(date +%H%M%S)_$(date +%N)
OUT="results_${TIMESTAMP}.csv"

echo "chain_length,time_s" > "${OUT}"

for FILE in exec_time_long_chain_*; do
    LENGTH=${FILE/exec_time_long_chain_/}
    LENGTH=${FILE/.csv/}
    TIME=$(cat ${FILE} | grep DELETE_CHAIN | cut -d, -f3)
    printf "%s,%s\n" ${LENGTH} ${TIME} >> ${OUT}
done

sed -i -e 's/\r$//' "${OUT}"
