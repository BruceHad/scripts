@echo off
REM.-- Prepare the Command Processor --
SETLOCAL ENABLEEXTENSIONS
SETLOCAL ENABLEDELAYEDEXPANSION
REM.-- Do something useful
set "source=Z:\ArchiveMail\out"
set "targetRoot=Z:\ArchiveMail\out\archive"
set /A count=0
set /A maxcount=5000
for %%F in ("%source%\*") do (
	set /A count+=1
	if !count!==!maxcount! goto :next
	for /f "tokens=1,2,3 delims=/ " %%A in ("%%~tF") do (
		if not exist "%targetRoot%\%%C\%%B\" mkdir "%targetRoot%\%%C\%%B\"
		move "%%~fF" "%targetRoot%\%%C\%%B\"
	)
)
:next
REM.-- End of application
pause