#!/usr/bin/env bash

set -Eeuo pipefail

# For each theme, check that:
#   - we have handpicked pictures folder for the theme
#   - the folder has a least one picture
grep "=" roboquote/entities/themes.py | cut -d "\"" -f 2 | while read -r line; do

    # Check that we have handpicked pictures folder for the theme
    if [ ! -d "pictures/$line" ]; then
        echo "Missing handpicked pictures folder for $line"
        exit 1
    fi

    # Check that we have at least one background picture for the theme
    num_files=$(find "pictures/$line" -maxdepth 1 -type f -name "*.jpg" | wc -l)
    if [ ! "$num_files" -gt 0 ]; then
        echo "No pictures in $line handpicked pictures folder"
        exit 1
    fi
done
