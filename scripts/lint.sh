#!/usr/bin/env bash

cd $(dirname ${BASH_SOURCE[0]})/..

fnames=""
for fname in $@
do
    if [[ "$fname" == *".py" ]] || [ -d $fname ] && [[ "$fname" == "scriptit"* ]]
    then
        fnames="$fnames $fname"
    else
        echo "Ignoring non-library file: $fname"
    fi
done
if [ "$fnames" == "" ]
then
    fnames="scriptit"
fi

ruff check $arg $fnames
