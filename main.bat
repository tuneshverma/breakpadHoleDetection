ECHO ON

REM A batch script to execute a Python script

set root=C:\Users\tunes\anaconda3

call %root%\Scripts\activate.bat %root%
 
call python C:\Users\tunes\Maxerience\image_processing\Brakepad\Brakepad\hole_c\main.py

PAUSE