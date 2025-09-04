@echo off
REM Batch file to build Sphinx documentation

SET SPHINX_DOCS_DIR="C:\Users\dahl\OneDrive\Open Voice Network\GitHub\openfloor-python\python\src\sphinx_docs"

echo Navigating to documentation directory: %SPHINX_DOCS_DIR%
cd /d %SPHINX_DOCS_DIR%

echo Starting Sphinx build...
python -m sphinx -b html . _build

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Sphinx build failed!
    echo Please check the output above for details.
    echo.
    goto :end
)

echo.
echo Sphinx build completed successfully!
echo You can find the generated HTML documentation in: %SPHINX_DOCS_DIR%\_build\html
echo.

:end
pause