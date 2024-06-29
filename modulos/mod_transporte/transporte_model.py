from database.db import conectar_bd
from utils.mensaje_error import formato_error
from utils.formato_time import fecha
        
class TransporteModel():

    @classmethod
    def registrar_transporte(cls,tra,lista_materiales):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                if not lista_materiales:
                    return [False,"La lista de materiales esta vacia!"]
                else:
                    for materiales in lista_materiales:
                        # Select de verificacion de Stock si cuenta con el material suficiente de abastecimiento
                        verificar= cursor.execute('''SELECT s.id_deposito, s.id_material, s.cantidad_material
                            FROM stock s WHERE s.id_deposito = %s and s.id_material = %s AND s.cantidad_material >= %s;''',
                            (materiales['id_deposito'],materiales['id_material'],materiales['cantidad_material']))
                        if not verificar:
                            return [False, "Revise la lista de materiales"]
                                        
                cursor.execute('''INSERT INTO Transporte (fecha_salida, fecha_hora_registro, observacion, 
                estado, id_proyecto, placa_vehiculo, id_chofer, id_encargado_deposito) VALUES
                (%s,NULL,NULL, 'A',%s,NULL, NULL,NULL);''',(tra.fecha_salida, tra.id_proyecto))
                id_transporte = cursor.lastrowid

                for materiales in lista_materiales:
                    cursor.execute('''INSERT INTO Detalle_transporte (id_transporte, id_deposito, id_material, 
                    cantidad_material) VALUES (%s, %s, %s, %s);''',
                    (id_transporte, materiales['id_deposito'],materiales['id_material'],materiales['cantidad_material']))
                conn.commit()
            conn.close()
            return [True, 'Registro exitoso!']
        except Exception as ex:
            print(ex)
            error = formato_error(ex)
            return [False, error]
    
    @classmethod
    def registrar_recepcion_transporte(cls,recep_tra,transporte):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                if transporte.estado == 'E':
                    cursor.execute('''INSERT INTO Recepcion_transporte (fechahora_entrega, observacion, id_encargado_recepcion, id_transporte) 
                    VALUES (NOW(),%s,%s,%s);''',(recep_tra.observacion, recep_tra.id_encargado_recepcion, recep_tra.id_transporte))
                cursor.execute('''UPDATE Transporte t SET t.estado = %s WHERE t.id = %s;''',
                               (transporte.estado, transporte.id))
                conn.commit()
            conn.close()
            return [True, 'Registro exitoso!']
        except Exception as ex:
            print(ex)
            error = formato_error(ex)
            return [False, error]
    
    
    def obtener_stock():
        try:
            resultado_final=[False, 'No hay datos']
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT st.id_deposito as id_depostio, st.id_material as id_material, m.nombre as material, 
                    tm.nombre as tipo_material, d.nombre as deposito, st.cantidad_material as cantidad_material
                FROM stock st
                JOIN deposito d ON st.id_deposito = d.id
                JOIN material m ON st.id_material = m.id
                JOIN tipo_material tm ON m.id_tipo_material = tm.id
                WHERE m.estado = 'A';""")
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'id_deposito': fila[0],
                            'id_material': fila[1],
                            'material': fila[2], 
                            'tipo_material': fila[3],
                            'deposito': fila[4],
                            'cantidad_material': fila[5]
                        }
                        datos_consulta.append(dato)
                    resultado_final=[True, datos_consulta]
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)
            
    def obtener_proyectos():
        try:
            resultado_final= [False,'No hay datos']
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT p.id as id_proyecto, p.nombre, p.fecha_inicio, p.estado, b.nombre
                    FROM proyecto p JOIN barrio b ON p.id_barrio = b.id
                    WHERE p.estado = 'A' ORDER BY p.id DESC;""")
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'id_proyecto': fila[0],
                            'nombre': fila[1],
                            'fecha_inicio': fecha(fila[2]),
                            'estado': fila[3],
                            'barrio': fila[4]
                        }
                        datos_consulta.append(dato)
                    resultado_final=[True, datos_consulta]
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)
            
    
    def obtener_proyectos_transporte_salida():
        try:
            resultado_final= [False,'No hay datos']
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT p.id as id_proyecto, p.nombre, p.fecha_inicio, p.estado, b.nombre,
                COUNT(t.id_proyecto) AS cantidad_transporte
                FROM proyecto p
                JOIN barrio b ON p.id_barrio = b.id
                JOIN transporte t ON t.id_proyecto = p.id
                WHERE p.estado = 'A' AND t.estado = 'A' AND t.fecha_hora_registro IS NOT NULL
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
    
    def obtener_transportes_de_proyecto(id_proyecto):
        try:
            resultado_final= [False,'No hay datos']
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT t.id, t.fecha_salida, t.observacion, v.placa, CONCAT(pl.nombres,' ',pl.p_apellido ) as chofer
                FROM transporte t
                JOIN proyecto p ON t.id_proyecto = p.id
                JOIN vehiculo v ON t.placa_vehiculo = v.placa
                JOIN chofer ch ON t.id_chofer = ch.id
                JOIN personal pl ON ch.id = pl.id
                WHERE t.estado = 'A' AND p.id = %s;""",(id_proyecto,))
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'id': fila[0],
                            'fecha_salida': fecha(fila[1]),
                            'observacion': fila[2],
                            'placa': fila[3],
                            'chofer': fila[4]
                        }
                        datos_consulta.append(dato)
                    resultado_final=[True, datos_consulta]
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)
            
    def obtener_detalle_de_transporte(id_transporte):
        try:
            resultado_final= [False,'No hay datos']
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT dt.id_transporte, d.nombre, m.nombre, dt.cantidad_material
                FROM transporte t 
                JOIN detalle_transporte dt ON dt.id_transporte = t.id
                JOIN deposito d ON dt.id_deposito = d.id
                JOIN material m ON dt.id_material = m.id
                WHERE dt.id_transporte = %s;""",(id_transporte,))
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'id': fila[0],
                            'deposito': fila[1],
                            'material': fila[2],
                            'cantidad_material': fila[3]
                        }
                        datos_consulta.append(dato)
                    resultado_final=[True, datos_consulta]
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)