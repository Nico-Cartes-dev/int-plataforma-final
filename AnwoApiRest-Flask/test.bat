@echo off

cls
echo ******************************************************
echo * PONGA MUCHA ATENCION A LAS SGUIENTES INSTRUCCIONES *
echo ******************************************************
echo.
echo Antes de probar la API Rest de ANWO, debe estar 
echo iniciado el servidor Flask en otra consola.
echo.
echo Si aun no lo ha hecho, entonces ejecute el script:
echo.
echo start.bat
echo.
echo antes de continuar con esta prueba...
echo.
pause

call C:\BuenosAires\integracion-plataforma\AnwoApiRest-Flask\.venv\Scripts\activate.bat
call C:\BuenosAires\integracion-plataforma\AnwoApiRest-Flask\.venv\Scripts\python.exe test.py
