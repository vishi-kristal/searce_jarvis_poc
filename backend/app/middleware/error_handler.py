from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.exceptions import AgentAPIError, NetworkError, ValidationError
from app.utils.logger import logger
import traceback

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": exc.errors()
            }
        }
    )

async def agent_api_error_handler(request: Request, exc: AgentAPIError):
    """Handle agent API errors"""
    logger.error(f"Agent API error: {exc.message} (Status: {exc.status_code})")
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": {
                "code": "AGENT_API_ERROR",
                "message": exc.message,
                "details": exc.details
            }
        }
    )

async def network_error_handler(request: Request, exc: NetworkError):
    """Handle network errors"""
    logger.error(f"Network error: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": {
                "code": "NETWORK_ERROR",
                "message": exc.message,
                "details": exc.details
            }
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred",
                "details": str(exc) if request.app.state.DEBUG else None
            }
        }
    )

def setup_error_handlers(app: FastAPI):
    """Setup all error handlers"""
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(AgentAPIError, agent_api_error_handler)
    app.add_exception_handler(NetworkError, network_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)

