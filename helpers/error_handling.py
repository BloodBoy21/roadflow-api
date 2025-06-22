from fastapi import HTTPException, status
from loguru import logger


def raise_server_error(e:Exception,message:str = "An unexpected error occurred.",status:int=status.HTTP_500_INTERNAL_SERVER_ERROR) -> None:
    """
    Raise a 500 Internal Server Error with the exception message.
    """
    logger.error(f"Server error: {e}")
    raise HTTPException(
        status_code=status,
        detail= f"{message} {str(e)}",
    ) from e
