@echo off
setlocal

set "YYYY=%date:~6,4%"
set "MM=%date:~3,2%"
set "DD=%date:~0,2%"


set "FORMATTED_DATE=%YYYY%-%MM%-%DD%"
:: Se deplacer dans le repertoire de travail GIT PYTHON ou autre
cd /d "%PYTHR%"
:: SELECTIONNER dossier ou fichier a envoyer...
git add "%CONSOLE%/Kivy/remplisseur_I/option.json"

:: Vérifie si des fichiers sont en cache (staged)
git diff --cached --quiet

if errorlevel 1 (
    git commit -m "UPDATES_(%FORMATTED_DATE%)"

    :: Vérifie si remote origin existe déjà
    git remote get-url origin >nul 2>&1
    if errorlevel 1 (
        :: Si pas d'URL, 
        git remote add origin "https://github.com/Ryan731-max/POWERSHELL-PLAN.git"
    )

    :: Push sur la branche courante (ex: main)
    git push -u origin main
) else (
    echo Aucun changement staged, pas de commit.
)


@REM git fetch origin && git pull origin main


@REM git add ""
@REM git add commit ""