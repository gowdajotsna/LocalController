#!/bin/bash

# Script to delete all files starting with 'kconfig' in the current directory

echo "Searching for files starting with 'kconfig' in the current directory..."

# Find and delete files
find . -maxdepth 1 -type f -name 'kconfig*' -exec rm -v {} \;

echo "Deletion complete."

