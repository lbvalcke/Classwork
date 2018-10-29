#!/bin/bash

if [[ "$#" -ne 1 ]]; then
    echo "usage: $0 <grid filename>"
    exit 0
fi

java -cp DrawGrid.jar DrawGrid $1
