from . import bp, services


@bp.get('/datos/<int:prueba_id>')
def list_datos(prueba_id):
    datos = services.get_datos(prueba_id)
    if datos is None:
        return {'error': f'No existe la prueba_wbt con id {prueba_id}'}, 404
    return datos, 200


@bp.get('/datos/pruebawbt')
def get_pruebawbt():
    existe = services.exist_prueba_wbt()
    return {'status': 'ok', 'existe_prueba_wbt': existe}, 200

@bp.get('/datos/calcular/<int: prueba_id>')
def calcular_prueba(id):
    datos = services.get_datos(id)
    return None