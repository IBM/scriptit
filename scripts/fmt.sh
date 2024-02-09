#!/usr/bin/env bash

# Run pre-commit checks on all files
pre-commit run --all-files
RETURN_CODE=$?

# Function to echo warning messages in yellow color
function echoWarning() {
  LIGHT_YELLOW='\033[1;33m'
  NC='\033[0m' # No Color
  echo -e "${LIGHT_YELLOW}${1}${NC}"
}

# If pre-commit checks failed
if [ "$RETURN_CODE" -ne 0 ]; then
  # If not running in CI environment
  if [ "${CI}" != "true" ]; then
    # Print warning messages for local environment
    echoWarning "☝️ This appears to have failed, but actually your files have been formatted."
    echoWarning "Make a new commit with these changes before making a pull request."
  else
    # Print warning messages for CI environment
    echoWarning "This test failed because your code isn't formatted correctly."
    echoWarning 'Locally, run `make run fmt`, it will appear to fail, but change files.'
    echoWarning "Add the changed files to your commit and this stage will pass."
  fi

  # Exit with the return code of the pre-commit checks
  exit $RETURN_CODE
fi
