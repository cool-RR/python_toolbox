@echo off

xcopy ""%~dp0"\simpack_template\simpack_name" %1 /E/Q/K/I
del /S/Q "%1\*.pyc"
del /S/Q "%1\*.pyo"

@echo on