from flask import Blueprint, jsonify, request, session, render_template, url_for, redirect, render_template

# Entidades
from entidades.transporte import Transporte
from entidades.recepcion_transporte import RecepcionTransporte
# Modelos
from .transporte_model import TransporteModel

rt_transporte = Blueprint('transporte_bp', __name__, template_folder='templates')

@rt_transporte.route('/', methods=['GET'])
def menu_transporte():
    return render_template('transporte.html')

@rt_transporte.route('/reg_transporte', methods=['GET','POST'])
def reg_transporte():
    if request.method == 'POST':
        data = request.json
        id_proyecto = data.get('id_proyecto')
        fecha_salida = data.get('fecha_salida'),
        lista_materiales = data.get('lista_materiales')
        ent_tranporte = Transporte(id_proyecto=id_proyecto,fecha_salida=fecha_salida)
        resultado = TransporteModel.registrar_transporte(ent_tranporte,lista_materiales)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'mensaje':resultado[1],
                         'redireccion': '/transporte/reg_transporte'}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
        
    elif request.method == 'GET':
        paso = int(request.args.get('paso', 1))
        if paso == 1:
            tb_proyectos = TransporteModel.obtener_proyectos()
            return render_template('reg_transporte1.html', tb_proyectos=tb_proyectos)
        elif paso == 2:
            id_proyecto = int(request.args.get('id_proyecto'))
            tb_stock = TransporteModel.obtener_stock()
            return render_template('reg_transporte2.html', tb_stock=tb_stock, id_proyecto=id_proyecto)

@rt_transporte.route('/reg_recepcion_transporte', methods=['GET','POST'])
def reg_recepcion_transporte():
    if request.method == 'POST':
        data = request.json
        id_transporte = data.get('id_transporte')
        observacion = data.get('observacion'),
        estado_transporte = data.get('estado_transporte')
        id_encargado_recepcion = session['datos_id']['id_personal']
        ent_recep_tranporte = RecepcionTransporte(id_transporte=id_transporte,observacion=observacion,id_encargado_recepcion=id_encargado_recepcion)
        ent_transporte = Transporte(id=id_transporte,estado=estado_transporte)
        resultado = TransporteModel.registrar_recepcion_transporte(ent_recep_tranporte,ent_transporte)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'mensaje':resultado[1],
                         'redireccion': '/transporte/reg_recepcion_transporte'}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
    elif request.method == 'GET':
        paso = int(request.args.get('paso', 1))
        if paso == 1:
            tb_proyectos = TransporteModel.obtener_proyectos_transporte_salida()
            return render_template('reg_recepcion_transporte1.html', tb_proyectos=tb_proyectos)
        elif paso == 2:
            id_proyecto = int(request.args.get('id_proyecto'))
            tb_transportes = TransporteModel.obtener_transportes_de_proyecto(id_proyecto)
            return render_template('reg_recepcion_transporte2.html',tb_transportes=tb_transportes)


@rt_transporte.route('/obtener_detalles_transporte/<id_transporte>', methods=['GET'])
def obtener_detalles_transporte(id_transporte):
    detalle_transporte = TransporteModel.obtener_detalle_de_transporte(id_transporte)
    return detalle_transporte