@echo off
REM === FIXED: Assumes clean local project exists ===
set REPO_URL=https://github.com/lihsianghsu/nlp-demo-app.git
REM Clean remote without touching LOCAL files
git remote set-url origin %REPO_URL%
git push origin main --force  REM Only if you have clean commits locally

REM Better: Delete/recreate repo on GitHub web, then push fresh
echo "Delete repo on GitHub web first, then run Create.bat instead."
pause
