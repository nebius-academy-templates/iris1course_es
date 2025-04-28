#!/bin/bash

strings=("test_homework_backend")

for str in "${strings[@]}"; do
  curl --output "repos/${str}.zip" -L \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer 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" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "https://api.github.com/repos/nebius-academy/${str}/zipball/main"
done
