
import functools

from app.controllers.api.utils.errors import ServiceError

def service(function):
    @functools.wraps(function)
    def service_wrapper(*args, **kwargs):
        try:
            data = function(*args, **kwargs)

            return {
                "success": True,
                "data": data
            }
        except Exception as error:
            service_error = error if isinstance(error, ServiceError) else ServiceError()
            error_data = service_error.to_dict()
            
            return {
                "success": False,
                "error": {
                    "type": service_error.__class__.__name__,
                    "message": str(service_error),
                    **({"data": error_data} if error_data else {})
                }
            }

    return service_wrapper
