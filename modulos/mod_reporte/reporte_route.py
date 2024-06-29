from flask import Blueprint, jsonify, request, session, render_template, url_for, redirect, render_template

# Modelos
from .reporte_model import ReporteModel

rt_reporte = Blueprint('reporte_bp', __name__, template_folder='templates')

@rt_reporte.route('/', methods=['GET'])
def menu_reporte():
    return render_template('reporte.html')


@rt_reporte.route('/materiales_enviados', methods=['GET','POST'])
def reporte_materiales_enviados():
    if request.method == 'POST':
        data = request.json
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin= data.get('fecha_fin')
        estado_transporte= data.get('estado_transporte')
        minimo_material_total= int(data.get('minimo_material_total'))
        resultado = ReporteModel.reporte_materiales_enviados(fecha_inicio,fecha_fin,estado_transporte,minimo_material_total)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'contenido':resultado[1]}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
    elif request.method == 'GET':
        return render_template('materiales_enviados.html')

@rt_reporte.route('/materiales_ingresados', methods=['GET','POST'])
def reporte_materiales_ingresados():
    if request.method == 'POST':
        data = request.json
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin= data.get('fecha_fin')
        estado_ingreso= data.get('estado_ingreso')
        resultado = ReporteModel.reporte_materiales_ingresados(fecha_inicio,fecha_fin,estado_ingreso)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'contenido':resultado[1]}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
    elif request.method == 'GET':
        return render_template('materiales_ingresados.html')
    
@rt_reporte.route('/reporte_stock', methods=['GET','POST'])
def reporte_stock():
    if request.method == 'POST':
        data = request.json
        p_deposito= data.get('p_deposito')
        p_tipo_material= data.get('p_tipo_material')
        resultado = ReporteModel.reporte_stock(p_deposito,p_tipo_material)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'contenido':resultado[1]}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
    elif request.method == 'GET':
        return render_template('reporte_stock.html')

