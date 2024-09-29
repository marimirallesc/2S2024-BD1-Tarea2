-- Script para Cargar los Datos de la Segunda Tarea Programada BD1

-- Borra los Datos existentes y reinicia Ids
DELETE dbo.Movimiento;
DBCC CHECKIDENT ('Movimiento', RESEED, 0);
DELETE dbo.Empleado;
DBCC CHECKIDENT ('Empleado', RESEED, 0);
DELETE dbo.Puesto;
DBCC CHECKIDENT ('Puesto', RESEED, 0);	
DELETE dbo.TipoEvento;
DELETE dbo.TipoMovimiento;
DELETE dbo.Usuario;
DELETE dbo.Error;	
DBCC CHECKIDENT ('Error', RESEED, 0);

-- Cargar el archivo XML: Datos.xml
DECLARE @xmlDatos XML;
SET @xmlDatos = (
    SELECT CAST(BulkColumn AS XML) 
    FROM OPENROWSET(
		BULK 'C:\cloudclusters\DatosTarea2.xml',
        SINGLE_BLOB) AS Datos
);

-- Cargar los datos de Puestos
INSERT INTO [dbo].[Puesto]
	([Nombre]
	,[SalarioxHora])
SELECT
    P.value('@Nombre', 'VARCHAR(64)')
    ,P.value('@SalarioxHora', 'MONEY')
FROM @xmlDatos.nodes('/Datos/Puestos/Puesto') AS Puestos(P);


-- Cargar los datos de TiposEventos
INSERT INTO [dbo].[TipoEvento] 
	([Id]
	,[Nombre])
SELECT
    TE.value('@Id', 'INT')
    ,TE.value('@Nombre', 'VARCHAR(64)')
FROM @xmlDatos.nodes('/Datos/TiposEvento/TipoEvento') AS TiposEventos(TE);


-- Cargar los datos de TiposMovimientos
INSERT INTO [dbo].[TipoMovimiento] 
	([Id]
	,[Nombre]
	,[TipoAccion])
SELECT
    TM.value('@Id', 'INT')
    ,TM.value('@Nombre', 'VARCHAR(64)')
    ,TM.value('@TipoAccion', 'VARCHAR(10)')
FROM @xmlDatos.nodes('/Datos/TiposMovimientos/TipoMovimiento') AS TiposMovimientos(TM);


-- Cargar los datos de Usuarios
INSERT INTO [dbo].[Usuario] 
	([Id]
	,[Username]
	,[Password])
SELECT
    U.value('@Id', 'INT')
    ,U.value('@Nombre', 'VARCHAR(64)')
    ,U.value('@Pass', 'VARCHAR(64)')
FROM @xmlDatos.nodes('/Datos/Usuarios/usuario') AS Usuarios(U);


-- Cargar los datos de Errores
INSERT INTO [dbo].[Error]
	([Codigo]
	,[Descripcion])
SELECT
    Er.value('@Codigo', 'INT')
    ,Er.value('@Descripcion', 'VARCHAR(128)')
FROM @xmlDatos.nodes('/Datos/Error/error') AS Errores(Er);


-- Cargar los datos de Empleados
-- Primero se usa una tabla variable para cargar los datos del XML
DECLARE @Empleado TABLE (	
	Puesto VARCHAR(64)
	, ValorDocumentoIdentidad INT
	, Nombre VARCHAR(64)
	, FechaContratacion DATE
	);
INSERT @Empleado (
	Puesto
	, ValorDocumentoIdentidad
	, Nombre
	, FechaContratacion)
SELECT
    E.value('@Puesto', 'VARCHAR(64)')
    ,E.value('@ValorDocumentoIdentidad', 'INT')
    ,E.value('@Nombre', 'VARCHAR(64)')
    ,E.value('@FechaContratacion', 'DATE')
