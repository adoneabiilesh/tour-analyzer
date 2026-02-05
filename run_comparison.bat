@echo off
echo ===========================================
echo Tour Website Comparison Tool
echo ===========================================
echo.

REM Check if analysis results exist
if not exist "analysis_results.json" (
    echo ERROR: analysis_results.json not found!
    echo Run analyzer first: python analyzer.py
    exit /b 1
)

echo Step 1: Installing dependencies (if needed)...
pip install pillow python-slugify -q

echo.
echo ===========================================
echo IMPORTANT INSTRUCTIONS:
echo ===========================================
echo.
echo 1. Open a NEW terminal window
echo 2. Navigate to your template:
echo    cd ..\rome-tour-tickets
echo 3. Start dev server:
echo    npm run dev
echo.
echo 4. Come back here and press any key to continue...
echo.
pause >nul

echo.
echo Running comparison...
python quick_compare.py

echo.
echo ===========================================
echo DONE!
echo Check the comparisons/ folder for GIFs
echo ===========================================
pause
