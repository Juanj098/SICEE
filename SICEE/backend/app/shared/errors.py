class AppError(Exception):
    status_code=500
    message="Error Interno"

    def __init__(self, message=None, details=None):
        self.message = message or self.message
        self.details = details

class NotFoundError(AppError):
    status_code=404
    message="Recurso no encontrado"

class ValidationError(AppError):
    status_code=400
    message="Datos Invalidos"

def register_error_handler(app):
    @app.errorhandler(AppError)
    def handle_app_error(e):
        return {"error":{"message": e.message, "details": e.details}}, e.status_code
    