from database.db import conectar_bd
from utils.mensaje_error import formato_error
from utils.formato_time import fecha,fecha_hora
        
class ReporteModel():

    def reporte_materiales_ingresados(fecha_inicio,fecha_fin,estado):
        try:
            resultado_final = [False, 'No hay datos!']
            conn = conectar_bd()
            with conn.cursor() as cursor:
                if estado == '':
                    estado = None
                cursor.execute('CALL ReporteMaterialesIngresados(%s, %s, %s);',
                               (fecha_inicio,fecha_fin,estado))
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'fecha_programada': fecha(fila[0]),
                            'registro_ingreso': fecha_hora(fila[1]) if fila[1] is not None else '',
                            'estado_ingreso': fila[2],
                            'observacion': fila[3],
                            'encargado': fila[4],
                            'deposito': fila[5],
                            'material': fila[6],
                            'cantidad_material': fila[7]
                        }
                        datos_consulta.append(dato)
                    resultado_final=[True, datos_consulta]
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)
            error = formato_error(ex)
            return [False, error]
        
    def reporte_materiales_enviados(fecha_inicio,fecha_fin,estado,minimo_material_total):
        try:
            resultado_final = [False, 'No hay datos!']
            conn = conectar_bd()
            with conn.cursor() as cursor:
                if estado == '':
                    estado = None
                cursor.execute('CALL ReporteMaterialesEnviados(%s, %s, %s, %s);',
                               (fecha_inicio,fecha_fin,estado,minimo_material_total))
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'proyecto': fila[0],
                            'salida_programada': fecha(fila[1]),
                            'registro_salida': fecha_hora(fila[2]) if fila[2] is not None else '',
                            'estado_transporte': fila[3],
                            'tipo_material': fila[4],
                            'material': fila[5],
                            'total_material': fila[6]
                        }
                        datos_consulta.append(dato)
                    resultado_final=[True, datos_consulta]
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)
            error = formato_error(ex)
            return [False, error]

    def reporte_stock(p_deposito,p_tipo_material):
        try:
            resultado_final = [False, 'No hay datos!']
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute('CALL ReporteStock(%s, %s);',(p_deposito,p_tipo_material))
                resultado_sql = cursor.fetchall()
                if resultado_sql:
                    datos_consulta=[]
                    for fila in resultado_sql:
                        dato = {
                            'deposito': fila[0],
                            'tipo_material': fila[1],
                            'material': fila[2],
                            'descripcion': fila[3],
                            'cantidad_material': fila[4]
                        }
                        datos_consulta.append(dato)
                    resultado_final=[True, datos_consulta]
            conn.close()
            return resultado_final
        except Exception as ex:
            print(ex)
            error = formato_error(ex)
            return [False, error]
        