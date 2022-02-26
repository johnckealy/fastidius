#!/bin/bash
set -e


# Comment out all the Mako syntax
for file in $(find fastidius/app_template/backend -type f)
do
    # Remove all the comments from the Mako syntax
    sed -i 's/# % if/% if/g' $file
    sed -i 's/# % endif$/% endif/g' $file
    sed -i 's/# % else:/% else/g' $file
    # Enclose all the keywords in mako_keywords file with ${ }
    while read -r KEYWORD; do
        echo $file
        sed -i s/[[:space:]]$KEYWORD/\ \${$KEYWORD}/g $file
    done < scripts/mako_keywords
done
