#!/bin/bash

echo "Starting project cleanup..."

# 1. Update .gitignore to ensure venv and pycache never return
echo "Updating .gitignore..."
cat <<EOT > .gitignore
# Environments
venv/
env/
.env

# Python junk
__pycache__/
*.pyc
*.pyo
*.pyd

# OS files
.DS_Store
Thumbs.db

# Monitoring/Local config
prometheus_local.yml
EOT

# 2. Remove venv and cache from Git tracking (without deleting them locally)
echo "Removing venv and pycache from Git index..."
git rm -r --cached venv/ 2>/dev/null
git rm -r --cached __pycache__/ 2>/dev/null

# 3. Organize scripts into the 'src' directory
echo "Organizing files into src/..."
mkdir -p src
# Moving logic and test files into src
mv load_test.py models.py push_metrics.py test_models.py src/ 2>/dev/null

# 4. Finalize changes
echo "Committing changes..."
git add .
git commit -m "Chore: Cleaned project structure, removed venv from git, and organized src"

echo "Cleanup complete! Run 'git push origin main' to update GitHub."
