Para ejecutar este programa, primero hay que seguir las siguientes instrucciones:

1. Instalar el driver ODBC 17 para SQL Server, que se encuentra dentro de la 
   carpeta del proyecto y se llama: "msodbcsql_v17.msi", o en la url:
   https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16&viewFallbackFrom=sql-server-ver17

2. Crear un ambiente virtual ejecutando el archivo: "create-venv.bat", que
   contiene los siguientes comandos:
      pip install flask
      pip install pyodbc
      pip install requests

   Se recomienda crear el ambiente virtual antes de arrancar la API REST, para
   asegurar que tome el Python del PC del programador. El ambiente se puede
   crear todas las veces que se quiera, ya que el archivo "create-venv.bat"
   elimina el ambiente actual y lo crea nuevamente.

3. Corregir las cadenas de conexión a la base de datos, que se encuentran al principio de los siguientes archivos:
   
   create-store-procedures.py
   apirest.py

   En caso de que aparezca uno de estos nombres en las cadenas de conexión a BD, se debe saber que:
   "AOAWSB03LC1100" es el nombre del PC del Profesor en DUOC Sala 2309 y
   "z80\SQLEXPRESS" es el nombre del Notebook del Profesor

   Para que todo funcione bien, se debe usar el nombre de servidor e instancia
   del PC que esté usando el programador, por lo que debes considerar
   que en los laboratorios de DUOC es el nombre del PC y en tu casa lo
   más probable es que sea "NOMBRE_DE_TU_PC\SQLEXPRESS"

4. Ejecutar el programa servidor de API REST con el comando:
      .\venv\Scripts\python.exe apirest.py
   o simplemente:
      start.bat

5. Dejar corriendo el servidor en una consola y en otra 
   consola a parte probar el cliente de la API REST 
   ejecutando el comando:
      .\venv\Scripts\python.exe test.bat
   o simplemente:
      test.bat