FROM @xmlDatos.nodes('/Datos/Empleados/empleado') AS Empleados(E);
-- Se insertan los empleados a la BD usando la Tabla variable y INNER JOIN
INSERT INTO [dbo].[Empleado] (
	IdPuesto
	, ValorDocumentoIdentidad
	, Nombre
	, FechaContratacion)
SELECT
	P.Id
	, E.ValorDocumentoIdentidad
	, E.Nombre
	, E.FechaContratacion
FROM @Empleado E
INNER JOIN dbo.Puesto P on E.Puesto = P.Nombre; 
-- Usamos el nombre del puesto para mapear y obtener el id del puesto

-- Cargar los datos de Movimientos
-- Primero se usa una tabla variable para cargar los datos del XML
DECLARE @Movimiento TABLE (
	ValorDocId INT
	, IdTipoMovimiento VARCHAR(64)
	, Fecha DATE
	, Monto MONEY
	, PostByUser VARCHAR(64)
	, PostInIP VARCHAR(32)
	, PostTime DATETIME
	);
INSERT @Movimiento (
	ValorDocId
	, IdTipoMovimiento
	, Fecha
	, Monto
	, PostByUser
	, PostInIP
	, PostTime)
SELECT
    M.value('@ValorDocId', 'INT'),
    M.value('@IdTipoMovimiento', 'VARCHAR(64)'),
    M.value('@Fecha', 'DATE'),
    M.value('@Monto', 'MONEY'),
    M.value('@PostByUser', 'VARCHAR(64)'),
    M.value('@PostInIP', 'VARCHAR(32)'),
    M.value('@PostTime', 'DATETIME')
FROM @xmlDatos.nodes('/Datos/Movimientos/movimiento') AS Movimientos(M);
-- Se usa una segunda tabla variable que optiene los ids por mapeo
DECLARE @Movimientos TABLE (
	Sec INT IDENTITY (1,1)
	, IdEmpleado INT
	, IdTipoMovimiento INT
	, Fecha DATE
	, Monto MONEY
	, IdPostByUser INT
	, PostInIp VARCHAR(32)
	, PostTime DATETIME
	);
INSERT @Movimientos (
	IdEmpleado
	, IdTipoMovimiento
	, Fecha
	, Monto
	, IdPostByUser
	, PostInIp
	, PostTime)
SELECT 
	E.Id
	, TM.Id
	, Fecha
	, Monto
	, U.Id
	, PostInIp
	, PostTime
FROM @Movimiento M
INNER JOIN dbo.Empleado E on E.ValorDocumentoIdentidad = M.ValorDocId
INNER JOIN dbo.TipoMovimiento TM on TM.Nombre = M.IdTipoMovimiento
INNER JOIN dbo.Usuario U on U.Username = M.PostByUser;

DECLARE @lo INT = 1;
DECLARE @hi INT;
SELECT @hi = MAX(Sec) from @Movimientos;

DECLARE @IdEmpleado INT;
DECLARE @IdTipoMovimiento INT;
DECLARE @Fecha DATE;
DECLARE @Monto MONEY;
DECLARE @IdPostByUser INT;
DECLARE @PostInIp VARCHAR(32);
DECLARE @PostTime DATETIME;

-- Se itera sobre la tabla @Movimentos, llamando a un SP
-- que incerta cada movimiento de uno en uno
WHILE (@lo <= @hi)
BEGIN
	SELECT 
		@IdEmpleado = M.IdEmpleado
		, @IdTipoMovimiento = M.IdTipoMovimiento
		, @Fecha = M.Fecha
		, @Monto = M.Monto
		, @IdPostByUser = M.IdPostByUser
		, @PostInIp = M.PostInIp
		, @PostTime = M.PostTime
	FROM @Movimientos M
	WHERE M.Sec = @lo;

	EXECUTE [dbo].[CargarMovimiento] 
		@IdEmpleado
		, @IdTipoMovimiento
		, @Fecha
		, @Monto
		, @IdPostByUser
		, @PostInIp
		, @PostTime
		, 0;

	SET @lo = @lo + 1;

END;





