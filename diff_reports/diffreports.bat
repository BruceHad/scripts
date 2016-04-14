@echo off
for %%i in (before\*.*) do (
	for %%j in (after\*.*) do (
		if %%~ni==%%~nj (
		echo excelcompare\bin\excel_cmp %%i %%j
		) else (
		echo Nomatch
		)
	)
)