from database.db import conectar_bd
from utils.mensaje_error import formato_error
from utils.formato_time import fecha
        
class StockModel():

    @classmethod
    def registrar_salida_transporte(cls,tra):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                
                print(tra.observacion, tra.placa_vehiculo,tra.id_chofer, tra.id_encargado_deposito, tra.id)
                cursor.execute('''UPDATE Transporte t SET t.fecha_hora_registro = NOW(), t.observacion = %s, 
                               t.placa_vehiculo = %s, t.id_chofer = %s, t.id_encargado_deposito = %s WHERE t.id = %s;''',
                               (tra.observacion, tra.placa_vehiculo,tra.id_chofer, tra.id_encargado_deposito, tra.id))
                conn.commit()
            conn.close()
            return [True, 'Registro exitoso!']
        except Exception as ex:
            print(ex)
            error = formato_error(ex)
            return [False, error]
        
    def obtener_proyectos_transporte():
        try:
            resultado_final= [False,'No hay datos']
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT p.id as id_proyecto, p.nombre, p.fecha_inicio, p.estado, b.nombre,
                COUNT(t.id_proyecto) AS cantidad_transporte
                FROM proyecto p
                JOIN barrio b ON p.id_barrio = b.id
                JOIN transporte t ON t.id_proyecto = p.id
                WHERE p.estado = 'A' AND t.estado = 'A' AND t.fecha_hora_registro IS NULL
                GROUP BY p.id 
                ORDER BY p.id DESC;""")
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'id_proyecto': fila[0],
                            'nombre': fila[1],
                            'fecha_inicio': fecha(fila[2]),
                            'estado': fila[3],
                            'barrio': fila[4],
                            'cantidad_transporte': fila[5]
                        }
                        datos_consulta.append(dato)
                    resultado_final=[True, datos_consulta]
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)
    
    def obtener_transportes(id_proyecto):
        try:
            resultado_final=[False, 'No hay datos']
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT t.id, p.nombre, t.fecha_salida FROM transporte t JOIN proyecto p ON t.id_proyecto = p.id 
                               WHERE t.id_proyecto = %s AND t.fecha_hora_registro IS NULL;""",(id_proyecto,))
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'id': fila[0],
                            'proyecto': fila[1],
                            'fecha_salida': fecha(fila[2])
                        }
                        datos_consulta.append(dato)
                    resultado_final=[True, datos_consulta]
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)
            
    def obtener_vehiculos_transporte():
        try:
            resultado_final=[False, [{'id': '', 'nombre': 'no hay datos'}]]
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT v.placa, v.tipo_vehiculo, CONCAT(mm.modelo, '-', mm.marca) AS modelo_marca
                FROM vehiculo v
                JOIN modelo_marca mm ON mm.id = v.id_modelo_marca
                LEFT JOIN transporte t ON t.placa_vehiculo = v.placa AND t.estado = 'A'
                WHERE t.placa_vehiculo IS NULL
                GROUP BY v.placa, v.tipo_vehiculo, modelo_marca;""")
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'id': fila[0],
                            'nombre': fila[1] +"-"+ fila[2]
                        }
                        datos_consulta.append(dato)
                    resultado_final=[True, datos_consulta]
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)
            
    def obtener_choferes_transporte():
        try:
            resultado_final=[False, [{'id': '', 'nombre': 'no hay datos'}]]
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT ch.id, p.nombres, p.p_apellido
                FROM chofer ch
                JOIN personal p ON p.id = ch.id
                LEFT JOIN transporte t ON t.id_chofer = ch.id AND t.estado = 'A'
                WHERE ch.estado = 'A' AND t.placa_vehiculo IS NULL
                GROUP BY ch.id;""")
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'id': fila[0],
                            'nombre': fila[1]+ "-" +fila[2]
                        }
                        datos_consulta.append(dato)
                    resultado_final=[True, datos_consulta]
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)
            
    