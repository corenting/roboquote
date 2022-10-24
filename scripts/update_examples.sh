#!/usr/bin/env bash

set -Eeuo pipefail

for i in {1..3}; do
    poetry run python main.py doc/examples/"$i".jpg
    convert -geometry 1000x doc/examples/"$i".jpg doc/examples/"$i".jpg
done
