@echo off
echo ============================================
echo    Installation de Leafy Life
echo ============================================
echo.

:: Se placer à la racine du projet (là où est le .bat)
cd /d "%~dp0"

:: Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installe.
    echo Ouverture du Microsoft Store pour installer Python...
    start ms-windows-store://pdp/?ProductId=9NCVDN91XZQP
    echo.
    echo Installe Python depuis le Microsoft Store puis
    echo relance ce fichier install.bat
    pause
    exit
)

echo Python detecte !
echo.
echo Installation des dependances...
python -m pip install --user flet==0.82.0 --quiet --no-warn-script-location
python -m pip install --user pyglet==2.1.13 --quiet --no-warn-script-location
python -m pip install --user pynput==1.8.1 --quiet --no-warn-script-location
python -m pip install --user pygame==2.6.1 --quiet --no-warn-script-location

echo.
echo ============================================
echo    Lancement de Leafy Life !
echo ============================================
python sources/main.py

pause