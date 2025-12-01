@echo off
echo ========================================
echo   Split Bill - Iniciar Servidor
echo ========================================
echo.

cd /d "%~dp0"

echo Limpiando cache...
if exist __pycache__ rmdir /s /q __pycache__

echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo.
echo ========================================
echo   Iniciando Flask en puerto 5000...
echo ========================================
echo.
echo   Abre tu navegador en:
echo   http://localhost:5000
echo.
echo   Presiona Ctrl+C para detener
echo ========================================
echo.

python app.py

pause

