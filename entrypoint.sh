#!/bin/bash

set -euo pipefail

echo "==================="

# Configure Git
git config --global user.name "$INPUT_NAME"
git config --global user.email "$INPUT_EMAIL"
git config --global --add safe.directory "${GITHUB_WORKSPACE}"

# Check for API key
if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "Error: OPENAI_API_KEY is required." >&2
  exit 1
fi

# Change to GitHub workspace
echo "Changing to the GitHub workspace directory: ${GITHUB_WORKSPACE}"
cd "${GITHUB_WORKSPACE}"

# Fetch the latest `main` branch and reset
echo "Fetching the latest main branch..."
git fetch origin main
git reset --hard origin/main

# Analyze the file structure
echo "Analyzing file structure..."
if [ -d "src" ]; then
  echo "Detected src folder. Limiting file structure analysis to src/."
  find src -type f \( -iname "*.js" -o -iname "*.ts" -o -iname "*.tsx" -o -iname "*.jsx" -o -iname "*.json" \) > file_structure.txt
else
  echo "No src folder detected. Analyzing entire project structure."
  find . -type f \( -iname "*.js" -o -iname "*.ts" -o -iname "*.tsx" -o -iname "*.jsx" -o -iname "*.json" \) > file_structure.txt
fi

# Run Python script to generate README
echo "Running Python script to generate README..."
/venv/bin/python /generate_readme.py

# Commit and push the changes
if [[ -f "README.md" ]]; then
  echo "Committing and pushing changes..."
  git add README.md
  git commit -m "Update README"
  git push --force
else
  echo "Error: README.md not generated." >&2
  exit 1
fi

echo "Workflow completed successfully."
