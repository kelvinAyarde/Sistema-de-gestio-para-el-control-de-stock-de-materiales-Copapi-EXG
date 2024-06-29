from flask import Blueprint, jsonify, request, session, render_template, url_for, redirect, render_template

# Entidades
from entidades.transporte import Transporte
# Modelos
from .stock_model import StockModel

rt_stock = Blueprint('stock_bp', __name__, template_folder='templates')

@rt_stock.route('/', methods=['GET'])
def menu_stock():
    return render_template('stock.html')

@rt_stock.route('/reg_salida_transporte', methods=['GET','POST'])
def reg_salida_transporte():
    if request.method == 'POST':
        data = request.json
        id_transporte = data.get('id_transporte')
        id_chofer = data.get('id_chofer')
        placa_vehiculo = data.get('placa_vehiculo')
        observacion = data.get('observacion')
        id_encargado_deposito = session['datos_id']['id_personal']
    
        ent_tranporte = Transporte(id=id_transporte, id_chofer=id_chofer, placa_vehiculo=placa_vehiculo,
                                   observacion=observacion,id_encargado_deposito=id_encargado_deposito)
        resultado = StockModel.registrar_salida_transporte(ent_tranporte)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'mensaje':resultado[1],
                         'redireccion': '/stock/reg_salida_transporte'}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
        
    elif request.method == 'GET':
        paso = int(request.args.get('paso', 1))
        if paso == 1:
            tb_proyectos = StockModel.obtener_proyectos_transporte()
            return render_template('reg_salida_transporte1.html', tb_proyectos=tb_proyectos)
        elif paso == 2:
            id_proyecto = int(request.args.get('id_proyecto'))
            tb_transportes = StockModel.obtener_transportes(id_proyecto)
            select_vehiculos = StockModel.obtener_vehiculos_transporte()
            select_choferes = StockModel.obtener_choferes_transporte()
            return render_template('reg_salida_transporte2.html', id_proyecto=id_proyecto,tb_transportes=tb_transportes,
                                   select_vehiculos=select_vehiculos,select_choferes=select_choferes)
    
