@echo off
echo Comparison Results > results.txt
for %%i in (before\*.*) do (
	for %%j in (after\*.*) do (
		if %%~ni==%%~nj (
		echo ------- Match %%i %%j ------- >> results.txt
		excelcompare\bin\excel_cmp %%i %%j >> results.txt
		)
	)
)