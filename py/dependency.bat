@echo off
echo ============================================
echo    Installation de Leafy Life
echo ============================================
echo.

:: Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installe. Telechargement en cours...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe
    echo Installation de Python...
    python_installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
    del python_installer.exe
    echo Python installe !
    echo.
    :: Recharger les variables d'environnement PATH
    call refreshenv >nul 2>&1
) else (
    echo Python detecte !
)

echo Installation des dependances...
pip install --user flet --quiet
pip install --user pyglet --quiet
pip install --user pynput --quiet

echo.
echo ============================================
echo    Lancement de Leafy Life !
echo ============================================
python py/main.py

pause