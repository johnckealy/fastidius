#!/bin/bash
set -e


 IGNORE_PATHS=" -not -path 'src/.git/*' -not -path 'src/.git/*'"


# Comment out all the Mako syntax
for file in $(find src/backend -type f)
do
    # Remove all the comments from the Mako syntax
    sed -i 's/^# % if/% if/g' $file
    sed -i 's/^# % endif$/% endif/g' $file

    # Enclose all the keywords in mako_keywords file with ${ }
    while read -r keyword; do
        echo $keyword
        sed -i s/[[:space:]]$keyword/\ \${$keyword}/g src/main.py
    done < scripts/mako_keywords
done
