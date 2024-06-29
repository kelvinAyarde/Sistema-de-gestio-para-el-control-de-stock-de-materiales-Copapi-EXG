from flask import Blueprint, jsonify, request, session, render_template, url_for, redirect, render_template

# Entidades
from entidades.proyecto import Proyecto
# Modelos
from .proyecto_model import ProyectoModel

rt_proyecto = Blueprint('proyecto_bp', __name__, template_folder='templates')

@rt_proyecto.route('/', methods=['GET'])
def menu_proyecto():
    return render_template('proyecto.html')

@rt_proyecto.route('/mostrar_proyectos', methods=['GET'])
def mostrar_proyectos():
    proyectos = ProyectoModel.mostrar_proyectos()
    return render_template('mostrar_proyectos.html',tabla_proyectos=proyectos)

@rt_proyecto.route('/modificar_proyecto', methods=['GET','PUT'])
def modificar_proyecto():
    if request.method == 'PUT':
        data = request.json
        id_proyecto = data.get('id_proyecto')
        nombre = data.get('nombre')
        estado = data.get('estado')
        ent_proyecto = Proyecto(id=id_proyecto,nombre=nombre,estado=estado)
        resultado = ProyectoModel.modificar_proyecto(ent_proyecto)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'mensaje':resultado[1],
                         'redireccion': '/proyecto/mostrar_proyectos'}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
    elif request.method == 'GET':
        datos_proyecto= {
            'id': request.args.get('id'),
            'nombre': request.args.get('nombre'),
            'fecha_inicio': request.args.get('fecha_inicio'),
            'estado': request.args.get('estado'),
            'barrio': request.args.get('barrio'),
            'servicios': request.args.get('servicios')
        }
        return render_template('pe_modificar_proyecto.html',datos_proyecto=datos_proyecto)

@rt_proyecto.route('/reg_proyecto', methods=['GET','POST'])
def reg_proyecto():
    if request.method == 'POST':
        data = request.json
        nombre = data.get('nombre')
        fecha_inicio = data.get('fecha_inicio')
        id_barrio = data.get('id_barrio')
        id_servicios = data.get('id_servicios', [])
        ent_proyecto = Proyecto(nombre=nombre,fecha_inicio=fecha_inicio,estado='A',id_barrio=id_barrio)
        resultado = ProyectoModel.registrar_proyecto(ent_proyecto,id_servicios)
        if resultado[0]:
            respuesta = {'exito':True ,'titulo':'exito', 'mensaje':resultado[1],
                         'redireccion': '/proyecto/reg_proyecto'}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':resultado[1]}
            return jsonify(respuesta)
    elif request.method == 'GET':
        dato_barrios = ProyectoModel.obtener_barrios()
        dato_servicios = ProyectoModel.obtener_servicios()
        return render_template('reg_proyecto.html',dato_barrios=dato_barrios,dato_servicios=dato_servicios)

