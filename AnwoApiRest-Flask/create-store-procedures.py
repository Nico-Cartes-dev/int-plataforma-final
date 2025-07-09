import pyodbc
import os

# PCROBERTO
pc="NICO"
conn_str = conn_str = f'DRIVER=ODBC Driver 17 for SQL Server; SERVER={pc}\\SQLEXPRESS; DATABASE=base_datos; UID=sa; PWD=123;'

# Crear un Stored Procedure (SP)
def eliminar_y_recompilar_sp(nombre_sp, cuerpo_sp):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Eliminar el SP si existe
        print(f"Eliminando el Stored Procedure {nombre_sp} si es que existe...")
        cursor.execute(f"""
            IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = '{nombre_sp}')
                DROP PROCEDURE {nombre_sp}
        """)

        conn.commit()

        # Crear el SP nuevamente
        print(f"Creando el Stored Procedure {nombre_sp}...")
        cursor.execute(cuerpo_sp)
        conn.commit()

        print(f"Stored Procedure {nombre_sp} creado con éxito\n")
    except pyodbc.Error as e:
        print("Error de SQL Server:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':

    os.system('cls')
    
    # Crear procedimientos almacenados del CRUD de AnwoStockProducto

    # OPERACION DE CREATE
    SP_CREAR_ANWO_STOCK_PRODUCTO = """
        CREATE PROCEDURE SP_CREAR_ANWO_STOCK_PRODUCTO
            @nroserieanwo NVARCHAR(100),
            @nomprodanwo NVARCHAR(100),
            @precioanwo INT,
            @reservado NVARCHAR(1)
        AS
        BEGIN
            INSERT INTO AnwoStockProducto (nroserieanwo, nomprodanwo, precioanwo, reservado)
            VALUES (@nroserieanwo, @nomprodanwo, @precioanwo, @reservado)
        END
    """
    eliminar_y_recompilar_sp('SP_CREAR_ANWO_STOCK_PRODUCTO', SP_CREAR_ANWO_STOCK_PRODUCTO)

    # OPERACION DE READ
    SP_LEER_ANWO_STOCK_PRODUCTO = """
        CREATE PROCEDURE SP_LEER_ANWO_STOCK_PRODUCTO
            @nroserieanwo NVARCHAR(100)
        AS
        BEGIN
            SELECT * FROM AnwoStockProducto WHERE nroserieanwo = @nroserieanwo
        END
    """
    eliminar_y_recompilar_sp('SP_LEER_ANWO_STOCK_PRODUCTO', SP_LEER_ANWO_STOCK_PRODUCTO)

    # OPERACION DE READ ALL
    SP_LEER_TODOS_ANWO_STOCK_PRODUCTO = """
        CREATE PROCEDURE SP_LEER_TODOS_ANWO_STOCK_PRODUCTO
        AS
        BEGIN
            SELECT * FROM AnwoStockProducto
        END
    """
    eliminar_y_recompilar_sp('SP_LEER_TODOS_ANWO_STOCK_PRODUCTO', SP_LEER_TODOS_ANWO_STOCK_PRODUCTO)

    # UPDATE: Store Procedure para actualizar un producto ANWO
    SP_ACTUALIZAR_ANWO_STOCK_PRODUCTO = """
        CREATE PROCEDURE SP_ACTUALIZAR_ANWO_STOCK_PRODUCTO
            @nroserieanwo NVARCHAR(100),
            @nomprodanwo NVARCHAR(100),
            @precioanwo INT,
            @reservado NVARCHAR(1)
        AS
        BEGIN
            UPDATE AnwoStockProducto
            SET nomprodanwo = @nomprodanwo, precioanwo = @precioanwo, reservado = @reservado
            WHERE nroserieanwo = @nroserieanwo
        END
    """
    eliminar_y_recompilar_sp('SP_ACTUALIZAR_ANWO_STOCK_PRODUCTO', SP_ACTUALIZAR_ANWO_STOCK_PRODUCTO)

    # DELETE: Store Procedure para eliminar un producto ANWO
    SP_ELIMINAR_ANWO_STOCK_PRODUCTO = """
        CREATE PROCEDURE SP_ELIMINAR_ANWO_STOCK_PRODUCTO
            @nroserieanwo NVARCHAR(100)
        AS
        BEGIN
            DELETE FROM AnwoStockProducto WHERE nroserieanwo = @nroserieanwo
        END
    """
    eliminar_y_recompilar_sp('SP_ELIMINAR_ANWO_STOCK_PRODUCTO', SP_ELIMINAR_ANWO_STOCK_PRODUCTO)

    # RESERVAR: Store Procedure para reservar o anular la reserva de un producto ANWO
    SP_RESERVAR_EQUIPO_ANWO = """
        CREATE PROCEDURE SP_RESERVAR_EQUIPO_ANWO
            @nroserieanwo NVARCHAR(100),
            @reservado NVARCHAR(1)
        AS
        BEGIN
            /*
                Ejemplos de ejecucion del procedimiento:
                
                EXEC SP_RESERVAR_EQUIPO_ANWO 'A9', 'S'
                SELECT * FROM AnwoStockProducto WHERE nroserieanwo = 'A9' --DEBE ENTREGAR UNA FILA CON reservado = 'S'

                EXEC SP_RESERVAR_EQUIPO_ANWO 'A9', 'N'
                SELECT * FROM AnwoStockProducto WHERE nroserieanwo = 'A9' --DEBE ENTREGAR UNA FILA CON reservado = 'N'
            */

            UPDATE AnwoStockProducto
            SET reservado = @reservado
            WHERE nroserieanwo = @nroserieanwo
        END
    """
    eliminar_y_recompilar_sp('SP_RESERVAR_EQUIPO_ANWO', SP_RESERVAR_EQUIPO_ANWO)