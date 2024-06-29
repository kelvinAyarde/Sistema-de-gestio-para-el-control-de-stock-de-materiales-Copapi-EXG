from database.db import conectar_bd
from utils.mensaje_error import formato_error
from utils.formato_time import fecha
        
class ProyectoModel():

    @classmethod
    def registrar_proyecto(cls,pro,id_servicios):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                # Verificar si el servicio esta activo
                if not id_servicios:
                    return [False,"El servicio no fue seleccionado"]
                else:
                    for id_servicio in id_servicios:
                        cursor.execute('''SELECT estado FROM Servicio WHERE id = %s''',(id_servicio,))
                        servicio_estado = cursor.fetchone()
                        if servicio_estado[0] != 'A':
                            return [False,"El servicio no esta activo"]
                # Insertar en la tabla Proyecto
                cursor.execute('''INSERT INTO Proyecto (nombre, fecha_inicio, id_barrio, estado) 
                               VALUES (%s, %s, %s, %s)''',(pro.nombre, pro.fecha_inicio, pro.id_barrio,'A'))
                id_proyecto = cursor.lastrowid

                # Insertar en la tabla Proyecto_servicio
                for id_servicio in id_servicios:
                    cursor.execute('''INSERT INTO Proyecto_servicio (id_proyecto, id_servicio) 
                                   VALUES (%s, %s)''',(id_proyecto, id_servicio))
                conn.commit()
            conn.close()
            return [True, 'Registro exitoso!']
        except Exception as ex:
            print(ex)
            error = formato_error(ex)
            return [False, error]
        
    @classmethod
    def modificar_proyecto(cls,pro):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute('''UPDATE Proyecto SET nombre = %s, estado =  %s WHERE id = %s;''',
                               (pro.nombre, pro.estado, pro.id))
                conn.commit()
            conn.close()
            return [True, 'Modificacion exitosa!']
        except Exception as ex:
            print(ex)
            error = formato_error(ex)
            return [False, error]
    
    def mostrar_proyectos():
        try:
            resultado_final= [False,'No hay datos']
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT p.id as id_proyecto, p.nombre, p.fecha_inicio, p.fecha_fin, p.estado, 
                               b.nombre, GROUP_CONCAT(s.nombre SEPARATOR ', ') as servicios
                FROM proyecto p
                JOIN proyecto_servicio ps ON ps.id_proyecto = p.id
                JOIN servicio s ON ps.id_servicio = s.id
                JOIN barrio b ON p.id_barrio = b.id
                GROUP BY p.id
                ORDER BY p.id DESC;""")
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'id': fila[0],
                            'nombre': fila[1],
                            'fecha_inicio': fecha(fila[2]),
                            'fecha_fin': fecha(fila[3]) if fila[3] is not None else '',
                            'estado': fila[4],
                            'barrio': fila[5],
                            'servicios': fila[6]
                        }
                        datos_consulta.append(dato)
                    resultado_final=[True, datos_consulta]
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)
        
    def obtener_barrios():
        try:
            resultado_final={'id': '','nombre': 'No hay datos'}
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT b.id, b.nombre, b.ubicacion FROM barrio b;""")
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'id': fila[0],
                            'nombre': fila[1] 
                        }
                        datos_consulta.append(dato)
                    resultado_final=datos_consulta
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)
    
    def obtener_servicios():
        try:
            resultado_final={'id': '','nombre': 'No hay datos'}
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT s.id, s.nombre FROM servicio s WHERE s.estado = 'A';""")
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'id': fila[0],
                            'nombre': fila[1]
                        }
                        datos_consulta.append(dato)
                    resultado_final=datos_consulta
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)