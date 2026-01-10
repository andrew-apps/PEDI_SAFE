@echo off
echo ========================================
echo PediSafe - Automated Testing Suite
echo ========================================
echo.

cd pedisafe

echo Verificando archivos de conocimiento...
if not exist "knowledge\*.md" (
    echo ERROR: No se encontraron archivos .md en knowledge/
    pause
    exit /b 1
)

echo.
echo Archivos de conocimiento encontrados:
dir /b knowledge\*.md

echo.
echo ========================================
echo Ejecutando tests criticos...
echo ========================================
python -m pytest test_pedisafe.py -v -m critical --html=report.html --self-contained-html

echo.
echo ========================================
echo Ejecutando TODOS los tests...
echo ========================================
python -m pytest test_pedisafe.py -v --html=report.html --self-contained-html

echo.
echo ========================================
echo Tests completados!
echo Reporte HTML: pedisafe\report.html
echo ========================================
pause
