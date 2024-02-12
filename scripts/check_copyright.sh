#!/usr/bin/env bash

notice='################################################################################
# Copyright The Script It Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################'

# Run from the root of the project
cd $(dirname ${BASH_SOURCE[0]})/..

# Function helper to check and optionally fix headers
function check_file {
    fname=$1
    if git check-ignore -q $fname
    then
        return 0
    fi
    second_line=$(cat $fname | head -n2 | tail -n1)
    if [ "$second_line" != "# Copyright The Script It Authors" ]
    then
        echo "Fixing missing copyright in $fname"
        file_content=$(cat $fname)
        echo "$notice" > $fname
        echo "$file_content" >> $fname
        return 1
    fi
}

exit_code=0
for fname in $(find scriptit -name "*.py")
do
    check_file $fname
    file_exit_code=$?
    exit_code=$(expr "$exit_code" "+" "$file_exit_code")
done
exit $exit_code
