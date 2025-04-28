#!/bin/bash

for folder in repos/Nebius-Academy-*; do
  # Check if it's a directory
  if [ -d "$folder" ]; then
    new_name=$(echo "$folder" | sed -E 's|^repos/Nebius-Academy-||; s/-[^-]*$//')
    mv "$folder" "repos/$new_name"
  fi
done
