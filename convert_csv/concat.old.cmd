@echo off
ECHO Set working directory
pushd %~dp0
setlocal ENABLEDELAYEDEXPANSION
for %%i in (*.2015) do (
  for /f "skip=1 delims=" %%j in ('type "%%i"') do echo %%j >> combined.txt
  echo %%i
)