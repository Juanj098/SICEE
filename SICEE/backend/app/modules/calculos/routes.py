from . import bp, services


@bp.get('/conjuntos/<int:conjunto_id>/iwa')
def iwa_conjunto(conjunto_id):
    datos = services.iwa_conjunto(conjunto_id)
    if datos is None:
        return {'error': f'No existe el conjunto de pruebas {conjunto_id}'}, 404
    return datos, 200


@bp.get('/datos/<int:prueba_id>')
def list_datos(prueba_id):
    """Devuelve la prueba con sus fases, ollas, mediciones y catálogos."""
    datos = services.get_datos(prueba_id)
    if datos is None:
        return {'error': f'No existe la prueba_wbt con id {prueba_id}'}, 404
    return datos, 200

@bp.get('/datos/pruebawbt')
def get_pruebawbt():
    existe = services.exist_prueba_wbt()
    return {'status': 'ok', 'existe_prueba_wbt': existe}, 200

@bp.get('/datos/calcular/<int:prueba_id>')
def calcular_prueba(prueba_id):
    datos = services.calculo_fases(prueba_id)
    if datos is None:
        return {'error': f'No existe la prueba_wbt con id {prueba_id}'}, 404
    
    return datos, 200

@bp.get('/datos/list/<int:prueba_id>')
def listar_prueba(prueba_id):
    datos = services.get_data(prueba_id)
    if datos is None:
        return {'error': f'No existe la prueba_wbt con id {prueba_id}'}, 404
    
    return datos, 200


@bp.get('/pruebas/<int:prueba_id>/resultado')
def resultado_prueba(prueba_id):
    """Métricas IWA y valores de referencia de la prueba."""
    datos = services.resultado_prueba_de(prueba_id)
    if datos is None:
        return {'error': f'No existe la prueba_wbt con id {prueba_id}'}, 404

    return datos, 200
