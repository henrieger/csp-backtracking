#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ANSWER=$(python $SCRIPT_DIR/dimacs_to_csp.py $1 | $SCRIPT_DIR/csp.py | head -n1)
if [[ $ANSWER == "INVIAVEL" ]] 
then
  echo "UNSAT" > $2
else
  echo "SAT" > $2
fi
