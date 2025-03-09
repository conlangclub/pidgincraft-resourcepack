#!/bin/sh
wget https://docs.google.com/spreadsheets/d/1_SCZqJMZ1UrwqbQ69Bxpf0JZVwz93x3tBZFf4DPrEDM/gviz/tq\?tqx\=out:csv\&sheet\=Vocabulary\ Script -O vocab.csv &&
wget https://docs.google.com/spreadsheets/d/1_SCZqJMZ1UrwqbQ69Bxpf0JZVwz93x3tBZFf4DPrEDM/gviz/tq\?tqx\=out:csv\&sheet\=Phrase\ Script -O phrases.csv &&
python3 ./translate.py &&
rm -f scc_resourcepack.zip &&
cd scc_resourcepack &&
zip -r ../scc_resourcepack.zip *