from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.schemas.response import BaseResponse
import traceback

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
    """处理HTTP异常"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail} - Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponse(
            code=exc.status_code,
            message=exc.detail
        ).dict()
    )

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理请求验证异常"""
    error_details = []
    for error in exc.errors():
        field = "".join([str(item) for item in error["loc"]])
        msg = error["msg"]
        error_details.append(f"{field}: {msg}")
    
    error_message = ", ".join(error_details)
    logger.error(f"Validation Error: {error_message} - Path: {request.url.path}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=BaseResponse(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Validation error",
            data={"errors": error_details}
        ).dict()
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """处理数据库异常"""
    logger.error(f"Database Error: {str(exc)} - Path: {request.url.path}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=BaseResponse(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Database operation failed"
        ).dict()
    )

async def general_exception_handler(request: Request, exc: Exception):
    """处理一般异常"""
    logger.error(f"Unexpected Error: {str(exc)} - Path: {request.url.path}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=BaseResponse(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error"
        ).dict()
    )
