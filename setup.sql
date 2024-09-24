USE master;
GO

-- Eliminar la base de datos si ya existe
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'DeaceroDB')
BEGIN
    ALTER DATABASE DeaceroDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE DeaceroDB;
END
GO

-- Crear la base de datos
CREATE DATABASE DeaceroDB;
GO

-- Usar la base de datos creada
USE DeaceroDB;
GO

-- Habilitar CDC en la base de datos si no está habilitado
IF NOT EXISTS (SELECT is_cdc_enabled FROM sys.databases WHERE name = 'DeaceroDB' AND is_cdc_enabled = 1)
BEGIN
    EXEC sys.sp_cdc_enable_db;
END
GO

-- Eliminar la tabla CatLineasAereas si ya existe
IF OBJECT_ID('dbo.CatLineasAereas', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.CatLineasAereas;
END
GO

-- Crear la tabla CatLineasAereas
CREATE TABLE dbo.CatLineasAereas (
    Code VARCHAR(10) PRIMARY KEY,       -- Código de la línea aérea, clave primaria
    Linea_Aerea VARCHAR(100)            -- Nombre de la línea aérea
);
GO

-- Eliminar la tabla Vuelos si ya existe
IF OBJECT_ID('dbo.Vuelos', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.Vuelos;
END
GO

-- Crear la tabla Vuelos
CREATE TABLE dbo.Vuelos (
    Cve_LA VARCHAR(10),                 -- Clave de la línea aérea, clave foránea hacia CatLineasAereas
    Viaje DATE,                         -- Fecha del viaje
    Clase VARCHAR(50),                  -- Clase del vuelo (Economy, First Class, etc.)
    Precio DECIMAL(10, 2),              -- Precio del vuelo
    Ruta VARCHAR(50),                   -- Ruta del vuelo (ej. DAL-ATL)
    Cve_Cliente INT,                    -- Clave del cliente
    FOREIGN KEY (Cve_LA) REFERENCES dbo.CatLineasAereas(Code) -- Relación con la tabla CatLineasAereas
);
GO

-- Eliminar la tabla Pasajeros si ya existe
IF OBJECT_ID('dbo.Pasajeros', 'U') IS NOT NULL
BEGIN
    DROP TABLE dbo.Pasajeros;
END
GO

-- Crear la tabla Pasajeros
CREATE TABLE dbo.Pasajeros (
    ID_Pasajero INT PRIMARY KEY,        -- Identificador del pasajero, clave primaria
    Pasajero VARCHAR(100),              -- Nombre del pasajero
    Edad INT                            -- Edad del pasajero
);
GO

-- Habilitar CDC en la tabla CatLineasAereas si no está habilitado
IF NOT EXISTS (SELECT * FROM cdc.change_tables WHERE source_table = 'CatLineasAereas' AND source_schema = 'dbo')
BEGIN
    EXEC sys.sp_cdc_enable_table 
        @source_schema = N'dbo', 
        @source_name = N'CatLineasAereas', 
        @role_name = NULL, 
        @supports_net_changes = 1;
END
GO

-- Habilitar CDC en la tabla Vuelos si no está habilitado
IF NOT EXISTS (SELECT * FROM cdc.change_tables WHERE source_table = 'Vuelos' AND source_schema = 'dbo')
BEGIN
    EXEC sys.sp_cdc_enable_table 
        @source_schema = N'dbo', 
        @source_name = N'Vuelos', 
        @role_name = NULL, 
        @supports_net_changes = 1;
END
GO

-- Habilitar CDC en la tabla Pasajeros si no está habilitado
IF NOT EXISTS (SELECT * FROM cdc.change_tables WHERE source_table = 'Pasajeros' AND source_schema = 'dbo')
BEGIN
    EXEC sys.sp_cdc_enable_table 
        @source_schema = N'dbo', 
        @source_name = N'Pasajeros', 
        @role_name = NULL, 
        @supports_net_changes = 1;
END
GO
