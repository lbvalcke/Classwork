#!/bin/bash

echo "Getting hrc-feb.json file..."

wget -O hrc-feb.json https://www.classes.cs.uchicago.edu/archive/2016/fall/12100-1/data/hrc-feb.json

echo
echo
echo
echo "Getting djt-feb.json file..."

wget -O djt-feb.json https://www.classes.cs.uchicago.edu/archive/2016/fall/12100-1/data/djt-feb.json

echo
echo
echo
echo "Getting hrc-500.json file..."

wget -O hrc-500.json https://www.classes.cs.uchicago.edu/archive/2016/fall/12100-1/data/hrc-500.json

echo
echo
echo
echo "Getting hrc-500.json file..."

wget -O djt-500.json https://www.classes.cs.uchicago.edu/archive/2016/fall/12100-1/data/djt-500.json


echo "Getting hrc-all.jsonz file..."

wget -O hrc-all.json.gz https://www.classes.cs.uchicago.edu/archive/2016/fall/12100-1/data/hrc-all.json.gz
gunzip hrc-all.json.gz

echo
echo
echo
echo "Getting djt-all.json file..."

wget -O djt-all.json.gz https://www.classes.cs.uchicago.edu/archive/2016/fall/12100-1/data/djt-all.json.gz
gunzip djt-all.json.gz