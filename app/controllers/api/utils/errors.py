
class ServiceError(Exception):
    def __init__(self, message=None):
        super().__init__(message or "No se pudo realizar la operación.")

    def to_dict(self):
        return {}

class UnauthorizedError(ServiceError):
    def __init__(self, message=None):
        super().__init__(message or "Se requiere estar autenticado.")

class BadRequestError(ServiceError):
    def __init__(self, message=None):
        super().__init__(message or "La solicitud no es válida.")

class FormValidationError(ServiceError):
    def __init__(self, errors, message=None):
        super().__init__(message or "Error al validar el formulario.")

        self.errors = errors
    
    def to_dict(self):
        return {
            **super().to_dict(),
            **self.errors
        }

class NotFoundError(ServiceError):
    def __init__(self, message=None):
        super().__init__(message or "No se encontró el recurso solicitado.")

class LimitError(ServiceError):
    def __init__(self, message=None):
        super().__init__(message or "Se superó el límite.")
