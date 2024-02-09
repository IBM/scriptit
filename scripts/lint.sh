#!/usr/bin/env bash

# Change directory to the parent directory of the script
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Initialize an empty string to store file names
fnames=""

# Loop through each argument passed to the script
for fname in "$@"
do
    # Check if the file name ends with ".py" or if it's a directory starting with "scriptit"
    if [[ "$fname" == *".py" ]] || [ -d "$fname" ] && [[ "$fname" == "scriptit"* ]]
    then
        # Add the file name to the list of files to be checked
        fnames="$fnames $fname"
    else
        # Print a message for non-library files that are being ignored
        echo "Ignoring non-library file: $fname"
    fi
done

# If no valid files are found, default to checking files in the "scriptit" directory
if [ "$fnames" == "" ]
then
    fnames="scriptit"
fi

# Run Ruff check on the specified files
ruff check $arg $fnames
