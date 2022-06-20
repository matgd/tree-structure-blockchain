#!/bin/bash

CONFIG_FILE="${1}"
CHANGE_FROM="${2}"

CHANGE_FROM=$((${CHANGE_FROM} + 1))
CHANGE_TO=$((${CHANGE_FROM} - 1))
# PASS n+1, e.g. for 2000-long chain pass 2001


[[ ${CONFIG_FILE} == "" ]] && echo "ERROR: No config file path provided." && exit 1
if ! grep -q "times: 0" ${CONFIG_FILE}; then
    echo "ERROR: Set 'times: 0' in ${CONFIG_FILE}"
    exit 3
fi

DIFFICULTY=0
sed -i "s/0/${CHANGE_FROM}/g" "${CONFIG_FILE}"

# CHANGE DIFFICULTY
sed -i "s/ProofOfWork()/ProofOfWork(difficulty = ${DIFFICULTY})/g" main.py

while [[ "${CHANGE_TO}" != 0 ]]; do
    sed -i "s/${CHANGE_FROM}/${CHANGE_TO}/g" "${CONFIG_FILE}"

    cp ${CONFIG_FILE} config.yaml
    CHANGE_FROM=$((CHANGE_FROM - 1))
    CHANGE_TO=$((CHANGE_TO - 1))
        
    if ! python3 main.py > /dev/null; then 
        echo "ERROR: File 'main.py' not found."
        exit 2
    fi 
    
    cp exec_time.csv extras/1_participants_delete_long_chain/exec_time_long_chain_${CHANGE_FROM}.csv

    echo "${CHANGE_FROM}..."

done | tqdm --total ${2}  # python3 -m pip install tqdm

sed -i "s/1/0/g" "${CONFIG_FILE}"

# CHANGE DIFFICULTY
sed -i "s/ProofOfWork(difficulty = ${DIFFICULTY})/ProofOfWork()/g" main.py

cd extras/1_participants_delete_long_chain
./prepare_results.sh
cd -
