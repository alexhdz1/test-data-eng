# Usar la imagen oficial de SQL Server
FROM mcr.microsoft.com/mssql/server:2019-latest

# Establecer el usuario root para poder instalar paquetes y copiar archivos
USER root

# Aceptar términos de la licencia de ODBC y evitar interacción del usuario
ENV ACCEPT_EULA=Y
ENV DEBIAN_FRONTEND=noninteractive

# Instalar las herramientas de SQL Server (sqlcmd, bcp) y otras dependencias de Python
RUN apt-get update && \
    apt-get install -y mssql-tools unixodbc-dev python3 python3-pip && \
    pip3 install pandas pyodbc && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && \
    apt-get clean

# Crear directorio de aplicación
RUN mkdir -p /usr/src/app

# Copiar el script de inicialización de Python al contenedor desde la carpeta db
COPY db/init_script.py /usr/src/app/init_script.py

# Copiar el script de creación de tablas al contenedor desde la raíz
COPY setup.sql /usr/src/app/setup.sql

# Cambiar permisos de los archivos copiados
RUN chmod 644 /usr/src/app/init_script.py && chmod 644 /usr/src/app/setup.sql

# Cambiar al usuario mssql para ejecutar SQL Server
USER mssql

# Variables de entorno necesarias para SQL Server
ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=YourStrong@Passw0rd!

# Exponer el puerto de SQL Server
EXPOSE 1433

# Iniciar SQL Server y asegurarse de que se ejecute correctamente
ENTRYPOINT ["/bin/bash", "-c", "/opt/mssql/bin/sqlservr"]

# Ejecutar el script de creación de tablas después de iniciar SQL Server
CMD /bin/bash -c "sleep 30 && /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P '$SA_PASSWORD' -i /usr/src/app/setup.sql && python3 /usr/src/app/init_script.py"
