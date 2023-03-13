@echo 

setlocal enabledelayedexpansion

:: parameters:
:: 1 = Setup Virtual Environment

:: Defines virtual environment -  if not present assumes TRUE
if %1==. (
    SET "SETVENV=TRUE"
) ELSE (
    SET "SETVENV=%2"
)

set PROJECTPATH=%~dp0

set "PYTHONDIR=C:\Users\Leone\AppData\Local\Programs\Python\Python310"
set "VENV=CarProjectVenv"

:: Loop thorugh all directories in PATH variable
:loop
FOR /F "tokens=1* delims=;" %%a IN ("%path_loop%") DO (
    rem Remove directory if it contains word python
    @ECHO %%a | findstr /i /c:"python" >NUL
    IF ERRORLEVEL 1 (
        IF .!new_path!==. (
            SET new_path=%%a
        ) ELSE (
            SET new_path=!new_path!;%%a
        )
    )
    SET path_loop=%%b
)
IF DEFINED path_loop GOTO :loop

set "PATH=%PYTHONDIR%;%PYTHONDIR%/Scripts;%PATH%"
set "PYTHONPATH=%PYTHONDIR%\Lib;%PYTHONDIR%\Lib\site-packages;%PYTHONDIR%\DLLs;"
set "PYTHONHOME=%PYTHONDIR%"

IF %SETVENV%==TRUE (
    IF exist %PROJECTPATH%\%VENV%\ (
        echo %VENV% Virtual Environment folder aready exists.
    ) ELSE (
        echo Creating Virtual Environment...
        %PYTHONDIR%\python.exe -m venv %VENV%
        echo DONE.
        echo Installing requirements...
        call %PROJECTPATH%\%VENV%\Scripts\activate
        pip install -r requirements.txt
        call %PROJECTPATH%\%VENV%\Scripts\deactivate
        echo DONE.
    )
)